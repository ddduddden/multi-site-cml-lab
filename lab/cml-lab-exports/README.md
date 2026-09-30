# CML Lab Exports

This subtree holds selected, versioned Cisco Modeling Labs YAML exports that represent meaningful architectural milestones. It is not a general backup directory and does not contain every intermediate working copy.

## Purpose

Milestone exports provide:

- a reconstructable CML topology/configuration baseline at significant stages of the build;
- recovery artifacts separate from targeted CLI verification evidence;
- a visible record of how the lab evolves; and
- version-controlled infrastructure artifacts that complement the design and as-built configuration records.

Authentication material is sanitised from public exports. Credential values are replaced with `<sanitised>`. The original unsanitised export is retained privately, so a public GitHub export must not be treated as a credential-complete recovery file until the required authentication values are restored.

## Export workflow

At a selected architectural milestone:

1. Review device state and write the intended running configuration to startup configuration.
2. Fetch the current device configurations using the relevant CML configuration-extraction action.
3. Retitle the CML lab so the exported topology name reflects the current milestone.
4. Create a new YAML lab export rather than overwriting an earlier milestone.
5. Retain the unsanitised export privately.
6. Create a public copy and replace authentication credential values with `<sanitised>`, including local usernames, line passwords, and local/enable secrets, while preserving the surrounding configuration and valid YAML structure. The IOS password-type digit (for example `5`, `7`, or `9`) is retained because it identifies the hash or encoding type without revealing the value. The same sanitisation applies to the per-device files in `configs/`. The Phase 01 and Phase 05 exports predate the username and type-digit convention.
7. Review the public copy for remaining credential material before committing it.
8. Record the CML version used for the export in the accompanying commit/build documentation or `docs/environment.md`.
9. Commit only meaningful milestone exports; incidental working backups remain outside the repository.

## Repository structure

Exports are kept flat within the site directory rather than creating one directory for every phase:

```text
lab/
└── cml-lab-exports/
    ├── README.md
    └── hq/
        ├── hq-phase-01-platform-baseline-2026-09-20.yaml
        ├── hq-phase-05-svi-hsrp-2026-09-29.yaml
        └── hq-phase-07-ospf-area10-2026-09-30.yaml
```

Future site directories are created only when a real export exists.

## Naming convention

Use lowercase kebab-case and include the site, milestone and export date:

```text
<site>-phase-<nn>-<milestone>-YYYY-MM-DD.yaml
```

A date is retained even when the phase number is unique because a milestone may be re-exported after an environment or documentation correction.

## Relationship to other repository content

- `docs/` explains design intent, implementation history and verification outcomes.
- `evidence/` contains targeted proof for verification tests.
- `configs/hq/` contains readable per-device as-built running configurations.
- `diagrams/` contains architecture visuals.
- `lab/cml-lab-exports/` contains selected milestone CML restoration/reconstruction artifacts.

The per-device files in `configs/hq/` remain the readable as-built configuration reference. CML YAML exports package the wider lab state and topology for milestone restoration; they do not replace verification evidence or the per-device configuration records.

## CML MAC-address continuity

CML interface MAC addresses are not assumed to remain identical across imports or node recreation unless they are explicitly pinned. Evidence that depends on bridge IDs or interface MAC addresses should therefore be interpreted alongside the configured STP priorities and topology roles rather than assuming a particular dynamically allocated MAC is permanent.
