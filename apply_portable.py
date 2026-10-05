#!/usr/bin/env python3
"""Apply the portable-mode source change to a modrinth/code checkout.

Run from the repository root:  python apply_portable.py

What it changes (Windows only):
  1. packages/app-lib/src/state/dirs.rs
     `initial_settings_dir_path()` checks for a `portable.txt` file next to the
     executable first. Priority: portable.txt > THESEUS_CONFIG_DIR > OS default.
  2. apps/app/src/main.rs
     At the top of `main()`, when portable.txt is present, set
     WEBVIEW2_USER_DATA_FOLDER to <exe dir>/data/webview so the WebView2
     runtime does not write its cache to C:.

The script fails loudly (non-zero exit) if an anchor is not found exactly
once, so a CI build never silently ships an unpatched binary.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent

DIRS_RS = ROOT / "packages/app-lib/src/state/dirs.rs"
MAIN_RS = ROOT / "apps/app/src/main.rs"

OLD_DIRS_FN = """\
    pub fn initial_settings_dir_path(app_identifier: &str) -> Option<PathBuf> {
        Self::env_path("THESEUS_CONFIG_DIR")
            .or_else(|| Some(dirs::data_dir()?.join(app_identifier)))
    }
"""

NEW_DIRS_FN = """\
    pub fn initial_settings_dir_path(app_identifier: &str) -> Option<PathBuf> {
        // Portable mode: if a `portable.txt` file exists next to the executable,
        // store all launcher data in a `data` folder next to the executable.
        // Priority: portable.txt > THESEUS_CONFIG_DIR env var > OS default dir.
        Self::portable_data_dir()
            .or_else(|| Self::env_path("THESEUS_CONFIG_DIR"))
            .or_else(|| Some(dirs::data_dir()?.join(app_identifier)))
    }

    /// Returns the portable data directory when portable mode is active.
    ///
    /// Portable mode is enabled by placing an (empty) `portable.txt` file
    /// next to the launcher executable. All Theseus data (database, logs,
    /// backups, instances, downloads) then lives in `<exe dir>/data`,
    /// so reinstalling the OS does not affect it.
    #[cfg(target_os = "windows")]
    pub fn portable_data_dir() -> Option<PathBuf> {
        let dir = std::env::current_exe().ok()?.parent()?.to_path_buf();
        if dir.join("portable.txt").exists() {
            Some(dir.join("data"))
        } else {
            None
        }
    }

    #[cfg(not(target_os = "windows"))]
    pub fn portable_data_dir() -> Option<PathBuf> {
        None
    }
"""

OLD_MAIN_ANCHOR = """\
fn main() {
    #[cfg(feature = "export-app-events")]
"""

NEW_MAIN_ANCHOR = """\
fn main() {
    // Portable mode: keep WebView2 user data next to the executable as well,
    // so nothing launcher-related is written to C: on first launch.
    // Must run before any Tauri/Theseus initialization.
    // (`set_var` is unsafe on recent Rust editions; the `unsafe` block keeps
    // this compiling on both old and new editions.)
    #[cfg(target_os = "windows")]
    if let Ok(exe) = std::env::current_exe() {
        if let Some(dir) = exe.parent() {
            if dir.join("portable.txt").exists() {
                unsafe {
                    std::env::set_var("WEBVIEW2_USER_DATA_FOLDER", dir.join("data").join("webview"));
                }
            }
        }
    }

    #[cfg(feature = "export-app-events")]
"""


def replace_once(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        sys.exit(f"ERROR: anchor found {count} times (expected 1) in {path}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"patched: {path}")


# Upstream bugfix (2026-10-05): newer tauri's `Builder<R, C>` no longer infers
# the config type param from a bare `Builder::new(...)` call (E0283).
# Pin C = () like the api/* plugins already do.
OLD_WINDOW_FRAME = 'tauri::plugin::Builder::new("window-frame")'
NEW_WINDOW_FRAME = 'tauri::plugin::Builder::<_, ()>::new("window-frame")'


def main() -> None:
    for p in (DIRS_RS, MAIN_RS):
        if not p.is_file():
            sys.exit(f"ERROR: not found: {p} (run this script from the repo root)")

    replace_once(DIRS_RS, OLD_DIRS_FN, NEW_DIRS_FN)
    replace_once(MAIN_RS, OLD_MAIN_ANCHOR, NEW_MAIN_ANCHOR)
    replace_once(MAIN_RS, OLD_WINDOW_FRAME, NEW_WINDOW_FRAME)

    # Sanity check: both markers must be present after patching.
    dirs_text = DIRS_RS.read_text(encoding="utf-8")
    main_text = MAIN_RS.read_text(encoding="utf-8")
    assert "portable_data_dir" in dirs_text, "dirs.rs patch did not stick"
    assert "WEBVIEW2_USER_DATA_FOLDER" in main_text, "main.rs patch did not stick"
    assert 'Builder::<_, ()>::new("window-frame")' in main_text, "window-frame fix did not stick"
    print("portable-mode source change applied successfully.")


if __name__ == "__main__":
    main()
