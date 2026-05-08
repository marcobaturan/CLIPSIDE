# Changelog — CLIPSIDE

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-08

### Added
- **Persistent Project Root**: The IDE now remembers the last opened project directory across sessions (~/.clipside_config.json).
- **Build Buffer (Ctrl+B)**: New command to save the current editor content to a temporary file and load all constructs (rules, templates, facts) into the engine simultaneously.
- **Close File (Ctrl+W)**: Added a close button (✖) in the editor header and a keyboard shortcut to close the active tab.
- **Explorer Enhancements**: Implemented `update_root` to correctly refresh the file tree when opening a new folder.
- **Improved UI Column Layout**: Stabilized the 3-column architecture (Explorer/AI, Editor/Console, Inspector).
- **Inspector Refresh**: Centralized UI refresh logic for Facts, Agenda, and Instances.
- **Streaming AI Chat**: Local Ollama assistant with word-by-word streaming and code snippet insertion.
- **CLIPS Engine Integration**: Thread-safe wrapper for `clipspy` supporting reset, run, step, and eval.

### Changed
- **Menu Structure**: Unified "Build" and "Run" commands in the File and Environment menus.
- **Internal Engine Logic**: Switched from `agenda()` to `activations()` for better compatibility with modern `clipspy`.

### Fixed
- Fixed AttributeError when accessing agenda in CLIPS environment.
- Resolved issues with File Explorer not updating after project folder change.
- Suppressed non-fatal Tkinter lifecycle warnings.

---
*Created by Antigravity AI for Marco Baturan*
