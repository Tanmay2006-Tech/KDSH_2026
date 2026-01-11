"""

KHARAGPUR DATA SCIENCE HACKATHON
Track A: Systems Reasoning with NLP and Generative AI

"""

import os
import csv
import argparse
import pathway as pw
import pandas as pd

# File Discovery

def find_test_csv():
    for p in [
        "test.csv",
        "Dataset/test.csv",
        "Data/test.csv",
        "data/test.csv",
        "/content/test.csv",
        "/mnt/data/test.csv",
    ]:
        if os.path.exists(p):
            return p
    raise RuntimeError("test.csv not found")
def find_novel_dir():
    for d in [
        "novels",
        "Books",
        "Dataset/Books",
        "Data/novels",
        "/content/novels",
        "/mnt/data/novels",
        "/mnt/data/Books",
    ]:
        if os.path.isdir(d):
            return d
    return None
def invariant_reasoning(backstory, narrative):
    back = str(backstory).lower() if backstory else ""
    text = str(narrative).lower() if narrative else ""

    # Life / Death
    if any(w in back for w in ["died", "dead", "executed"]) and \
       any(w in text for w in ["alive", "survived", "escaped", "lived"]):
        return 0, (
            "Causal Paradox Detected: Death established in the hypothesized past "
            "precludes the continued active behavior observed in the narrative."
        )

    # Legal Constraint
    if "arrested" in back and "escaped" in text:
        return 0, (
            "Causal Paradox Detected: Imprisonment established in the backstory "
            "is violated by an unresolved escape in the narrative."
        )

    # Commitment / Refusal
    if any(w in back for w in ["vowed", "promised", "refused", "would never"]) and \
       any(w in text for w in ["agreed", "accepted", "joined", "complied"]):
        return 0, (
            "Causal Paradox Detected: A binding commitment in the hypothesized past "
            "is violated by subsequent voluntary action."
        )

    return None

# SOFT TRAIT CHECKS (NON-OVERRIDING)

TRAIT_RULES = {
    "non-violent": (["pacifist", "non-violent"], ["murdered", "killed"]),
    "impoverished": (["poor", "destitute"], ["gold", "fortune", "luxury"]),
    "solitary": (["hermit", "orphan"], ["family", "parents", "wedding"]),
}

def soft_trait_check(backstory, narrative):
    back = str(backstory).lower()
    text = str(narrative).lower()
    for trait, (signals, violations) in TRAIT_RULES.items():
        if any(s in back for s in signals) and any(v in text for v in violations):
            return (
                1,  
                f"Potential Tension Detected: Backstory suggests '{trait}', "
                f"but narrative includes '{v}'. This is treated as non-fatal."
            )
    return None

# PIPELINE

def run_pipeline(test_csv, output_csv):
    schema = pw.schema_from_csv(test_csv)
    pw.io.csv.read(test_csv, schema=schema, mode="static")
    novel_dir = find_novel_dir()
    if novel_dir:
        pw.io.fs.read(novel_dir, format="plaintext")
    pw.run()
    df = pd.read_csv(test_csv, dtype=str)
    story_id_col = next(c for c in df.columns if "id" in c.lower())
    backstory_col = next(c for c in df.columns if "caption" in c.lower() or "backstory" in c.lower())
    narrative_col = next(c for c in df.columns if c.lower() in ("content", "story", "narrative"))
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Story ID", "Prediction", "Rationale"])
        for _, row in df.iterrows():
            result = invariant_reasoning(row[backstory_col], row[narrative_col])
            if result:
                pred, rationale = result
            else:
                soft = soft_trait_check(row[backstory_col], row[narrative_col])
                if soft:
                    pred, rationale = soft
                else:
                    pred = 1
                    rationale = (
                        "No Irreversible State Violation Detected: "
                        "Narrative remains causally compatible with the backstory."
                    )
            writer.writerow([row[story_id_col], pred, rationale])

# ENTRY

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--test-csv", type=str)
    parser.add_argument("--output", default="results.csv")
    args, _ = parser.parse_known_args()
    test_csv = args.test_csv or find_test_csv()
    if os.path.exists(args.output):
        os.remove(args.output)
    run_pipeline(test_csv, args.output)
    print("results.csv generated successfully.")
if __name__ == "__main__":
    main()
