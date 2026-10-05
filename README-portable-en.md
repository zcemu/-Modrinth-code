# Modrinth App — Portable Build (unofficial)

A portable build of the official [Modrinth App](https://github.com/modrinth/code),
with one small addition: **portable mode**.

## How to use

1. Download `Modrinth-App-Portable.zip` and extract it anywhere you like
   (e.g. `D:\Games\ModrinthApp`).
2. Make sure an (empty) file named `portable.txt` sits next to
   `Modrinth App.exe` — it's already included in the zip, so usually
   there's nothing to do.
3. Run `Modrinth App.exe`.

On first launch a `data/` folder is created next to the exe. **Everything**
the launcher stores — database, logs, backups, instances, downloads,
WebView2 cache — lives inside `data/`. Nothing important is written to `C:`.

- Reinstalling Windows doesn't affect it: just keep the folder on another drive.
- Copy the whole folder to a different PC and it just works.
- Delete `portable.txt` to fall back to the official default behavior
  (data stored in `%APPDATA%\ModrinthApp`).

## Notes

- Unofficial build. Source: [`modrinth/code`](https://github.com/modrinth/code)
  plus a ~20-line portable-mode patch (see `apply_portable.py` in this repo).
- The binary is **unsigned**, so Windows SmartScreen will warn on first run:
  click *More info* → *Run anyway*.
- This build has **no auto-updater**. That's intentional: an official update
  would overwrite the portable build and kill portable mode. To update,
  download the newer portable release and replace the exe — your `data/`
  folder (instances, worlds, settings) stays untouched.
