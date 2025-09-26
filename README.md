# HoI4ModdingPythonScripts
Collection of Python 3 utilities that automate repetitive Hearts of Iron IV modding tasks.

All scripts live in the `python3/` directory:

- `hoi4statemapgenerator.py` - generate state/strategic region overview maps with optional ID overlays and legends.
- `hoi4focusgfxentry.py` - add missing focus icon sprite definitions to goals and goals_shine GFX files.
- `focusgfxshine.py` - create the complementary shine sprites for focus icons.
- `hoi4ideagfxentry.py` - populate sprite definitions for idea icons in a chosen GFX file.
- `hoi4localisationadder.py` - scan events/focuses/ideas/decisions and append any missing localisation keys.
- `hoi4statemanpowermultiplier.py` - multiply manpower entries across one or many state history files.
- `hoi4transfertechsegen.py` - build (or extend) a scripted effect that shares researched technologies between countries.
- `hoi4fileformatter.py` - re-indent Paradox script files for consistent formatting.
- `hoi4newspaperheaderadded.py` - generate scripted localisation headers for HoI4 news events.
- `DHtoHoi4MinisterConverter_python3.py` - convert Darkest Hour minister files into HoI4 idea templates (Unicode-friendly).
- `USAElectionGenerator.py` - transform a CSV of election results into HoI4 event chains (sample input: `python3/USAElectionGenerator_example.csv`).
- `hoi4statemapgenerator_colors.pickle` - bundled colour palette used by the state map generator.

## License

- Current commits (this change and later) are released under the GNU Affero General Public License v3.0. See `LICENSE` or `licenses/LICENSE-AGPL-3.0`.
- Historical commits up to `f487423b2fb01c51fa1a7350f119c66cddd8aceb` remain under the MIT License; the MIT text is archived at `licenses/LICENSE-MIT`.

## Getting Started

1. Install Python 3.10 or newer from <https://www.python.org/downloads/> and ensure the `py` launcher is added to your PATH.
2. In a terminal opened in the repository root, create and activate a virtual environment, then install dependencies:

   ```powershell
   py -3 -m venv .venv
   .\\.venv\\Scripts\\activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements-python3.txt
   ```

   The requirements file covers all third-party packages used by the scripts (for example `p_tqdm` for the state map generator and `unidecode` for the minister converter).
3. Run any tool from the activated environment. Double-clicking `python3/hoi4statemapgenerator.py` with no arguments now launches an interactive wizard and keeps the console open so you can review errors. You can pass arguments manually as usual, e.g. `python python3/hoi4transfertechsegen.py --help`.
4. Prefer to launch from an existing console but still want pause-on-exit behaviour? Add the `--pause-on-exit` flag where supported (e.g. the state map generator).
