# Prompt Specifications for Safety-Aware Clinical Dialogue

This folder contains the system-level prompt specifications used in our
safety-aware dialogue framework for postoperative oral cancer care.

These prompts are part of the dialogue controller design and are released
to support reproducibility and transparent evaluation.

## Files

### generation_system_prompt.txt
Defines the behavior of the system in the normal information-seeking state.
The prompt enforces:
- Evidence-grounded responses using retrieved QA entries only
- Patient-friendly educational tone
- Explicit clinical safety boundaries
- Avoidance of personalized medical advice

### protective_mode_prompt_template.txt
Defines the behavior of the system when psychologically concerning language
(e.g., extreme emotional distress or suicidal ideation) is detected.
This mode suppresses clarification and retrieval and restricts responses to:
- Emotional support and validation
- Encouragement of professional help
- Strict avoidance of self-harm method descriptions

The template includes placeholders for dynamically injected user messages
and detected danger cues.

## Design Principles
- Prompts are intentionally conservative and safety-first.
- They are not intended for diagnosis or clinical decision-making.
- All responses are informational or supportive in nature.
- Prompt behavior aligns with the ethical and clinical constraints
  described in the accompanying paper.

## Notes
These prompts are provided for research and replication purposes.
Deployments in real clinical environments should be reviewed and adapted
in accordance with local regulations and institutional policies.