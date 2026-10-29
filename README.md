# 📖 Tom Riddle's Diary

> *"Hello, my name is Tom Riddle."*

An enchanted diary that writes back. You write on the page, your ink soaks in and fades, and then a reply from the memory of 16-year-old Tom Riddle shows up in handwriting. It's a fan project inspired by *Harry Potter and the Chamber of Secrets*.

- ✒️ **Handwritten ink effect:** your words soak into the paper and disappear
- 🧠 **AI replies** in character, powered by Google Gemini (with an optional offline fallback through Ollama)
- 📜 **"Words remembered" page:** the diary keeps the conversation going for the whole session
- 🎵 **Atmosphere:** background music, a page-turn sound when the book opens, and quill sounds as you type (you can mute all of it)
- 🇱🇰 **Sinhala support:** write in Sinhala and it's drawn in a Sinhala handwriting font

---

## 🗺️ How it works

The project has **two parts**, and **both must be running** at the same time:

```
┌──────────────────────────┐   your words    ┌──────────────────────────┐   prompt   ┌────────────────┐
│  FRONTEND (the diary)    │ ──────────────► │  BACKEND (FastAPI)       │ ─────────► │ Google Gemini  │
│  frontend/               │                 │  tom_riddle_backend/     │            │ (or Ollama)    │
│  tom_riddle_diary.html   │ ◄────────────── │  http://localhost:8000   │ ◄───────── │                │
└──────────────────────────┘   Tom's reply   └──────────────────────────┘   reply    └────────────────┘
      opens in your browser                     runs in a terminal window
```

| Folder | What it is |
|---|---|
| [`frontend/`](frontend/) | The diary itself: one HTML page plus its sounds, fonts and textures. You don't need to install or build anything. |
| [`tom_riddle_backend/`](tom_riddle_backend/) | A small Python server that takes your message, asks the AI to answer as Tom Riddle, and sends the reply back. |

---

## ✅ What you need

You only need **two things** (both free):

1. **`uv`**, a tool that installs Python and all of this project's packages for you. You **don't** need to install Python yourself.
2. **A Google Gemini API key**, which is a password that lets the backend use Google's AI. You can get one free in about a minute (see Step 3).

You'll also want a modern web browser (Chrome, Edge, Firefox or Safari) and an internet connection.

---

## 🚀 Setup (first time only)

> 💡 **What's a terminal?** It's the window where you type commands.
> - **Windows:** press the <kbd>Start</kbd> key, type **PowerShell** and open it.
> - **macOS:** press <kbd>Cmd</kbd> + <kbd>Space</kbd>, type **Terminal** and open it.
> - **Linux:** open your Terminal app.
>
> Type (or paste) each command, then press <kbd>Enter</kbd>.

### Step 1: Install `uv`

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

When it finishes, **close the terminal and open a new one** so it can find `uv`. Then check that it worked:

```bash
uv --version
```

You should see something like `uv 0.x.x`. If you get *"command not found"* or *"not recognized"*, see [Troubleshooting](#-troubleshooting).

### Step 2: Download this project

**Option A: with Git** (if you have [Git](https://git-scm.com/downloads) installed):

```bash
git clone https://github.com/amithaisuru/tom-ridle-diary.git
cd tom-ridle-diary
```

**Option B: without Git.** On the GitHub page click the green **Code** button, then **Download ZIP**. Unzip it, then `cd` into the unzipped folder in your terminal, for example:

```bash
cd Downloads/tom-ridle-diary-main
```

### Step 3: Get your Gemini API key

1. Go to **<https://aistudio.google.com/apikey>** and sign in with a Google account.
2. Click **Create API key**.
3. Copy the key (a long string of letters and numbers).

> 🔒 Treat this key like a password. Don't share it or post it online.

### Step 4: Put your key in a `.env` file

The backend reads your key from a file called **`.env`** inside the `tom_riddle_backend` folder. There's a template you can copy:

**Windows (PowerShell):**

```powershell
cd tom_riddle_backend
copy .env.example .env
notepad .env
```

**macOS / Linux:**

```bash
cd tom_riddle_backend
cp .env.example .env
nano .env
```

Paste your key after the `=` so the line looks like this (no spaces and no quotes):

```env
GEMINI_API_KEY=AIzaSyYourKeyGoesHere
```

Save and close the file. (In `nano`: <kbd>Ctrl</kbd>+<kbd>O</kbd>, <kbd>Enter</kbd>, then <kbd>Ctrl</kbd>+<kbd>X</kbd>.)

> ⚠️ **Windows:** make sure the file is named exactly `.env` and **not** `.env.txt`. In File Explorer, turn on **View → Show → File name extensions** to check.

### Step 5: Install the backend's packages

You should still be inside the `tom_riddle_backend` folder. Run:

```bash
uv sync
```

This downloads the right Python version and all the packages. The first time can take a minute or two.

🎉 **Setup is done.** You won't need to repeat these steps.

---

## ▶️ Running the diary (every time)

### 1. Start the backend

Open a terminal, go into the `tom_riddle_backend` folder and start the server:

```bash
cd path/to/tom-ridle-diary/tom_riddle_backend
uv run uvicorn app.main:app --reload
```

It's working when you see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

> 🟢 **Leave this terminal window open.** The diary can only answer while it's running. To stop it later, click the window and press <kbd>Ctrl</kbd>+<kbd>C</kbd>.

### 2. Open the diary

In your file explorer, open the **`frontend`** folder and **double-click `tom_riddle_diary.html`**. It opens in your web browser.

### 3. Write to Tom

1. Click the book to **open the diary**.
2. Click the page and **write something**, for example *"Who are you?"*
3. Press <kbd>Enter</kbd>. Your ink sinks into the page, and a moment later Tom writes back.

Use the 🔊 speaker button to mute or unmute the music and sounds.

---

## 🧯 Troubleshooting

<details>
<summary><b>"The diary could not answer. Check the backend and press Enter to retry."</b></summary>

The page can't reach the backend.

- Make sure the backend terminal is still open and shows `Uvicorn running on http://127.0.0.1:8000`.
- To check that the backend is up, open <http://localhost:8000/docs> in your browser. You should see an API page.
- The diary always talks to **port 8000**. If you started the backend on another port, either restart it without `--port`, or change `CHAT_URL` near the top of the `<script>` in [`frontend/tom_riddle_diary.html`](frontend/tom_riddle_diary.html).
</details>

<details>
<summary><b>Tom keeps replying: "The Dark Lord is currently dealing with lesser beings. Try again in a moment."</b></summary>

The backend is running, but it couldn't get an answer from the AI. Look at the **backend terminal** for a message that starts with `Gemini ...`:

- **`Client Error (400)` or `(403)`:** your API key is missing or wrong. Check `tom_riddle_backend/.env` (see [Step 4](#step-4-put-your-key-in-a-env-file)), then **stop the backend with <kbd>Ctrl</kbd>+<kbd>C</kbd> and start it again**. The key is only read when the server starts.
- **`Client Error (429)`:** you've hit Gemini's free usage limit. Wait a while and try again.
- **`Overloaded (503)`:** Google's servers are busy. Try again in a minute.

If you see `Ollama fallback failed` right after that, it's expected unless you set up the [optional offline fallback](#-optional-offline-fallback-with-ollama).
</details>

<details>
<summary><b><code>uv</code> is "not recognized" / "command not found"</b></summary>

Close **all** terminal windows and open a new one, because the installer only takes effect in new terminals. If that doesn't help, restart your computer, or follow the [official uv install guide](https://docs.astral.sh/uv/getting-started/installation/).
</details>

<details>
<summary><b><code>ModuleNotFoundError: No module named 'app'</code></b></summary>

You ran the command from the wrong folder, or used `fastapi dev`. Make sure you are **inside `tom_riddle_backend`** and use exactly:

```bash
uv run uvicorn app.main:app --reload
```
</details>

<details>
<summary><b>"Address already in use" / port 8000 is busy</b></summary>

Another backend (or another program) is already using port 8000. Close the other terminal that is running the backend, or restart your computer, and try again.
</details>

<details>
<summary><b>The handwriting looks like a normal font, or there's no music</b></summary>

- The handwriting font loads from Google Fonts, so you need an internet connection.
- Browsers block sound until you interact with the page. Click anywhere or press a key and the music will start.
- Check that the 🔊 speaker button isn't set to muted.
</details>

---

## 🌙 Optional: offline fallback with Ollama

If Gemini fails (bad key, quota used up, servers down), the backend tries a **local AI model** through [Ollama](https://ollama.com) before giving up. You don't need this, but it helps if you want the diary to keep answering without Gemini.

1. Install Ollama from <https://ollama.com/download> and start it.
2. Download the model the backend expects (a few GB):
   ```bash
   ollama pull huihui_ai/qwen3.5-abliterated:4B
   ```
3. Keep Ollama running. The backend uses it automatically when Gemini fails.

> Note: the fallback model only sees your latest message, not the earlier conversation.

---

## 🛠️ For developers

### Project structure

```
tom-ridle-diary/
├── frontend/
│   ├── tom_riddle_diary.html   # The whole diary UI (HTML + CSS + JS in one file)
│   ├── sinhala-legacy.js       # Converts Sinhala Unicode for the legacy Sinhala font
│   ├── leather-grain.svg       # Book cover texture
│   ├── audio/                  # Background music and sound effects
│   └── fonts/                  # Sinhala handwriting font
└── tom_riddle_backend/
    ├── .env.example            # Template for your GEMINI_API_KEY
    ├── pyproject.toml          # Python dependencies (managed by uv)
    └── app/
        ├── main.py             # FastAPI app, CORS setup, loads .env
        ├── api/chat.py         # POST /chat/ endpoint
        ├── schemas/chat.py     # Request/response models
        └── services/llm_service.py  # Tom Riddle prompt, Gemini call, Ollama fallback
```

### API

**`POST /chat/`**

Request:

```json
{
  "prompt": "Who are you?",
  "history": [
    { "role": "user",  "content": "Hello" },
    { "role": "model", "content": "Hello. My name is Tom Riddle." }
  ]
}
```

Response:

```json
{ "reply": "A memory, preserved in these pages." }
```

- `history` is optional. Only the **last 10 messages** are sent to the model.
- `role` must be `"user"` or `"model"`.
- Interactive API docs: <http://localhost:8000/docs> (while the backend is running).

Try it from a terminal:

```bash
# macOS / Linux
curl -X POST http://localhost:8000/chat/ -H "Content-Type: application/json" -d '{"prompt": "Who are you?"}'
```

```powershell
# Windows PowerShell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/chat/ -ContentType "application/json" -Body '{"prompt": "Who are you?"}'
```

### Customising

| What | Where |
|---|---|
| Tom's personality / instructions | `TOM_RIDDLE_PROMPT` in [`llm_service.py`](tom_riddle_backend/app/services/llm_service.py) |
| Gemini model | `GEMINI_MODEL` in [`llm_service.py`](tom_riddle_backend/app/services/llm_service.py) |
| Ollama fallback model | `model=` in `generate_chat_reponse` in [`llm_service.py`](tom_riddle_backend/app/services/llm_service.py) |
| Backend URL the diary calls | `CHAT_URL` in [`tom_riddle_diary.html`](frontend/tom_riddle_diary.html) |
| Ink timing, colours, reply size | The `settings` block at the top of the `<script>` in [`tom_riddle_diary.html`](frontend/tom_riddle_diary.html) |
| Music tracks | `musicTracks` in [`tom_riddle_diary.html`](frontend/tom_riddle_diary.html) |

---

## 🙏 Credits

- Sinhala Unicode-to-legacy conversion: [sinhala-unicode-converter](https://github.com/Open-SL/sinhala-unicode-converter) by Janaka Chathuranga (MIT), based on mapping work by the UCSC Language Technology Research Laboratory
- Handwriting font: [Moon Dance](https://fonts.google.com/specimen/Moon+Dance) (Google Fonts)
- Sinhala font: Tharu Digital Nidahasa
- Music: *The Magic Tree* by geoffharvey, and *Magic Mystery* and *Mysterious Music* by hitslab

## ⚖️ Disclaimer

This is an unofficial, non-commercial fan project. *Harry Potter*, Tom Riddle and related names are trademarks of their respective owners. This project is not affiliated with or endorsed by them.
