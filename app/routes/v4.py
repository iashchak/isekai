from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.utils.helpers import verify_credentials
import pandas as pd
import os
import random
from typing import Dict, List, Optional, Set
from faker import Faker

security = HTTPBasic()

DATAPATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "v4")

stage_templates_df = pd.read_csv(os.path.join(DATAPATH, "stage_templates.csv"), quotechar='"')
variables_df = pd.read_csv(os.path.join(DATAPATH, "variables.csv"), quotechar='"')

router = APIRouter()

class StoryState:
    def __init__(self) -> None:
        self.variables: Dict[str, str] = {}
        self.flags: Set[str] = set()

    def add_flags(self, flags: List[str]) -> None:
        for flag in flags:
            self.flags.add(flag)

def pick_template(stage: str, story_state: StoryState) -> Optional[Dict[str, object]]:
    possible_templates = stage_templates_df[stage_templates_df['stage'] == stage].to_dict('records')
    valid_templates = [
        t for t in possible_templates if all(req in story_state.flags for req in eval(t["requires"]))
    ]
    if not valid_templates:
        return None
    return random.choice(valid_templates)

def apply_template(template: Dict[str, object], story_state: StoryState) -> str:
    story_state.add_flags(eval(template.get("ensures", "[]")))
    return template["text"].format(**story_state.variables)

def generate_variables() -> Dict[str, str]:
    fake = Faker("ja-JP")
    variables = {
        "place": fake.city(),
        "isekai_origin": fake.city(),
        "isekai_world": fake.word(),
        "mentor": fake.name(),
        "enemy": fake.name(),
        "world": fake.word(),
    }
    if random.random() < 0.5:
        variables["magic_ability"] = fake.word() + " magic"
    else:
        variables["magic_ability"] = fake.word() + " skill"
    return variables

@router.get(
    "/generate_story",
    description="Generates a random story with stages.",
)
async def generate_story(credentials: HTTPBasicCredentials = Depends(security)):
    verify_credentials(credentials)
    
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
    story_state.variables = generate_variables()

    chosen_texts: List[str] = []

    for stage in story_stages:
        template = pick_template(stage, story_state)
        if template is None:
            chosen_texts.append(f"[Stage: {stage}]\nNo suitable scenario found for this stage.\n")
            continue
        final_text = apply_template(template, story_state)
        chosen_texts.append(f"[Stage: {stage}]\n{final_text}\n")

    return chosen_texts
