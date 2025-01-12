from fastapi import APIRouter
import pandas as pd
import os
from dataclasses import dataclass
import logging
logger = logging.getLogger("uvicorn.error")

DATAPATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "..",
    "data",
    "v5"
)


@dataclass
class Story:
    stage: str
    text: str
    requires: list[str]
    ensures: list[str]
    story_id: int


stories_df = pd.read_json(
    os.path.join(
        DATAPATH,
        "stories.json"
    ),
    orient="records"
)



def get_first_story() -> Story:
    first_story = stories_df[stories_df["stage"] == "ordinary_world"].sample(1).iloc[0].to_dict()
    return Story(**first_story)


def get_story_by_stage_and_available_options(
    options: list[str],
    used_stages: list[str]
) -> Story:
    """Find a story where each of `require` values are in `options`"""
    # get all the stories where the `requires` are in the options
    stories = stories_df[
        stories_df["requires"].apply(
            lambda x: all(r in options for r in x)
        )
    ]

    unused_stories = stories[~stories["stage"].isin(used_stages)]
    random_story = unused_stories.sample(1).iloc[0].to_dict()

    return Story(**random_story)


router = APIRouter()


@router.get(
    "/generate",
    description="Generates a random isekai scenario based on predefined stories.",
)
async def generate_story() -> dict:
    stages: list[Story] = [get_first_story()]
    options = stages[0].ensures
    try:
        while 'story_complete' not in options:
            current_stages = [str(s.stage) for s in stages]
            # the first row in df
            stage = get_story_by_stage_and_available_options(
                options,
                current_stages
            )
            stages.append(stage)
            options += stage.ensures
        number_of_different_story_ids = len(
            set([s.story_id for s in stages])
        )
        logger.info(msg=f"Number of different story ids: {number_of_different_story_ids}")

        return {stage.stage: stage.text for stage in stages}
    except Exception as e:
        logger.error(msg=f"""
            Error: {e}
            stages: {stages}
            options: {options}
        """)
        return {"error": "An error occurred"}

