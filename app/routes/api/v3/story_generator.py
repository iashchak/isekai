from enum import Enum
from transitions import Machine
import random
from faker import Faker
import numpy as np
import pandas as pd
import os

class MonomythSteps(Enum):
    INITIAL = "INITIAL"
    CALL_TO_ADVENTURE = "CALL_TO_ADVENTURE"
    REFUSAL_OF_THE_CALL = "REFUSAL_OF_THE_CALL"
    SUPERNATURAL_AID = "SUPERNATURAL_AID"
    CROSSING_THE_FIRST_THRESHOLD = "CROSSING_THE_FIRST_THRESHOLD"
    BELLY_OF_THE_WHALE = "BELLY_OF_THE_WHALE"
    ROAD_OF_TRIALS = "ROAD_OF_TRIALS"
    MEETING_WITH_THE_GODDESS = "MEETING_WITH_THE_GODDESS"
    WOMAN_AS_TEMPTRESS = "WOMAN_AS_TEMPTRESS"
    ATONEMENT_WITH_THE_FATHER = "ATONEMENT_WITH_THE_FATHER"
    APOTHEOSIS = "APOTHEOSIS"
    THE_ULTIMATE_BOON = "THE_ULTIMATE_BOON"
    REFUSAL_OF_THE_RETURN = "REFUSAL_OF_THE_RETURN"
    THE_MAGIC_FLIGHT = "THE_MAGIC_FLIGHT"
    RESCUE_FROM_WITHOUT = "RESCUE_FROM_WITHOUT"
    THE_CROSSING_OF_THE_RETURN_THRESHOLD = "THE_CROSSING_OF_THE_RETURN_THRESHOLD"
    MASTER_OF_TWO_WORLDS = "MASTER_OF_TWO_WORLDS"
    FREEDOM_TO_LIVE = "FREEDOM_TO_LIVE"

DATAPATH = os.path.join(os.path.dirname(__file__),
                        "..", "..", "..", "..","data", "v3")

# Read CSV files into a dictionary of DataFrames: attributes["skill"], etc.
attributes = {
    os.path.splitext(f)[0]: pd.read_csv(os.path.join(DATAPATH, f))
    for f in os.listdir(DATAPATH)
    if f.endswith(".csv")
}


class StoryGenerator(Machine):
    _transitions = [
        {
            "trigger": "proceed",
            "source": MonomythSteps.INITIAL,
            "dest": MonomythSteps.CALL_TO_ADVENTURE,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.CALL_TO_ADVENTURE,
            "dest": MonomythSteps.REFUSAL_OF_THE_CALL,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.REFUSAL_OF_THE_CALL,
            "dest": MonomythSteps.SUPERNATURAL_AID,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.SUPERNATURAL_AID,
            "dest": MonomythSteps.CROSSING_THE_FIRST_THRESHOLD,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.CROSSING_THE_FIRST_THRESHOLD,
            "dest": MonomythSteps.BELLY_OF_THE_WHALE,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.BELLY_OF_THE_WHALE,
            "dest": MonomythSteps.ROAD_OF_TRIALS,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.ROAD_OF_TRIALS,
            "dest": MonomythSteps.MEETING_WITH_THE_GODDESS,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.MEETING_WITH_THE_GODDESS,
            "dest": MonomythSteps.WOMAN_AS_TEMPTRESS,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.WOMAN_AS_TEMPTRESS,
            "dest": MonomythSteps.ATONEMENT_WITH_THE_FATHER,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.ATONEMENT_WITH_THE_FATHER,
            "dest": MonomythSteps.APOTHEOSIS,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.APOTHEOSIS,
            "dest": MonomythSteps.THE_ULTIMATE_BOON,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.THE_ULTIMATE_BOON,
            "dest": MonomythSteps.REFUSAL_OF_THE_RETURN,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.REFUSAL_OF_THE_RETURN,
            "dest": MonomythSteps.THE_MAGIC_FLIGHT,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.THE_MAGIC_FLIGHT,
            "dest": MonomythSteps.RESCUE_FROM_WITHOUT,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.RESCUE_FROM_WITHOUT,
            "dest": MonomythSteps.THE_CROSSING_OF_THE_RETURN_THRESHOLD,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.THE_CROSSING_OF_THE_RETURN_THRESHOLD,
            "dest": MonomythSteps.MASTER_OF_TWO_WORLDS,
        },
        {
            "trigger": "proceed",
            "source": MonomythSteps.MASTER_OF_TWO_WORLDS,
            "dest": MonomythSteps.FREEDOM_TO_LIVE,
        },
    ]

    def __init__(self):
        self.fake = Faker()
        self.random_seed = None
        self.adventure_cause = None
        self.refusal_cause = None
        self.aid = None
        self.threshold = None
        self.whale = None
        self.trials = None
        self.goddess = None
        self.temptress = None
        self.atonement = None
        self.apotheosis = None
        self.boon = None
        self.refusal_return = None
        self.magic_flight = None
        self.rescue = None
        self.return_threshold = None
        self.master = None
        self.freedom = None

        super().__init__(
            states=MonomythSteps,
            transitions=self._transitions,
            initial=MonomythSteps.INITIAL,
            send_event=True,
            auto_transitions=False,
            after_state_change="auto_proceed",
        )

    def set_random_seed(self, random_seed: int = None):
        self.random_seed = random_seed
        # Seed the global RNGs only once (if needed).
        if self.random_seed is not None:
            random.seed(self.random_seed)
            Faker.seed(self.random_seed)
            np.random.seed(self.random_seed)

    def auto_proceed(self, event=None):
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def reset_machine(self):
        self.set_state(MonomythSteps.INITIAL)
        self.auto_proceed()

    def sample_csv_column_string(self, key: str) -> str:
        """
        Generic method to pick a single random item from a CSV column.
        key should match both the DataFrame key and the column name inside that DataFrame.
        """
        return attributes[key][key].sample(1).values[0]

    def on_enter_CALL_TO_ADVENTURE(self, event):
        self.adventure_cause = self.sample_csv_column_string("adventure_cause")

    def on_enter_REFUSAL_OF_THE_CALL(self, event):
        self.refusal_cause = self.sample_csv_column_string("refusal_cause")

    def on_enter_SUPERNATURAL_AID(self, event):
        self.aid = self.sample_csv_column_string("aid")

    def on_enter_CROSSING_THE_FIRST_THRESHOLD(self, event):
        self.threshold = self.sample_csv_column_string("threshold")

    def on_enter_BELLY_OF_THE_WHALE(self, event):
        self.whale = self.sample_csv_column_string("whale")

    def on_enter_ROAD_OF_TRIALS(self, event):
        self.trials = self.sample_csv_column_string("trials")

    def on_enter_MEETING_WITH_THE_GODDESS(self, event):
        self.goddess = self.sample_csv_column_string("goddess")

    def on_enter_WOMAN_AS_TEMPTRESS(self, event):
        self.temptress = self.sample_csv_column_string("temptress")

    def on_enter_ATONEMENT_WITH_THE_FATHER(self, event):
        self.atonement = self.sample_csv_column_string("atonement")

    def on_enter_APOTHEOSIS(self, event):
        self.apotheosis = self.sample_csv_column_string("apotheosis")

    def on_enter_THE_ULTIMATE_BOON(self, event):
        self.boon = self.sample_csv_column_string("boon")

    def on_enter_REFUSAL_OF_THE_RETURN(self, event):
        self.refusal_return = self.sample_csv_column_string("refusal_return")

    def on_enter_THE_MAGIC_FLIGHT(self, event):
        self.magic_flight = self.sample_csv_column_string("magic_flight")

    def on_enter_RESCUE_FROM_WITHOUT(self, event):
        self.rescue = self.sample_csv_column_string("rescue")

    def on_enter_THE_CROSSING_OF_THE_RETURN_THRESHOLD(self, event):
        self.return_threshold = self.sample_csv_column_string("return_threshold")

    def on_enter_MASTER_OF_TWO_WORLDS(self, event):
        self.master = self.sample_csv_column_string("master")

    def on_enter_FREEDOM_TO_LIVE(self, event):
        self.freedom = self.sample_csv_column_string("freedom")

    def generate_story(self):
        self.reset_machine()

        story = {
            "adventure_cause": self.adventure_cause,
            "refusal_cause": self.refusal_cause,
            "aid": self.aid,
            "threshold": self.threshold,
            "whale": self.whale,
            "trials": self.trials,
            "goddess": self.goddess,
            "temptress": self.temptress,
            "atonement": self.atonement,
            "apotheosis": self.apotheosis,
            "boon": self.boon,
            "refusal_return": self.refusal_return,
            "magic_flight": self.magic_flight,
            "rescue": self.rescue,
            "return_threshold": self.return_threshold,
            "master": self.master,
            "freedom": self.freedom,
        }

        if self.random_seed is not None:
            story["random_seed"] = self.random_seed

        return story


story_generator = StoryGenerator()
story_generator.set_random_seed(42)
story_data = story_generator.generate_story()
print(story_data)
