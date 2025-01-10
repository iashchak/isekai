from fastapi import APIRouter
import pandas as pd
import os
from typing import List

DATAPATH = os.path.join(os.path.dirname(__file__), "..",
                        "..", "..", "..", "data", "v5")

stories_df = pd.read_json(os.path.join(
    DATAPATH, "stories.json"),  orient="records")

router = APIRouter()


def get_first_story():
    return stories_df[stories_df["stage"] == "ordinary_world"].sample(1).iloc[0].to_dict()


def get_story_by_stage_and_available_options(options: List[str], used_stages: List[str]):
    """
        Finds a stages where each of `require` values are in `options`
    """
    # get all the stories where the `requires` are in the options
    stories = stories_df[stories_df["requires"].apply(
        lambda x: all(r in options for r in x))]
    # get the stories that have not been used
    stories = stories[~stories["stage"].isin(used_stages)]
    # get a random story
    return stories.sample(1).iloc[0].to_dict()


@router.get(
    "/generate",
    description="Generates a random isekai scenario based on predefined stories.",
)
async def generate_story():
    stages = [get_first_story()]
    options = stages[0]["ensures"]
    try:
        while 'story_complete' not in options:
            # the first row in df
            stage = get_story_by_stage_and_available_options(
                options, [s["stage"] for s in stages])
            stages.append(stage)
            options = options + stage["ensures"]
        number_of_different_story_ids = len(set([s["story_id"] for s in stages]))
        print(f"Number of different story ids: {number_of_different_story_ids}")

        return {stage["stage"]: stage["text"] for stage in stages}
    except Exception as e:
        print(f"""
            Error: {e}
            stages: {stages}
            options: {options}
        """)
        return {"error": "An error occurred"}


if __name__ == "__main__":
    from asyncio import run
    print(run(generate_story()))
