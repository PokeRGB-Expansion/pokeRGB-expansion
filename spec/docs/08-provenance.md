# Provenance and distribution

## Settled scope

No project-wide MIT license is added. This decision applies to the proposed derived project; it does not remove existing notices or make someone else's code or assets newly licensed.

Keep this process small and factual. Preserve source history, credit the work used, retain applicable file-level notices, and avoid claims of rights the project has not established. A disclaimer does not create rights or guarantee protection from a takedown.

GitHub's licensing documentation distinguishes a license grant from merely making source visible. The technical spec does not rely on a blanket claim that a missing license permits every reuse. [GitHub licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## What the checked repositories establish

The pinned `pret/pokered`, Solus, Shin Lite, PureRGB and Solid Red trees have no root project-wide `LICENSE`/`COPYING` file under those names. Pokéemerald Expansion also has no such root file, but contains licenses/notices for several tools. The absence of a root file is a limited repository observation, not a complete rights review. [E38](../research/evidence.md#e38)

Pokéemerald Expansion asks users to credit RHH and contributors. That is useful evidence for its attribution practice; it is not an MIT declaration for the whole project. [E35](../research/evidence.md#e35)

This specification imports no donor game code or artwork. Source repositories were read for research. The future implementation should retain upstream Git history and distinguish inherited disassembly, imported contributor work, independently written fixes, tools, and assets.

## Record each imported change

For code or an asset used directly, record the source repository, commit, file/routine, author where known, existing notice, reason for use, and integration changes. Preserve the original commit attribution where appropriate. Link the related bug/test record.

For a newly written implementation informed by a report, credit the report and identify the implementation separately. Do not describe a close port as independent work merely because labels or register choices changed.

For graphics and audio, record the actual creator/source. Do not strip credits because an asset is easy to find online. If a Green asset is based on an original-game asset, describe that provenance accurately.

Use a simple `CREDITS.md` plus a structured import ledger when code imports begin. This spec's [source lock](../research/source-lock.json) is a research ledger; it is not an import or permission ledger.

## Release form

Proposed consumer distribution is patches with exact Red/Blue input hashes and clear build instructions. Green uses an English Blue input because its gameplay foundation is Blue. Select the patch format during release preparation; verify applying it to the documented base and checking the resulting hash.

The current artifact is Markdown and research data only. No consumer ROM, Nintendo asset pack, donor source archive, or ready-to-publish release is included.

Public project text can identify the project as an unofficial fan effort and credit the original game rights holders and community sources. Do not claim Nintendo, Game Freak, Creatures, or The Pokémon Company approval. Do not invent special wording that supposedly prevents enforcement.

## Boundaries still requiring engineering evidence

Patch compatibility, save interoperability and link compatibility are technical test claims. They are not established by provenance or by keeping a familiar cartridge title. Resolve them in the implementation and publish only the tested support matrix.
