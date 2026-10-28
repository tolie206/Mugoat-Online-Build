# Mugoat Online iOS — public build workflow

This repository contains only the build workflow. It does not publish game data, private test inputs, saves, or the private source repository history.

Standard GitHub-hosted macOS runner; manual runs only; source pinned to commit `afa13ea8e6b2cb491f439ecfb90167afa3e9a08e` of `tolie206/Regeneration`. The workflow checks iOS UI, native bridge ABI and regression tests before producing one IPA.

`PRIVATE_SOURCE_TOKEN` must be stored as a GitHub Actions secret with read access to the private source repository. Credentials are not persisted by checkout. Do not paste credentials into commits, workflow inputs or logs. Only the intended IPA is uploaded as an artifact; no raw input archive or compiler log artifact is uploaded.

The app is Mugoat Online, bundle ID `vn.gta.mugoat.online`, based on the separate R007 fork. Initial release is a multiplayer foundation for iOS; full RP accounts, server-authorized assets and production security are not yet complete. A public runner does not make the multiplayer server public or remove per-job runtime/storage limits.

Runner billing reference: https://docs.github.com/en/actions/concepts/billing-and-usage
