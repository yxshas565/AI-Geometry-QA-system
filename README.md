# AI-Geometry-QA-System

An AI-assisted **geometry quality assurance system** for cartographic vector data.  
This project automates one specific QA task using **rule-based validation**, **machine learning anomaly detection**, and **deterministic, human-readable explanations**.

Built as a hackathon solution aligned with *Option B – Rule-Based Geometry Validation*.

---

## 🎯 Problem Focus

Manual QA of geometric vector data (lines, polygons) is time-consuming and error-prone.  
This system automates **line geometry quality assurance** by detecting structural and statistical anomalies and clearly explaining the results.

**Chosen focus area:**  
**Option B – Rule-Based Geometry Validation**

---

## 🧠 What This System Does

For each line geometry, the system:

1. Validates geometry using deterministic rules  
2. Detects abnormal geometric patterns using ML  
3. Analyzes contextual role-based behavior  
4. Fuses results into a final QA verdict  
5. Generates **clear, human-readable QA explanations**

---

## 🧩 Pipeline Overview

1. Geometry Input  
2. Feature Extraction  
3. Rule-Based Validation  
4. ML Anomaly Detection  
5. Contextual Role Analysis  
6. Decision Fusion (PASS / WARNING / FAIL)  
7. Deterministic QA Explanation  


---

## ✅ Key Features

- ✔ Rule-based geometry validation (topology, structure)
- ✔ ML-based anomaly detection on geometric features
- ✔ Context-aware analysis using role statistics
- ✔ Deterministic decision fusion
- ✔ Verdict-aware, human-friendly explanations
- ✔ Streaming console output (demo-friendly)
- ✔ Secure and stable (no runtime LLM dependency)

---

## 🧪 Example QA Output

Each geometry produces a structured QA report:

- **Severity:** PASS / WARNING / FAIL  
- **Why it was flagged or approved**
- **Where the issue occurs (segment-level if applicable)**
- **Recommended corrective actions**

A final dataset-level summary is also generated.

---

## ▶️ How to Run

```bash
python run_full_pipeline_with_llm.py
```

📁 Project Structure
agent/        → Explanation & decision logic
geometry/     → Geometry parsing & validation
features/     → Feature extraction
models/       → ML anomaly detection
context/      → Role-based contextual analysis
decision/     → Decision fusion engine
data/         → Sample geometry inputs
tests/        → Phase-wise validation tests

🧪 Testing

Phase-wise test scripts are included to validate each stage of the pipeline:

Geometry parsing

Rule validation

ML detection

Context analysis

Decision fusion

Explanation generation

🔐 Why No LLM in Final Output?

LLM-based explanations were experimented with but intentionally disabled in the final pipeline to ensure:
1. Deterministic behavior
2. Zero hallucination risk
3. Stable demo execution
4. Secure public repository (no API keys)
5. Explanations are generated using structured, rule-driven templates instead.

🚀 Why This Exceeds a Basic Solution

A basic solution would:
1. Check one geometry rule
2. Print a simple error message

This system:
1. Combines rules + ML + context
2. Produces actionable QA explanations
3. Mimics real-world GIS QA pipelines


flowchart TD :-
  
    A[Input Vector Line Geometry] --> B[Phase 1: Geometry Parsing & Feature Extraction]

    B --> C[Phase 2: Rule-Based Geometry Validation]
    C -->|Structural issues?| D[Rule Violations Detected]

    B --> E[Phase 3: ML-Based Anomaly Detection]
    E -->|Unusual patterns?| F[Statistical Anomaly Detected]

    B --> G[Phase 4: Contextual Role Analysis]
    G -->|Role deviation?| H[Contextual Anomaly Detected]

    D --> I[Phase 5: Decision Fusion]
    F --> I
    H --> I

    I --> J{Final QA Verdict}
    J -->|PASS| K[Approved Geometry]
    J -->|WARNING| L[Minor Issues Detected]
    J -->|FAIL| M[Critical Geometry Issue]

    K --> N[Phase 6: Deterministic QA Explanation]
    L --> N
    M --> N

    N --> O[Human-Readable QA Report]


This flow illustrates how the system directly aligns with the problem statement by
automating one specific QA task. Geometry validation is first performed using deterministic
rules, enhanced with ML-based anomaly detection and contextual analysis. All signals are
fused into a single QA verdict, followed by a clear, human-readable explanation.
