# 🚨 IncidentFrameAI

An AI-powered **Incident Frame Identification** pipeline that combines **Computer Vision observations** and **witness statements** to produce structured incident data and generate professional incident reports.

The project demonstrates how Large Language Models (LLMs) can be used for evidence attribution, incident classification, conflict detection, and automated report generation while explicitly distinguishing between **Observed**, **Reported**, and **Inferred** information.

Everything runs **completely locally** using **Ollama + Qwen 3**, ensuring privacy and eliminating dependency on cloud APIs.

---

# ✨ Features

- 📹 Computer Vision + Witness Statement fusion
- 🧠 Structured Incident Frame Identification
- 📄 Strict JSON schema generation
- 📊 Automatic confidence estimation
- 🔍 Evidence attribution
- ⚖️ Conflict detection
- ❓ Unknown information tracking
- 📝 Professional Markdown report generation
- 📑 PDF report generation
- 🖥️ Interactive Command-Line Interface (CLI)
- 🚀 Automatic Ollama detection and startup
- 📂 External Computer Vision JSON input
- 💬 Interactive witness statement collection
- 📁 Automatic numbered output generation
- 💻 Runs completely locally using **Ollama + Qwen 3**

---

# 🔄 Pipeline

```
                   CCTV Video
                        │
                        ▼
          Computer Vision Processing
                        │
      Structured CV Observations (JSON)
                        │
                        │
Witness Statements ─────┘
                        │
                        ▼
         Frame Identification Agent
                (Qwen 3 via Ollama)
                        │
                        ▼
              Structured Incident JSON
                        │
                        ▼
          Report Generation Agent
                (Qwen 3 via Ollama)
                        │
                        ▼
          Markdown Incident Report
                        │
                        ▼
               PDF Incident Report
```

---

# 📁 Project Structure

```
IncidentFrameAI/
│
├── ReportCompiler.py
├── README.md
├── LICENSE
├── path.txt                 # Optional (custom Ollama location)
│
├── assets/
│
├── incident_output_*.json
├── incident_report_*.md
└── incident_report_*.pdf
```

---

# 🏷️ Supported Incident Frames

The Frame Identification Agent classifies incidents into one of the following categories:

- 🥊 Fight
- 🚫 Bullying
- 💰 Theft
- 🎨 Vandalism
- 🚷 Trespassing
- 🚑 Medical Emergency
- 🔥 Fire
- ⚠️ Accident
- 👀 Suspicious Activity
- ✅ Normal Activity

---

# 📦 JSON Output Schema

The Frame Identification Agent produces a structured JSON object containing:

- 🏷️ Frame classification
- 📍 Metadata
- 👥 Participants
- ⏱️ Chronological events
- 🔎 Evidence
- ⚖️ Conflicts
- ❓ Unknown information

Example:

```json
{
    "frame": {
        "label": "Fight",
        "confidence": 82
    },

    "metadata": {
        "location": "Science Block",
        "date": "2026-07-22",
        "time": "12:37:14"
    },

    "participants": [
        {
            "id": "Person_1",
            "role": "Unknown",
            "confidence": 65
        }
    ],

    "events": [
        {
            "sequence": 1,
            "event": "Fall",
            "description": "Person fell to the ground.",
            "evidence_type": "Observed",
            "confidence": 90,
            "source": [
                "CAM-03"
            ],
            "supports_frame": true
        }
    ]
}
```

---

# 🧠 Prompt Design

The Frame Identification Agent follows several core principles:

- 👁️ Separate **Observed**, **Reported**, and **Inferred** events.
- 🚫 Never convert witness statements into observed facts.
- 📌 Explicitly attribute evidence sources.
- ⚖️ Detect mutually exclusive witness statements.
- ❓ Preserve uncertainty rather than hallucinating missing information.
- 📊 Assign confidence values based on supporting evidence.
- 📄 Produce only valid JSON conforming to a predefined schema.
- 🏷️ Restrict classifications to predefined incident frame labels.
- 👥 Keep witnesses separate from incident participants.
- 🔄 Merge duplicate events while preserving evidence attribution.

The Report Generation Agent converts the structured incident JSON into a formal incident report while preserving uncertainty, evidence attribution, and conflict information.

---

# 💻 Command-Line Interface

After startup, IncidentFrameAI launches an interactive CLI.

Available commands:

| Command | Description |
|----------|-------------|
| `/help` | Display available commands |
| `/review-default` | Run the built-in demonstration incident |
| `/review` | Review an incident using an external Computer Vision JSON file |
| `/status` | Show Ollama connection status and active model |
| `/models` | List installed Ollama models |
| `/clear` | Clear the console |
| `/exit` | Exit IncidentFrameAI |

---

# 🚀 Running the Project

## Requirements

- Python 3.10+
- Ollama
- Qwen 3 model
- markdown-pdf

Install Python dependencies:

```bash
pip install requests markdown-pdf
```

Install the Qwen 3 model:

```bash
ollama pull qwen3
```

Run the application:

```bash
python ReportCompiler.py
```

IncidentFrameAI automatically:

- Detects whether Ollama is already running.
- Starts Ollama if necessary.
- Falls back to a non-administrator launch if administrator startup fails.
- Displays startup progress.
- Opens the interactive CLI.

If Ollama is installed in a non-default location, create a `path.txt` file beside `ReportCompiler.py` containing the full path to:

```
ollama app.exe
```

---

# 🖥️ Example CLI Session

```
======================================================================
IncidentFrameAI CLI
Type /help for available commands.
======================================================================

> /help

Available commands

/review-default
/review
/status
/models
/clear
/help
/exit

> /review

Path to CV observations JSON:
> cv.json

Enter witness statements.

Witness_1:
> I saw two students arguing.

Witness_2:
> One pushed the other.

Witness_3:

...

Review complete.

JSON : incident_output_1.json
Markdown : incident_report_1.md
PDF : incident_report_1.pdf
```

---

# 🔍 Example Workflow

```
Start Program
       │
       ▼
Automatic Ollama Startup
       │
       ▼
IncidentFrameAI CLI
       │
       ├──────────────┐
       ▼              ▼
/review-default   /review
                      │
                      ▼
            Load CV JSON File
                      │
                      ▼
       Enter Witness Statements
                      │
                      ▼
      Frame Identification Agent
                      │
                      ▼
      Structured Incident JSON
                      │
                      ▼
       Report Generation Agent
                      │
                      ▼
        Markdown + PDF Reports
```

---

# 🛠️ Technologies Used

- 🐍 Python
- 🦙 Ollama
- 🤖 Qwen 3
- 📦 JSON
- 📝 Markdown
- 📄 markdown-pdf
- 🖥️ Windows API (ctypes)
- 💻 Command-Line Interface (CLI)

---

# 🚀 Future Improvements

- 🎥 Automatic Computer Vision observation generation from video
- 📡 Real-time CCTV integration
- 📹 Multi-camera evidence fusion
- 📈 Interactive timeline visualization
- 🌐 Web dashboard
- 🔄 Batch incident processing
- 🧠 Configurable LLM selection
- 🌍 Multi-language report generation
- 🗄️ Database integration
- 🔌 REST API

---

# ⚠️ Disclaimer

This project is intended for **research, educational, and demonstration purposes**.

The generated incident classifications and reports are AI-assisted outputs and should **not** be considered definitive evidence or used as the sole basis for disciplinary, legal, or administrative decisions.

All generated reports should be reviewed and verified by an appropriate human authority before being used in operational, legal, or administrative contexts.

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.
