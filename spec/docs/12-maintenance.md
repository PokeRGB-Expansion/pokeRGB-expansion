# Adoption, maintenance, and contribution plan

This is the proposed workflow for the game repository. It does not imply that a remote repository, contribution service, or release pipeline already exists.

## Contribution workflow

Use issues for precise bug reports and feature proposals, pull requests for changes, and a short contribution guide for the build/test workflow. Use a decision record when a change affects a protected rule, saved data, supported builds, or a major engine interface. Routine fixes do not need a separate governance process.

A correction request should explain the problem, source/reproduction evidence, narrow change, affected behavior, verification, and provenance. Link its stable RGB record. Show failing-before and passing-after results when executable tests are required. The [bug policy](03-bug-fix-policy.md) defines review depth and the [test plan](07-testing-ci.md) defines the evidence.

Keep the [feature catalog](14-features-and-extensions.md#feature-catalog) current with each accepted feature. State Core or Extension, default selection, delivery status, changed behavior, dependencies, save/hardware effects, and supported test cases. Record core inclusion explicitly; an Extension is shared project work with its own release criteria.

For an optional developer system, identify one real use case, dependencies, supported configurations, hardware costs, and behavior when disabled. Include a small use example. A gameplay design choice cannot enter the default core merely by being called a fix.

Keep changes small enough to review. A coupled repair can include all required dependent changes; splitting it must not leave an unsafe intermediate result. Text and simple graphics changes need proportionate checks. Battle, memory, save, and link changes need stronger executable and boundary evidence.

## Deliberate upstream updates

Keep the pristine `pret/pokered` reference and record the implementation's upstream commit. Review relevant updates rather than merging the entire current branch automatically.

For a proposed update:

1. Record the old and new commits and inspect engine, data, memory, build, and tool changes.
2. Rebuild the pristine reference with the applicable pinned tools and check its documented hashes.
3. Integrate the update in a reviewable change. Resolve each affected correction against its record and tests.
4. Run the supported-target builds, protected-mechanics suite, and regressions for affected systems. Add link/save checks when those boundaries change.
5. Update source references, tool pins, compatibility notes, and interface migration notes where needed.

Do not change the upstream pin just to make a conflict disappear. A donor update receives the same review as a new import; a README claim alone is insufficient. Record actual code/asset imports in the ledger described by [provenance](08-provenance.md#record-each-imported-change).

## Release record

Document every difference from upstream, including a build option or a change with identical player behavior. Use one record with its original result, new result, affected presets, reason, evidence and first released game version. Link that record from the release notes. Keep storage internals and historical uncertainty behind the player-facing explanation. [Change guide and examples](16-game-changes.md)

Keep one maintained development line initially and tag releases. Create a separate maintenance branch only when supporting an older release requires it.

Each feature review records its behavior in Minimal, Core, and Extended, including inherited rules and any options. Use the [preset examples](14-features-and-extensions.md#product-presets) and attach the test for any gameplay difference.

Each game release records:

- Source/upstream commits, target configuration, tools, assets, and test-suite revisions.
- Included RGB corrections, known inherited defects, and explicit deferred cases.
- A short mechanics change table with the original result, released result, trigger, compatibility effect, and links to the RGB record and tests. Naming a bug alone does not explain the changed rule.
- Supported targets, hardware modes, and save/link versions, with completed test evidence.
- Reproducible output hashes and, for distributed patches, exact input and applied-output hashes.
- Applicable credits/notices and build/customization instructions.

Do not publish an unfinished support claim as a release result. A known inherited quirk can remain with an explicit disposition. New serious regressions or failures of advertised behavior block release. The [roadmap](09-roadmap.md) defines the gates for each stage.

## Community use

Credit reports, implementations, and assets accurately. Offer generally useful findings to their source projects when appropriate; contact or publication is a separate action. Contributors can share a foundation while choosing different rules for their own games.

Evaluate usefulness through reproducible builds, understandable corrections, and downstream developers completing real changes with less duplicated engine work. Adoption does not require painless migration from an existing hack.

## Adoption and visibility

Developer adoption and public attention are project goals. Plan visibility for the public launch. PokéRGB Expansion is the preferred working name. Its description must make clear that small Gen 1 hacks can use the base as directly as projects with later-generation systems.

Proposed release and outreach plan:

1. Lead with a clear project description and a short demonstration of delivered work. Explain the broad ambition through the roadmap, with planned capabilities labeled.
2. Provide a quick start that reaches a working small customization. Include the default example and, when available, one optional-feature example. Each uses the shared engine.
3. Prepare release notes and a concise public announcement around the developer problems that release solves. Include working demonstrations, source links, and contribution steps. Choose community channels during release preparation.
4. Make useful contribution tasks easy to find. Credit contributors, respond to reproducible reports, and document extension interfaces so downstream work can become shared improvements.
5. Track attention and actual use separately. Record independent developers who build and customize the base, downstream projects that use it, and reusable contributions. Stars, views, and discussion can measure reach; they do not establish adoption on their own.

Use early adoption feedback to improve the examples, documentation, and feature priorities.

## Main risks and checks

| Risk | Control | Evidence to review |
|---|---|---|
| A repair or donor import changes a protected rule | Narrow corrections and independent expected results | Before/after defect test plus neighboring mechanics results |
| Individually sound changes interact badly | Test their shared state and dependencies | Combined turn/event cases and explicit compatibility notes |
| Future capacity work breaks saves, links, or hardware | Change representation only for a measured need | Boundary IDs/banks, save round trips, both endpoints, and hardware costs |
| A variant leaks gameplay data or reuses stale outputs | Keep gameplay and cosmetics distinct; isolate target outputs | Clean/incremental builds and Green/Blue equality results |
| Attribution or source history becomes unclear | Preserve history, notices, and the import ledger | Actual source commit, author/asset record, and retained notices |
| Tooling grows harder to maintain than the engine | Begin with a small runner and useful diagnostics | A contributor can run focused checks and recreate failures |
| Internal milestones get mistaken for release scope | Track every accepted Core behavior against the public gate | The integrated release candidate passes the full register and all color checks |
| Useful work gets little attention or developer use | Plan launch materials, runnable examples, and a clear first-edit guide | Independent build/edit reports, downstream projects, and reusable contributions |

This register does not classify every possible risk. Add a specific entry when an implementation exposes a new material failure mode.
