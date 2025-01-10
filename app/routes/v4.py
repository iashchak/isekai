from fastapi import APIRouter
from fastapi.security import HTTPBasic
import pandas as pd
import os
import random
from typing import Dict, List, Optional, Set

security = HTTPBasic()

DATAPATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "v4")

stage_templates_df = pd.read_json(os.path.join(DATAPATH, "stage_templates.jsonl"), lines=True)
variables_df = pd.read_json(os.path.join(DATAPATH, "variables.jsonl"), lines=True)

router = APIRouter()

class StoryState:
    def __init__(self) -> None:
        self.variables: Dict[str, str] = {}
        self.flags: Set[str] = set()

    def add_flags(self, flags: List[str]) -> None:
        for flag in flags:
            self.flags.add(flag)

def pick_template(stage: str, story_state: StoryState) -> Optional[Dict[str, object]]:
    # possible_templates = [t for t in stage_templates_df if t['stage'] == stage]
    possible_templates = stage_templates_df[stage_templates_df["stage"] == stage].to_dict(orient="records")
    valid_templates = [
        t for t in possible_templates if all(req in story_state.flags for req in t["requires"])
    ]
    if not valid_templates:
        return None
    return random.choice(valid_templates)

def apply_template(template: Dict[str, object], story_state: StoryState) -> str:
    story_state.add_flags(template.get("ensures", []))
    return template["text"].format(**story_state.variables)

@router.get(
    "/generate_story",
    description="Generates a random story with stages.",
)
async def generate_story():
    story_stages = [
        "ordinary_world",
        "call_to_adventure",
        "refusal_of_call",
        "meeting_the_mentor",
        "crossing_first_threshold",
        "tests_allies_enemies",
        "approach_inmost_cave",
        "ordeal",
        "reward",
        "road_back",
        "resurrection",
        "return_with_elixir",
    ]

    story_state = StoryState()

    # df to dict
    story_state.variables = variables_df.set_index("name").to_dict()["value"]
    steps: List[Dict[str, str]] = []

    for stage in story_stages:
        template = pick_template(stage, story_state)
        if template is None:
            steps.append({"step": stage, "value": "No suitable scenario found for this stage."})
            continue
        final_text = apply_template(template, story_state)
        steps.append({"step": stage, "value": final_text})

    return {step["step"]: step["value"] for step in steps}

if __name__ == "__main__":
    import asyncio
    
    if __name__ == "__main__":
        result = asyncio.run(generate_story())
        print(result)