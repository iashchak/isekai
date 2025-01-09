from enum import Enum
from transitions import Machine
import random

import pandas as pd
import os
from faker import Faker
import numpy as np

DATAPATH = os.path.join(os.path.dirname(__file__),
                        "..", "..", "..", "data", "v2")

# Read CSV files into a dictionary of DataFrames: attributes["skill"], etc.
attributes = {
    os.path.splitext(f)[0]: pd.read_csv(os.path.join(DATAPATH, f))
    for f in os.listdir(DATAPATH)
    if f.endswith(".csv")
}


def biased_sample_series(data: pd.Series, base: float = 0.5, cutoff: int = None) -> pd.Series:
    """
    Returns a random subset of the Series, size chosen by a geometric-like distribution.
    base ~ probability factor, cutoff ~ max elements to choose.
    """
    if cutoff is None or cutoff > len(data):
        cutoff = len(data)

    # Generate probabilities for counts from 1..cutoff
    probabilities = np.array([base**i for i in range(1, cutoff + 1)])
    probabilities /= probabilities.sum()

    # Choose how many items to pick
    count = np.random.choice(range(1, cutoff + 1), p=probabilities)

    # Shuffle data; random_state=None uses the global numpy RNG
    sampled_data = data.sample(frac=1, random_state=None)
    return sampled_data.head(count)


class HeroGenerationSteps(Enum):
    INITIAL = "INITIAL"
    GENDER = "GENDER"
    FEMALE_NAME = "FEMALE_NAME"
    MALE_NAME = "MALE_NAME"
    OCCUPATION = "OCCUPATION"
    TIMEKILLER = "TIMEKILLER"
    HAREM_WITH_GIRLS = "HAREM_WITH_GIRLS"
    HAREM_WITH_BOYS = "HAREM_WITH_BOYS"
    DEVINE_BLESSING = "DEVINE_BLESSING"
    SKILL = "SKILL"
    UNIQUE_ITEM = "UNIQUE_ITEM"
    WEAKNESS = "WEAKNESS"


class HeroGenerator(Machine):
    _transitions = [
        # Step by step transitions
        {"trigger": "proceed", "source": HeroGenerationSteps.INITIAL, "dest": HeroGenerationSteps.GENDER},
        {"trigger": "proceed", "source": HeroGenerationSteps.GENDER, "dest": HeroGenerationSteps.MALE_NAME, "conditions": "is_male"},
        {"trigger": "proceed", "source": HeroGenerationSteps.GENDER, "dest": HeroGenerationSteps.FEMALE_NAME, "unless": "is_male"},
        {"trigger": "proceed", "source": HeroGenerationSteps.MALE_NAME, "dest": HeroGenerationSteps.OCCUPATION},
        {"trigger": "proceed", "source": HeroGenerationSteps.FEMALE_NAME, "dest": HeroGenerationSteps.OCCUPATION},
        {"trigger": "proceed", "source": HeroGenerationSteps.OCCUPATION, "dest": HeroGenerationSteps.DEVINE_BLESSING},
        {"trigger": "proceed", "source": HeroGenerationSteps.DEVINE_BLESSING, "dest": HeroGenerationSteps.SKILL},
        {"trigger": "proceed", "source": HeroGenerationSteps.SKILL, "dest": HeroGenerationSteps.UNIQUE_ITEM},
        {"trigger": "proceed", "source": HeroGenerationSteps.UNIQUE_ITEM, "dest": HeroGenerationSteps.WEAKNESS},
        {"trigger": "proceed", "source": HeroGenerationSteps.WEAKNESS, "dest": HeroGenerationSteps.TIMEKILLER},
        {"trigger": "proceed", "source": HeroGenerationSteps.TIMEKILLER, "dest": HeroGenerationSteps.HAREM_WITH_GIRLS, "conditions": "is_male"},
        {"trigger": "proceed", "source": HeroGenerationSteps.TIMEKILLER, "dest": HeroGenerationSteps.HAREM_WITH_BOYS, "unless": "is_male"},
    ]

    def __init__(self):
        # Main hero attributes
        self.gender = None
        self.name = None
        self.occupation = None
        self.timekiller = None
        self.harem = None
        self.devine_blessing = None
        self.skill = None
        self.unique_item = None
        self.weakness = None

        self.fake = Faker("ja-JP")

        super().__init__(
            states=HeroGenerationSteps,
            transitions=self._transitions,
            initial=HeroGenerationSteps.INITIAL,
            send_event=True,
            auto_transitions=False,
            after_state_change='auto_proceed',  # Automatically call proceed if possible
        )

    def set_random_seed(self, random_seed: int = None):
        self.random_seed = random_seed
        # Seed the global RNGs only once (if needed).
        if self.random_seed is not None:
            random.seed(self.random_seed)
            Faker.seed(self.random_seed)
            np.random.seed(self.random_seed)

    def auto_proceed(self, event = None):
        """
        Called after each transition. If the machine can go further, do it automatically.
        """
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    @property
    def is_male(self):
        return self.gender == "M"

    def sample_csv_column_strings(self, key: str, base: float = 0.5) -> list[str]:
        """
        Generic method to pick random items from a CSV column using biased_sample_series.
        key should match both the DataFrame key and the column name inside that DataFrame.
        """
        # Example: attributes["skill"]["skill"]
        col = attributes[key][key]
        sampled = biased_sample_series(col, base=base)
        return [item.strip() for item in sampled.values]
    
    def sample_csv_column_string(self, key: str) -> str:
        """
        Generic method to pick a single random item from a CSV column.
        key should match both the DataFrame key and the column name inside that DataFrame.
        """
        return attributes[key][key].sample(1).values[0]

    def reset_machine(self):
        """
        Reset the state machine to the INITIAL step, without reseeding RNG.
        This way, multiple calls produce varied results.
        """
        self.set_state(HeroGenerationSteps.INITIAL)
        self.auto_proceed()

    # ----- on_enter_* Handlers -----
    def on_enter_GENDER(self, event):
        self.gender = random.choice(["M", "F"])

    def on_enter_MALE_NAME(self, event):
        self.name = self.fake.romanized_name_male()

    def on_enter_FEMALE_NAME(self, event):
        self.name = self.fake.romanized_name_female()

    def on_enter_OCCUPATION(self, event):
        self.occupation = self.sample_csv_column_string("occupation")

    def on_enter_DEVINE_BLESSING(self, event):
        # If your CSV file is named "devine_bleesing.csv", keep the old key:
        self.devine_blessing = self.sample_csv_column_strings("devine_bleesing")

    def on_enter_SKILL(self, event):
        self.skill = self.sample_csv_column_strings("skill")

    def on_enter_UNIQUE_ITEM(self, event):
        self.unique_item = self.sample_csv_column_strings("unique_item")

    def on_enter_WEAKNESS(self, event):
        self.weakness = self.sample_csv_column_strings("weakness")

    def on_enter_TIMEKILLER(self, event):
        self.timekiller = self.sample_csv_column_strings("timekiller")

    def on_enter_HAREM_WITH_GIRLS(self, event):
        # Example: pick between 0..10 female names
        self.harem = [self.fake.romanized_name_female() for _ in range(random.randint(0, 10))]

    def on_enter_HAREM_WITH_BOYS(self, event):
        # Example: pick between 0..10 male names
        self.harem = [self.fake.romanized_name_male() for _ in range(random.randint(0, 10))]

    def generate_hero(self):
        """
        Public method to trigger the entire hero generation process.
        Resets state to INITIAL, then transitions automatically through all steps.
        Returns a dictionary with the final attributes.
        """
        self.reset_machine()

        hero = {
            "gender": self.gender,
            "name": self.name,
            "occupation": self.occupation,
            "timekiller": self.timekiller,
            "harem": self.harem,
            "devine_blessing": self.devine_blessing,
            "skill": self.skill,
            "unique_item": self.unique_item,
            "weakness": self.weakness,
        }

        if self.random_seed is not None:
            hero["random_seed"] = self.random_seed

        return hero
