# Clinically Curated Postoperative Oral Cancer Dialogue Dataset

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Paper](https://img.shields.io/badge/Paper-ACL%202026%20Findings-blue.svg)](#11-citation)

This repository releases a **clinically curated Chinese postoperative oral cancer (OC) dialogue dataset** together with **structured facet schemas, clinician-authored clarification prompts, safety cue lexicons, and system prompt specifications**.

The dataset is designed to support research on **safety-aware clinical dialogue systems**, **structured clarification**, and **retrieval-augmented generation (RAG)** in high-risk postoperative care settings.

This release accompanies the paper:

> **Safety-Aware Dialogue System for Postoperative Oral Cancer Care with Structured Clarification and a Clinically Curated Dataset**
> *Findings of the Association for Computational Linguistics (ACL 2026)*

---

## 1. Repository Structure

```
Clinically_Curated_OC_Dataset/
├── qa/
│   └── all.jsonl
│
├── raw_data/
│   └── Q0001.json
│   └── Q0002.json
│   └── …
│
├── data_split/
│   ├── train.jsonl
│   ├── valid.jsonl
│   └── test.jsonl
│
├── schema/
│   ├── facet_schema.json
│   └── clarification_prompts.json
│
├── prompts/
│   ├── generation_system_prompt.txt
│   ├── generation_system_prompt_en.txt
│   ├── protective_mode_prompt_template.txt
│   ├── protective_mode_prompt_template_en.txt
│   └── prompts_readme.md
│
├── safety_lexicon/
│   ├── extreme_negative_cues.txt
│   ├── suicidal_cues.txt
│   └── cue_lexicon_readme.md
│
├── refs/
│   └── refs_catalog.csv
│
├── export_prompts_and_check.py
│
└── README.md
```

---

---

## 2. Quick Start

### 2.1 Load the Dataset in Python

The example below shows how to read the training split and load the corresponding QA instances from `raw_data/`.

```python
import json
import pathlib

root = pathlib.Path("Clinically_Curated_OC_Dataset")
manifest_path = root / "data_split" / "train.jsonl"

with manifest_path.open("r", encoding="utf-8") as f:
    for line in f:
        rec = json.loads(line)
        qa_path = root / rec["path"]
        qa = json.loads(qa_path.read_text(encoding="utf-8"))
        print(qa["id"], qa["text_canonical"], qa["answer"])
```

### 2.2 Load the Unified JSONL File

For batch processing or training, users may directly load the aggregated file:

```python
import json
from pathlib import Path

data_path = Path("Clinically_Curated_OC_Dataset/qa/all.jsonl")

samples = []
with data_path.open("r", encoding="utf-8") as f:
    for line in f:
        samples.append(json.loads(line))

print("Total samples:", len(samples))
print(samples[0]["id"], samples[0]["text_canonical"])
```

### 2.3 Export Clarification Prompts and Check Coverage

The repository also includes a utility script for exporting clarification prompts and checking whether prompt labels cover the labels observed in the released dataset.

Example:
```bash
python export_prompts_and_check.py \
  --dataset-root ./Clinically_Curated_OC_Dataset \
  --check
```

This command will:
- export schema/clarification_prompts.json
- scan raw_data/
- report whether the observed labels are fully covered by the prompt specification

---

## 3. QA Data

### 3.1 Raw QA Format (`raw_data/`)

Each QA item is stored as one JSON file, named by its unique ID (e.g., `Q0001.json`).

Example:

```json
{
  "id": "Q0001",
  "text_canonical": "我和家人一時接受不了疾病的打擊,可以找誰幫忙?",
  "answer": "您可以找其他信任的家人、朋友聊聊天...",
  "source_type": "interview",
  "modality": "verbal",
  "focusp": ["F", "C", "U"],
  "treatment_phase": ["手術前", "手術後"],
  "functional_impact": [],
  "心理問題": true,
  "RTW": false,
  "經濟與社會資源": false,
  "危險字詞": false,
  "癌症復發": false,
  "營養照護": false,
  "傷口與症狀照護": false,
  "治療原因與安排": false,
  "口腔復健與身體活動": false,
  "other_condition": null,
  "pii_checked": true,
  "evidence_ref_ids": ["REF0001"],
  "version": "2024-10-24"
}
```

All data are fully de-identified and reviewed by clinical experts prior to release.

---

### 3.2 Unified QA File (qa/all.jsonl)

For convenience, all QA items are also provided in a single JSONL file:

```
qa/all.jsonl
```

Each line corresponds to one QA object identical to the content in `raw_data/`.

### 3.3 Format Rationale

This repository provides the dataset in two complementary formats:

- `raw_data/`  
  - One JSON file per QA instance  
  - Serves as the **canonical and human-readable version**  
  - Suitable for inspection, annotation, and fine-grained processing  

- `qa/all.jsonl`  
  - Aggregated JSONL file for all QA pairs  
  - Designed for **efficient loading in training pipelines**  
  - Suitable for batch processing and model training  

Both formats contain the same underlying data. Users can choose the format that best fits their workflow.

---

## 4. Dataset Statistics

The dataset consists of a clinically curated collection of postoperative oral cancer–related question–answer (QA) pairs.

- Total QA pairs: 867
- Language: Traditional Chinese
- Domain: Postoperative oral cancer care (rehabilitation, symptom management, daily care, return-to-work considerations)
- Data format: JSON (per-sample) and JSONL (aggregated)

### 4.1 Data Splits
- Train: 694 samples
- Validation: 86 samples
- Test: 87 samples

### 4.2 Included Resources
In addition to QA pairs, the repository also provides:

- Clinician-defined facet schema for structured clarification
- Clarification prompt templates
- Safety lexicon for risk-aware routing
- Prompt specifications used in the dialogue pipeline
- Reference answer catalog for evaluation

This dataset is designed to support research on safe and clinically grounded dialogue systems, rather than general-purpose question answering.

---

## 5. Train / Validation / Test Splits

### 5.1 Split Manifests (data_split/)

The dataset is split into train / validation / test sets using file-aware proportional sampling to preserve the original distribution of QA sources.

Files:
- train.jsonl
- valid.jsonl
- test.jsonl

Each line in a split file is a manifest entry, not the QA content itself.

Example:

```
{
  "id": "Q0086",
  "qnum": 86,
  "group": "group2",
  "path": "raw_data/Q0086.json"
}
```

Field description:
- id: QA identifier
- qnum: numeric QA index
- group: original source group (derived from original Excel files)
- path: relative path to the QA JSON file

---

### 5.2 Loading Example (Python)

```
import json, pathlib

root = pathlib.Path("Clinically_Curated_OC_Dataset")
manifest = root / "data_split" / "train.jsonl"

for line in manifest.read_text(encoding="utf-8").splitlines():
    rec = json.loads(line)
    qa = json.loads((root / rec["path"]).read_text(encoding="utf-8"))
    print(qa["text_canonical"], qa["focusp"])
```

---

## 6. Facet Schema and Clarification Prompts

### 6.1 Facet Schema (schema/facet_schema.json)

Defines the clinically grounded facet space used for annotation and clarification control, including:
- booleans: care-related and psychosocial indicators
- focusp: FOCUSP psychosocial support domains
- treatment_phase: treatment trajectory stages
- functional_impact: functional and symptom burdens
- other_condition / other_condition_text: optional contextual factors

This schema serves two purposes:
1. A consistent annotation framework for the QA dataset
2.	The action space for structured clarification in dialogue control

---

### 6.2 Clarification Prompts (schema/clarification_prompts.json)

Maps each facet value to a clinician-authored natural-language follow-up question used during clarification.

These prompts are designed to:
- Be short, patient-friendly, and non-threatening
- Reflect real postoperative OC clinical follow-up practice
- Reduce ambiguity before retrieval and response generation

The repository also includes `export_prompts_and_check.py`, a utility script for exporting the prompt specification to JSON and verifying label coverage against the released dataset.

--- 

## 7. Prompt Specifications (Dialogue Controller)

### 7.1 Information-Seeking Mode

Files:
- prompts/generation_system_prompt.txt (Chinese)
- prompts/generation_system_prompt_en.txt (English reference)

Defines system behavior when no psychological safety risk is detected:
- Evidence-grounded responses using retrieved QA only
- Explicit clinical safety boundaries
- No personalized medical advice

---

### 7.2 Protective Mode (Safety-Critical)

Files:
- prompts/protective_mode_prompt_template.txt
- prompts/protective_mode_prompt_template_en.txt

Defines system behavior when extreme emotional distress or suicidal ideation is detected:
- Emotional validation and psychological support
- Suppression of clarification and retrieval
- Strict prohibition of self-harm or suicide method descriptions

See prompts/prompts_readme.md for detailed design rationale.

---

## 8. Clinically Concerning Utterance Cue Lexicons

Located in safety_lexicon/:
- extreme_negative_cues.txt: cues for extreme emotional distress
- suicidal_cues.txt: cues for suicidal ideation
- cue_lexicon_readme.md: usage notes and limitations

These lexicons support keyword-based and embedding-based semantic detection and are intended for safety-aware dialogue routing—not diagnosis.

---
## 9. Reference Catalog

refs/refs_catalog.csv provides a mapping from REFxxxx identifiers to source URLs or textual references used to construct QA answers.

---

## 10. Ethics, Intended Use, and Restrictions

### 10.1 Data Privacy and De-identification
All data in this repository have been carefully curated and de-identified. No personally identifiable information (PII) is included.

### 10.2 Intended Use
This dataset is intended for:
- Academic research
- Method development for safety-aware dialogue systems
- Evaluation of clinically informed language models

### 10.3 Not Intended For
This dataset is **not intended for**:
- Direct clinical decision-making
- Medical diagnosis or treatment recommendations
- Deployment in real-world patient-facing systems without professional oversight

### 10.4 Safety Notice
Although the dataset is clinically curated, it does not cover all possible medical scenarios and should not be considered a substitute for professional medical advice.

### 10.5 Usage Restrictions
- Non-commercial use only (CC BY-NC 4.0)
- Users must comply with applicable regulations and institutional policies (e.g., IRB requirements)
- Redistribution of modified versions should clearly indicate changes

### 10.6 Responsibility
The authors are not responsible for any misuse of the dataset or for decisions made based on models trained using this data.

---

## 11. Citation

If you use this dataset or accompanying resources, please cite the following paper.

### 11.1 BibTeX

```bibtex
@inproceedings{liu2026safetyaware,
  title={Safety-Aware Dialogue for Postoperative Oral Cancer Care with Structured Clarification and a Clinically Curated Dataset},
  author={Liu, Tzu-Chi and Yang, Hui-Ying and Shun, Shiow-Ching and Chen, Yu-Chi and Chen, Lu-Yen Anny and Chen, Yong-Sheng},
  booktitle={The 64th Annual Meeting of the Association for Computational Linguistics},
  year={2026}
}
```

### 11.2 CFF Metadata

This repository also provides a CITATION.cff file for GitHub-based citation metadata.

```yaml
cff-version: 1.2.0
title: "Clinically Curated Postoperative Oral Cancer Dialogue Dataset"
message: "If you use this dataset or its accompanying resources, please cite our ACL 2026 paper."
type: dataset

authors:
  - family-names: "Liu"
    given-names: "Tzu-Chi"
  - family-names: "Yang"
    given-names: "Hui-Ying"
  - family-names: "Shun"
    given-names: "Shiow-Ching"
  - family-names: "Chen"
    given-names: "Yu-Chi"
  - family-names: "Chen"
    given-names: "Lu-Yen Anny"
  - family-names: "Chen"
    given-names: "Yong-Sheng"

year: 2026

preferred-citation:
  type: paper
  title: "Safety-Aware Dialogue for Postoperative Oral Cancer Care with Structured Clarification and a Clinically Curated Dataset"
  authors:
    - family-names: "Liu"
      given-names: "Tzu-Chi"
    - family-names: "Yang"
      given-names: "Hui-Ying"
    - family-names: "Shun"
      given-names: "Shiow-Ching"
    - family-names: "Chen"
      given-names: "Yu-Chi"
    - family-names: "Chen"
      given-names: "Lu-Yen Anny"
    - family-names: "Chen"
      given-names: "Yong-Sheng"
  year: 2026
  conference:
    name: "Annual Meeting of the Association for Computational Linguistics"
```

---

## 12. License

This dataset is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

The dataset is intended for **non-commercial research and educational use only**.