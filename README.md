# HoI4ModdingPythonScripts

Utility toolkit for Hearts of Iron IV modding, packaged as the `hoi4modtools` Python distribution. The package exposes each automation script as a CLI command while keeping the original interactive wizards intact.

## Available Commands

- `hoi4modtools-statemap` – generate state/strategic region overview maps with optional ID overlays and legends.
- `hoi4modtools-focusgfx` – add missing focus icon sprite definitions to goals and goals_shine GFX files.
- `hoi4modtools-focusshine` – create the complementary shine sprites for focus icons.
- `hoi4modtools-ideagfx` – populate sprite definitions for idea icons in a chosen GFX file.
- `hoi4modtools-localisation` – scan events/focuses/ideas/decisions and append any missing localisation keys.
- `hoi4modtools-manpower` – multiply manpower entries across one or many state history files.
- `hoi4modtools-transfertech` – build (or extend) a scripted effect that shares researched technologies between countries.
- `hoi4modtools-fileformatter` – re-indent Paradox script files for consistent formatting.
- `hoi4modtools-newsheader` – generate scripted localisation headers for HoI4 news events.
- `hoi4modtools-minister` – convert Darkest Hour minister files into HoI4 idea templates (Unicode-friendly).
- `hoi4modtools-usa-election` – transform a CSV of election results into HoI4 event chains (sample input shipped as package data).

All bundled resources (e.g. `hoi4statemapgenerator_colors.pickle`, USA election example CSV) live under `hoi4modtools.data` and are loaded via `importlib.resources`, so they work out-of-the-box after installation.

## Continuous Integration

GitHub Actions (`.github/workflows/ci.yml`) installs the project, runs `ruff` linting, executes `pytest`, and performs a bytecode compilation check on every push or pull request targeting `main`.

## Getting Started

1. **Install locally**
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install -e .
   ```
   For development tools (linting/tests) install the extras: `python -m pip install -e .[dev]`.

2. **Run a command** from the activated environment using any of the CLI names above. The original interactive prompts remain available (e.g. `hoi4modtools-statemap` launches the wizard if no arguments are provided).

3. **VS Code integration:** the repository includes `.vscode/tasks.json` with ready-made tasks (State Map, Focus GFX, Localisation). Use `Ctrl+Shift+P → Run Task` to launch them in a dedicated terminal.

4. **Pause-on-exit support:** commands that previously opened a blocking window (such as the state map generator) still accept `--pause-on-exit` when you need the console to remain open after completion.

## PyCharm Setup

1. Open the project root in PyCharm (`File → Open…`).
2. Configure the interpreter to use the local virtualenv (create one via `py -3 -m venv .venv` if needed).
3. Shared run configurations in `.idea/runConfigurations/` provide shortcuts for the State Map, Focus GFX, and Localisation tools—they appear automatically once the interpreter is set.
4. Workspace-specific files remain untracked thanks to `.idea/.gitignore`.

## License

- Commits at or after the AGPL relicensing commit (`78180abe3c723af9e4e1bba3c50e1688e15f7feb`) are released under the GNU Affero General Public License v3.0. See `LICENSE` or `licenses/LICENSE-AGPL-3.0`.
- Historical commits up to `f487423b2fb01c51fa1a7350f119c66cddd8aceb` remain under the MIT License; the MIT text is archived at `licenses/LICENSE-MIT`.
