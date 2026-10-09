# WILDSENSE-OFFLINE
WILDSENSE OFFLINE — WINDOWS QUICK START
======================================

FEATURES
- Local website with 12 nature missions and category filters.
- Mission progress stored in this browser.
- Field journal stored locally with JSON export.
- Local AI chat routed to Ollama on this computer.
- No user account, analytics, or cloud AI API is configured.

REQUIREMENTS AND FIRST RUN
--------------------------
Python 3 is required for the local web server. If Python is missing, install
it from https://www.python.org/downloads/windows/ and select "Add Python to PATH".

1. Extract this folder from the ZIP.
2. Connect to the internet for first-time setup.
3. Double-click start.bat.
4. If Ollama is missing, the launcher downloads and opens the official installer.
   You may need to complete its prompts. The launcher cannot bundle Ollama itself.
5. The launcher downloads the llama3.2:1b model through Ollama. Wait for it to finish.
6. Your browser should open http://127.0.0.1:8765. Keep the terminal open.

AFTER SETUP
-----------
Run start.bat whenever you want to use the site. Once Ollama and the model have
been downloaded, the app's main features and AI can run without internet, as long
as Python, Ollama, and the model remain installed. Do not open index.html directly;
the AI chat needs the local server.

LOCAL DATA AND MODEL
--------------------
Progress and journal entries use browser localStorage. Export journal entries as
JSON for backup. The AI chat talks to http://127.0.0.1:11434 on your computer.
The default model is llama3.2:1b. Review current model terms at
https://ollama.com/library/llama3.2. Ollama and the model have separate terms.

LIMITATIONS
-----------
- This is not a visual species-identification app; no image recognition is wired in.
- This is not a PWA and does not cache the website for browser-only offline use.
- First-time setup needs internet and disk space for Ollama and the model.
- Python is not automatically installed by this launcher.
- AI may be incorrect; do not use it to decide if a plant or mushroom is edible.
