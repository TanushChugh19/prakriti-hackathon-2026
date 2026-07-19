"""
Incident Frame Identification Pipeline
----------------------------------------
Stage 1: CV observations + witness statements -> Frame Identification Agent -> Incident JSON
Stage 2: Incident JSON -> Report Generation Agent -> Formal English report

Runs against a locally hosted Qwen 3 model via Ollama.
Prereq: ollama pull qwen3 and ollama serve running on localhost:11434.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import requests
from markdown_pdf import MarkdownPdf, Section

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:8b-q4_K_M"


# ---------------------------------------------------------------------------
# Stage 1: Frame Identification Agent
# ---------------------------------------------------------------------------

FRAME_IDENTIFICATION_PROMPT = """You are a Frame Identification Agent for an incident reconstruction system.

You are given:
1. Structured computer vision observations from CCTV.
2. Raw witness statements (natural language).

Your task: identify the incident frame and produce a structured JSON representation.
Do NOT generate an English report. Output ONLY valid JSON, nothing else.

Rules:
- Separate observations, reports, and inferences.

    -- Observed events come directly from computer vision.
    -- Reported events come directly from witness statements.
    -- Inferred events may only be created by combining multiple pieces of evidence.

    An inferred event must always have
    "evidence_type": "Inferred"
    and list every supporting source.
  
- Every significant computer vision observation must either:

    -- appear in the events list,
    -- appear in the evidence list,
    -- or be explicitly ignored with justification.

- Do not silently omit observations.

- Every event must specify its evidence type.

  Each event must contain an "evidence_type" field whose value is exactly one
  of the following:

  - "Observed"  → Directly observed by the computer vision system.
  - "Reported"  → Reported by one or more witnesses.
  - "Inferred"  → Derived by combining multiple pieces of evidence.

- Do not convert a witness statement into an observed fact.

- Never state an inference as an observed fact.

- If witness statements conflict with each other or with vision data, record
  this under "conflicts" rather than silently picking one.
  
- A conflict exists only when two sources make mutually exclusive claims.

    Incomplete observations,
    different viewing angles,
    or observations made at different times
    are not conflicts.

- Different observations made at different times should not automatically be
  classified as conflicts.

- Do NOT confuse witnesses with participants.
  A witness providing a statement is not necessarily involved in the incident.

- Participants represent people directly involved in the incident.

    Do not create participant entries for witnesses,
    teachers,
    or bystanders unless they actively participated.

- If the identity of a participant is unknown, assign generic identifiers such
  as "Person_1", "Person_2", etc.

- Never infer roles such as "Aggressor", "Victim", or "Initiator" unless they
  are explicitly supported by the available evidence.

- If evidence is insufficient to assign a participant role with confidence,
  record the role as "Unknown" and explain the uncertainty in "unknowns".

- Confidence values are integers from 0 to 100 and should reflect how strongly
  the combined evidence supports each claim.

Confidence Guidelines:

- 90-100:
  Confirmed by multiple independent sources (e.g., computer vision and
  multiple consistent witness statements).

- 70-89:
  Supported by one reliable source and partially corroborated by other
  available evidence.

- 40-69:
  Supported by a single source only, or by multiple sources with minor
  inconsistencies.

- 10-39:
  Weakly supported, speculative, or based on incomplete evidence.

- 0-9:
  No meaningful supporting evidence. Avoid using these values unless
  explicitly indicating extreme uncertainty.

For every confidence value, choose the score using the Confidence Guidelines
above. Do not assign arbitrary numbers.

The confidence should reflect the amount and reliability of supporting
evidence.

Confidence is not a measure of severity.

Confidence measures only how strongly the available evidence supports the claim.

Valid incident frame labels are ONLY:

- Fight
- Bullying
- Theft
- Vandalism
- Trespassing
- Medical Emergency
- Fire
- Accident
- Suspicious Activity
- Normal Activity

The value of "frame.label" MUST be exactly one of the above labels.
Do not invent new frame names such as
"altercation leading to fall" or
"push resulting in crowd formation".
Do not choose a frame solely because a witness claims one occurred.
The selected frame must be supported by the combined evidence.

Merge duplicate events whenever they refer to the same occurrence.

Instead of creating duplicate events,
combine their supporting sources.

Events must be ordered chronologically whenever the available evidence permits.

If the order cannot be determined,
maintain the most likely ordering
and record the uncertainty under "unknowns".

Return exactly one valid JSON object.

Do not include Markdown.

Do not include explanations.

Do not omit required fields.

Every field in the schema must appear exactly once.

Unknown values should be represented using empty strings,
empty arrays,
or "Unknown" rather than omitted.

Output strictly in this JSON schema:
{{
  "frame": {{"label": "", "confidence": 0}},
  "metadata": {{"location": "", "date": "", "time": ""}},
  "participants": [{{"id": "", "role": "", "confidence": 0}}],
  "events": [{{"sequence": 0, "event": "", "description": "", "evidence_type": "", "confidence": 0, "source": [], "supports_frame": true}}],
  "evidence": [{{"source": "", "type": "", "observation": ""}}],
  "conflicts": [{{"statement_1": "", "statement_2": "", "status": ""}}],
  "unknowns": [""]
}}

The JSON schema is mandatory.

Do not rename fields.

Do not add fields.

Do not remove fields.

Every key must exactly match the schema.

Computer Vision Observations:
{cv_observations}

Witness Statements:
{witness_statements}
"""

REPORT_GENERATION_PROMPT = f"""You are an incident reporting assistant.

Today's date is {datetime.now().strftime("%d %B %Y")}.

Prepared by:
IncidentFrameAI

Convert the following incident JSON into a professional, objective incident report.

Requirements:
- Formal English, suitable for a school/workplace administrator.
- Do not invent facts beyond what is in the JSON.
- Explicitly mention uncertainty where confidence values are low or where
  "unknowns" or "conflicts" are present.
- Do not assign blame beyond what the "frame" and "participants" fields
  already state.
- Use the "evidence_type" field when describing events.
- Observed events should be written as confirmed observations.
- Reported events should be written as witness reports.
- Inferred events should be explicitly described as inferences.
- Do not merge separate events into a single sentence if doing so obscures their evidence type or source.

Incident JSON:
{{incident_json}}
"""


def get_next_run_id():
    i = 1
    while Path(f"incident_output_{i}.json").exists():
        i += 1
    return i


def call_ollama(prompt: str, temperature: float = 0.2) -> str:
    """Send a prompt to the local Ollama server and return the raw text response."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        sys.exit(
            "ERROR: Could not connect to Ollama at "
            f"{OLLAMA_URL}. Is ollama serve running?"
        )
    except requests.exceptions.HTTPError as e:
        sys.exit(f"ERROR: Ollama returned an error: {e}\n{resp.text}")

    return resp.json().get("response", "")


def extract_json(raw_text: str) -> dict:
    text = raw_text.strip()

    # Remove markdown code fences if present
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON found in model output.")

    candidate = text[start : end + 1]

    return json.loads(candidate)


def identify_frame(cv_observations: dict, witness_statements: list) -> dict:
    prompt = FRAME_IDENTIFICATION_PROMPT.format(
        cv_observations=json.dumps(cv_observations, indent=2),
        witness_statements="\n\n".join(
            f"[{w['source']}]: {w['statement']}" for w in witness_statements
        ),
    )
    raw = call_ollama(prompt)
    try:
        return extract_json(raw)
    except (ValueError, json.JSONDecodeError) as e:
        print("WARNING: Failed to parse Stage 1 output as JSON.")
        print(f"Raw model output:\n{raw}\n")
        raise e


def generate_report(incident_json: dict) -> str:
    prompt = REPORT_GENERATION_PROMPT.format(
        incident_json=json.dumps(incident_json, indent=2)
    )
    return call_ollama(prompt, temperature=0.4).strip()


# ---------------------------------------------------------------------------
# Dummy input data (school fight scenario, matching the example this
# architecture was tested against)
# ---------------------------------------------------------------------------

DUMMY_CV_OBSERVATIONS = {
    "camera_id": "CAM-03",
    "timestamp": "2026-07-22T12:37:14",
    "location": "Science Block, Outside Chemistry Lab C-204",
    "observations": [
        {"type": "person_count", "value": 8},
        {"type": "running", "detected": True},
        {"type": "fall", "detected": True},
        {"type": "crowd", "detected": True},
    ],
}

DUMMY_WITNESS_STATEMENTS = [
    {
        "source": "Student A",
        "statement": "I saw two boys arguing outside the chemistry lab. One pushed the other and he fell.",
    },
    {
        "source": "Teacher",
        "statement": "I heard shouting around 12:37 PM and found one student on the floor near the lab entrance. About seven students had gathered around.",
    },
    {
        "source": "Student C",
        "statement": "I didn't see anyone get pushed, I just saw a crowd forming and someone already on the ground.",
    },
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 70)
    print("STAGE 1: Frame Identification")
    print("=" * 70)

    incident_json = identify_frame(DUMMY_CV_OBSERVATIONS, DUMMY_WITNESS_STATEMENTS)
    print(json.dumps(incident_json, indent=2))

    print("\n" + "=" * 70)
    print("STAGE 2: Report Generation")
    print("=" * 70)

    run_id = get_next_run_id()

    report = generate_report(incident_json)
    md_file = f"incident_report_{run_id}.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(report)

    pdf = MarkdownPdf(toc_level=0)
    with open(md_file, "r", encoding="utf-8") as f:
        pdf.add_section(Section(f.read()))

    pdf_file = f"incident_report_{run_id}.pdf"
    pdf.save(pdf_file)

    # Save outputs for inspection / downstream use
    out = {
        "generated_at": datetime.now().isoformat(),
        "incident_json": incident_json,
        "report": report,
    }

    json_file = f"incident_output_{run_id}.json"
    with open(json_file, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved full output to incident_output_{run_id}.json")


if __name__ == "__main__":
    main()
