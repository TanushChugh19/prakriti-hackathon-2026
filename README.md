# 🚨 IncidentFrameAI

An AI-powered **Incident Frame Identification** pipeline that combines **computer vision observations** and **witness statements** to produce structured incident data and generate professional incident reports.

The project demonstrates how Large Language Models (LLMs) can be used for evidence attribution, incident classification, and automated report generation while explicitly distinguishing between **observed**, **reported**, and **inferred** information.

---

## ✨ Features

- 📹 Computer Vision + Witness Statement fusion
- 🧠 Structured Incident Frame Identification
- 📄 Strict JSON schema generation
- 📊 Automatic confidence estimation
- 🔍 Evidence attribution
- ⚖️ Conflict detection
- ❓ Unknown information tracking
- 📝 Professional Markdown report generation
- 📑 PDF report generation
- 💻 Runs completely locally using **Ollama + Qwen 3**

---

## 🔄 Pipeline

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

## 📁 Project Structure

```
IncidentFrameAI/
│
├── ReportCompiler.py
├── README.md
├── LICENSE
│
├── incident_output_1.json
├── incident_report_1.md
├── incident_report_1.pdf
│
└── assets/
```

---

## 🏷️ Incident Frames Supported

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

## 📦 JSON Output Schema

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
            "evidence_type": "Observed",
            "confidence": 90
        }
    ]
}
```

---

## 🧠 Prompt Design

The Frame Identification Agent follows several principles:

- 👁️ Separate **Observed**, **Reported**, and **Inferred** events.
- 🚫 Never convert witness statements into observed facts.
- 📌 Explicitly attribute evidence sources.
- ⚖️ Detect mutually exclusive witness statements.
- ❓ Track uncertainty rather than hallucinating missing information.
- 📊 Use confidence scores based on available supporting evidence.
- 📄 Produce only valid JSON conforming to a predefined schema.

The Report Generation Agent converts the structured JSON into a formal incident report while preserving uncertainty and evidence attribution.

---

## 🚀 Running the Project

### 📋 Requirements

- 🐍 Python 3.10+
- 🦙 Ollama
- 🤖 Qwen 3 model
- 📄 markdown-pdf

Install dependencies:

```bash
pip install requests markdown-pdf
```

Install and start Ollama:

```bash
ollama pull qwen3
ollama serve
```

Run the project:

```bash
python ReportCompiler.py
```

Generated outputs:

```
incident_output_1.json
incident_report_1.md
incident_report_1.pdf
```

Each execution automatically creates the next numbered report:

```
incident_output_2.json
incident_report_2.md
incident_report_2.pdf
```

---

## 🛠️ Technologies Used

- 🐍 Python
- 🦙 Ollama
- 🤖 Qwen 3
- 📦 JSON
- 📝 Markdown
- 📄 markdown-pdf

---

## 🔍 Example Workflow

```
Computer Vision Observations
+
Witness Statements
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
Markdown Report
        │
        ▼
PDF Report
```

---

## 🚀 Future Improvements

- 📡 Real-time CCTV integration
- 📹 Multi-camera evidence fusion
- 📈 Timeline visualization
- 🌐 Interactive web dashboard
- 🎯 Evidence confidence calibration
- 🏷️ Support for additional incident categories
- 🎥 Integration with object detection and tracking pipelines
- 🌍 Multi-language report generation

---

## ⚠️ Disclaimer

This project is intended for **research, educational, and demonstration purposes**.

The generated incident classifications and reports are AI-assisted outputs and should **not** be considered definitive evidence or used as the sole basis for disciplinary, legal, or administrative decisions. Human review is always required.

---

## 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.
