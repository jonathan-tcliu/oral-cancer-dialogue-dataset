# Clinically Concerning Utterance Cue Lexicons

This folder provides two cue lexicons used for safety-aware routing in postoperative oral-cancer dialogue.

## Files
- extreme_negative_cues.txt: cues for extreme emotional distress (non-suicidal crisis language)
- suicidal_cues.txt: cues for suicidal ideation / self-harm intent

## Intended use
These lexicons can be used in two ways:
1) Keyword matching: trigger if any cue appears in the user utterance.
2) Embedding similarity detection: embed the utterance and compute max cosine similarity against the cue set.
   Trigger if the max similarity exceeds a fixed threshold (Trigger thresholds are implementation-dependent and should be set by downstream users.).

## Notes and limitations
- These lexicons are not diagnostic tools and must not be used to infer clinical diagnoses.
- Short utterances are ambiguous; false positives/negatives are expected.
- The system should adopt conservative behavior: when safety-critical meaning is suspected, route to protective supportive mode.
- Do not use the lexicons to generate or suggest self-harm methods. Protective mode responses should avoid method details and encourage professional help.

## License and ethics
All cues were curated and reviewed by clinical experts. All text is de-identified prior to release.