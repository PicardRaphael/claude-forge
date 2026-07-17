from __future__ import annotations

import sqlite3

from forge_cognition.domain.models import Principal


def test_verify_store_checks_profile_acl_projection(services) -> None:
    product = services[Principal.FORGE_PRODUCT]
    project = product.project_create(
        name="Verify",
        slug="verify",
        objective="Verify",
        owner="raphael",
        initial_constraints=[],
        idempotency_key="verify-project",
    )
    episode = product.episode_record(
        project_id=project["project_id"],
        title="Private",
        prediction="private",
        actual_outcome=None,
        error_types=[],
        procedures_used=[],
        candidate_lessons=[],
        confidence_before=0.5,
        confidence_after=0.5,
        idempotency_key="verify-private",
    )
    reviewer_path = product.indexes.path_for(Principal.RED_TEAM)
    connection = sqlite3.connect(reviewer_path)
    try:
        connection.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                episode["id"],
                "private/forge-product/episodes/leak.md",
                project["project_id"],
                "episode",
                "leak",
                "candidate",
                0.5,
                "",
                1,
                "sha256:x",
            ),
        )
        connection.commit()
    finally:
        connection.close()
    assert "profile_index_acl_mismatch" in product.system_health()["consistency_errors"]


def test_verify_store_flags_unrecognized_files_without_exposing_contents(services) -> None:
    curator = services[Principal.CURATOR]
    (curator.store.root / "rogue.bin").write_bytes(b"TOP SECRET")
    health = curator.system_health()
    assert "unrecognized_file" in health["consistency_errors"]
    assert "TOP SECRET" not in str(health)
