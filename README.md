Narrative Consistency Engine

Kharagpur Data Science Hackathon
Track A: Systems Reasoning with NLP and Generative AI

📘 Overview

This project implements a deterministic narrative consistency reasoning system designed to evaluate whether a hypothetical character backstory is logically consistent with a full-length novel.
The system does not judge writing quality or surface-level textual contradictions. Instead, it evaluates whether the proposed backstory respects the causal, behavioral, and narrative constraints established throughout the story.

🎯 Problem Statement

Given:
A complete long-form narrative (100k+ words)
A newly written, plausible character backstory (not part of the novel)
The task is to determine whether the backstory:
Remains consistent over time
Preserves causal reasoning
Respects narrative constraints
Is supported by evidence from the text

📂 Dataset Description

The dataset provided for this challenge consists of three main components:

1. Training File (train.csv)

The training CSV file contains examples of character backstories paired with narrative consistency labels.
It is intended to help participants understand the structure of the data and experiment with reasoning strategies.
Each row typically includes:
Story ID – Unique identifier for the narrative
Backstory – A hypothetical character backstory
Label – Ground-truth consistency indicator (used for development and validation)
Note: The final system does not rely on supervised learning or model fitting, and train.csv is used only for understanding data patterns and refining reasoning rules.

2. Test File (test.csv)

The test CSV file contains unlabeled hypothetical backstories that must be evaluated by the system.
Each row includes:
Story ID – Identifier for the narrative
Backstory – A newly written, plausible character backstory (not part of the novel)
These backstories are deliberately crafted to require causal and narrative reasoning, rather than surface-level contradiction detection.

3. Novel Texts (novels/)

The novels/ directory contains one or more full-length narrative text files in .txt format.
Key properties:
Each file represents a complete long-form narrative (often exceeding 100,000 words)
Texts are unannotated and unstructured
The system scans the entire narrative without truncation
Evidence for decisions may be drawn from any point in the story
Dataset Characteristics
Long-form natural language data
No explicit alignment between backstory and specific passages
Requires reasoning across distant narrative sections
Designed to test consistency over time, causal logic, and narrative constraints

How the Dataset Is Used

train.csv is used for exploratory analysis and rule design
test.csv is used for final evaluation and prediction
novels/ provide the narrative context against which backstories are checked

Dataset Assumptions

Each backstory refers to a central character in the corresponding novel
The backstory is plausible by design, even when inconsistent
Inconsistencies may be subtle and distributed across the narrative

🧠 Approach & Design Philosophy

This system follows a symbolic reasoning and constraint-based approach, aligned with systems reasoning principles, rather than relying solely on black-box predictions.
Core Ideas:
Backstories imply character traits (e.g., non-violent, solitary, impoverished)
Traits impose constraints on possible actions or events
Violations of these constraints indicate narrative inconsistency
All decisions must be explainable and evidence-backed

The system is:
Deterministic
Interpretable
Rule-driven
Hackathon-safe (no external APIs or randomness)

⚙️ System Components
1. File Discovery

Automatically locates the input CSV file and novel directory across common hackathon folder structures.

2. Baseline Grounding Check

Ensures the backstory:
Is present and non-empty
Contains sufficient semantic signals to ground narrative behavior

3. Trait-Based Constraint Reasoning

Checks for logical clashes between:
Backstory-implied traits (signals)
Narrative events (violations)

Examples:

Non-violent → cannot commit murder
Impoverished → cannot suddenly acquire great wealth
Solitary → cannot have unexplained family relationships

4. Evidence-Based Decisions

When an inconsistency is detected:
A relevant excerpt from the narrative is extracted
The rationale explicitly explains the logical clash

📊 Output Format

The system produces a CSV file with the following columns:

| Column Name | Description                          |
| ----------- | ------------------------------------ |
| Story ID    | Identifier from input CSV            |
| Prediction  | `1` = Consistent, `0` = Inconsistent |
| Rationale   | Explanation with supporting evidence |

🚀 How to Run

Requirements
Python 3.9+
pathway
pandas

Execution
python main.py --test-csv test.csv --output results.csv
If --test-csv is not provided, the system automatically searches for the input file.

🧪 Key Properties

✔ Deterministic execution
✔ No external APIs
✔ No embeddings or LLM inference
✔ Full-narrative scan (no truncation)
✔ Explainable, rule-based reasoning
✔ Evidence-backed conclusions

🏁 Final Note

This project demonstrates systems-level narrative reasoning by enforcing logical constraints over long-form text. It aligns directly with the goals of Track A: Systems Reasoning with NLP and Generative AI, emphasizing consistency, causality, and explainability.
