from __future__ import annotations

import pytest
from concurrent.futures import ThreadPoolExecutor

from forge_cognition.domain.errors import ConflictError, IdempotencyConflictError
from forge_cognition.domain.models import Principal


def proposal(service, *, key: str, content: str = "Evidence body"):
    return service.memory_propose(
        entity_type="evidence",
        project_id=None,
        title="Evidence",
        content=content,
        provenance=[{"type": "user", "reference": "test"}],
        confidence=0.8,
        idempotency_key=key,
    )


def test_idempotency_same_request_returns_same_result(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    first = proposal(product, key="same")
    second = proposal(product, key="same")
    assert second == first


def test_idempotency_key_with_different_payload_is_refused(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    proposal(product, key="conflict")
    with pytest.raises(IdempotencyConflictError):
        proposal(product, key="conflict", content="Different")


def test_optimistic_locking_returns_current_hash(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    curator = services[Principal.CURATOR]
    candidate = proposal(product, key="optimistic")
    with pytest.raises(ConflictError) as error:
        curator.memory_commit(
            candidate_id=candidate["id"],
            decision="validated",
            target_namespace="shared/context",
            expected_hash="sha256:stale",
            idempotency_key="commit-stale",
            reason="test",
        )
    assert error.value.current_hash == candidate["content_hash"]


def test_index_failure_rolls_back_file(services, monkeypatch) -> None:
    product = services[Principal.FORGE_PRODUCT]
    original = product.indexes.rebuild_all
    calls = 0

    def fail_once():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("index failed")
        original()

    monkeypatch.setattr(product.indexes, "rebuild_all", fail_once)
    with pytest.raises(RuntimeError, match="index failed"):
        proposal(product, key="index-failure")
    assert list((product.store.root / "inbox" / "forge-product").glob("*.md")) == []


def test_audit_failure_rolls_back_file_and_index(services, monkeypatch) -> None:
    product = services[Principal.FORGE_PRODUCT]

    def fail(_event):
        raise RuntimeError("audit failed")

    monkeypatch.setattr(product.transactions.audit, "append", fail)
    with pytest.raises(RuntimeError, match="audit failed"):
        proposal(product, key="audit-failure")
    assert list((product.store.root / "inbox" / "forge-product").glob("*.md")) == []
    assert product.system_health()["consistency_errors"] == []


def test_retry_after_transient_index_failure_succeeds(services, monkeypatch) -> None:
    product = services[Principal.FORGE_PRODUCT]
    original = product.indexes.rebuild_all
    calls = 0

    def fail_once():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("transient")
        original()

    monkeypatch.setattr(product.indexes, "rebuild_all", fail_once)
    with pytest.raises(RuntimeError):
        proposal(product, key="retry")
    monkeypatch.setattr(product.indexes, "rebuild_all", original)
    assert proposal(product, key="retry")["id"]


def test_interruption_during_mutation_rolls_back(services) -> None:
    product = services[Principal.FORGE_PRODUCT]

    def interrupted(tx):
        tx.write_text("inbox/forge-product/interrupted.md", "partial")
        raise KeyboardInterrupt("interrupted")

    with pytest.raises(KeyboardInterrupt):
        product.transactions.execute(
            action="interrupted",
            principal=Principal.FORGE_PRODUCT,
            idempotency_key="interrupted",
            request_payload={"x": 1},
            mutate=interrupted,
            result_payload=lambda _value: {},
        )
    assert not (product.store.root / "inbox" / "forge-product" / "interrupted.md").exists()


def test_oversized_serialized_content_is_never_left_on_disk(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    product.store.max_document_bytes = 256
    with pytest.raises(Exception, match="size limit"):
        proposal(product, key="oversized", content="X" * 1000)
    assert list((product.store.root / "inbox" / "forge-product").glob("*.md")) == []


def test_concurrent_same_idempotency_key_converges_to_one_result(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: proposal(product, key="concurrent"), range(2)))
    assert results[0] == results[1]
    assert len(list((product.store.root / "inbox" / "forge-product").glob("*.md"))) == 1
