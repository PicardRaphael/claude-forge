# Store layout

`inbox/` holds unvalidated Product and Red Team proposals. `shared/` holds Curator-governed context, procedures and consolidated calibration. `private/` isolates agent episodes, lessons and calibration. `projects/` holds neutral artifacts, evidence, hypotheses, decisions, experiments, reviews, outcomes and retrospectives. `audit/` is append-only metadata. `indexes/` is disposable. `archive/` holds rejected or retired canonical documents.

Project folders use `PRJ-YYYY-NNN-slug`. `project.yaml` is the project aggregate; Markdown documents use ULIDs and validated frontmatter. Indexes and lock/temp files are never authoritative.

To add a memory type, first extend the domain enum and schema, map its memory class and namespace policy, add a canonical template, then add transition/ACL/index/rebuild tests. Do not create a new root zone unless its trust boundary differs from every existing zone.
