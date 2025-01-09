from enum import Enum
from transitions import Machine
import random
from faker import Faker

class MonomythSteps(Enum):
    CALL_TO_ADVENTURE = "Call to Adventure"
    REFUSAL_OF_THE_CALL = "Refusal of the Call"
    SUPERNATURAL_AID = "Supernatural Aid"
    CROSSING_THE_FIRST_THRESHOLD = "Crossing the First Threshold"
    BELLY_OF_THE_WHALE = "Belly of the Whale"
    ROAD_OF_TRIALS = "Road of Trials"
    MEETING_WITH_THE_GODDESS = "Meeting with the Goddess"
    WOMAN_AS_TEMPTRESS = "Woman as Temptress"
    ATONEMENT_WITH_THE_FATHER = "Atonement with the Father"
    APOTHEOSIS = "Apotheosis"
    THE_ULTIMATE_BOON = "The Ultimate Boon"
    REFUSAL_OF_THE_RETURN = "Refusal of the Return"
    THE_MAGIC_FLIGHT = "The Magic Flight"
    RESCUE_FROM_WITHOUT = "Rescue from Without"
    THE_CROSSING_OF_THE_RETURN_THRESHOLD = "The Crossing of the Return Threshold"
    MASTER_OF_TWO_WORLDS = "Master of Two Worlds"
    FREEDOM_TO_LIVE = "Freedom to Live"

class StoryGenerator(Machine):
    _transitions = [
        {"trigger": "proceed", "source": MonomythSteps.CALL_TO_ADVENTURE, "dest": MonomythSteps.REFUSAL_OF_THE_CALL},
        {"trigger": "proceed", "source": MonomythSteps.REFUSAL_OF_THE_CALL, "dest": MonomythSteps.SUPERNATURAL_AID},
        {"trigger": "proceed", "source": MonomythSteps.SUPERNATURAL_AID, "dest": MonomythSteps.CROSSING_THE_FIRST_THRESHOLD},
        {"trigger": "proceed", "source": MonomythSteps.CROSSING_THE_FIRST_THRESHOLD, "dest": MonomythSteps.BELLY_OF_THE_WHALE},
        {"trigger": "proceed", "source": MonomythSteps.BELLY_OF_THE_WHALE, "dest": MonomythSteps.ROAD_OF_TRIALS},
        {"trigger": "proceed", "source": MonomythSteps.ROAD_OF_TRIALS, "dest": MonomythSteps.MEETING_WITH_THE_GODDESS},
        {"trigger": "proceed", "source": MonomythSteps.MEETING_WITH_THE_GODDESS, "dest": MonomythSteps.WOMAN_AS_TEMPTRESS},
        {"trigger": "proceed", "source": MonomythSteps.WOMAN_AS_TEMPTRESS, "dest": MonomythSteps.ATONEMENT_WITH_THE_FATHER},
        {"trigger": "proceed", "source": MonomythSteps.ATONEMENT_WITH_THE_FATHER, "dest": MonomythSteps.APOTHEOSIS},
        {"trigger": "proceed", "source": MonomythSteps.APOTHEOSIS, "dest": MonomythSteps.THE_ULTIMATE_BOON},
        {"trigger": "proceed", "source": MonomythSteps.THE_ULTIMATE_BOON, "dest": MonomythSteps.REFUSAL_OF_THE_RETURN},
        {"trigger": "proceed", "source": MonomythSteps.REFUSAL_OF_THE_RETURN, "dest": MonomythSteps.THE_MAGIC_FLIGHT},
        {"trigger": "proceed", "source": MonomythSteps.THE_MAGIC_FLIGHT, "dest": MonomythSteps.RESCUE_FROM_WITHOUT},
        {"trigger": "proceed", "source": MonomythSteps.RESCUE_FROM_WITHOUT, "dest": MonomythSteps.THE_CROSSING_OF_THE_RETURN_THRESHOLD},
        {"trigger": "proceed", "source": MonomythSteps.THE_CROSSING_OF_THE_RETURN_THRESHOLD, "dest": MonomythSteps.MASTER_OF_TWO_WORLDS},
        {"trigger": "proceed", "source": MonomythSteps.MASTER_OF_TWO_WORLDS, "dest": MonomythSteps.FREEDOM_TO_LIVE},
    ]

    def __init__(self):
        self.fake = Faker()
        self.story_steps = {step: None for step in MonomythSteps}
        super().__init__(
            states=MonomythSteps,
            transitions=self._transitions,
            initial=MonomythSteps.CALL_TO_ADVENTURE,
            send_event=True,
            auto_transitions=False,
            after_state_change='auto_proceed',
        )

    def auto_proceed(self, event=None):
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def reset_machine(self):
        self.set_state(MonomythSteps.CALL_TO_ADVENTURE)
        self.auto_proceed()

    def generate_story(self):
        self.reset_machine()
        for step in MonomythSteps:
            self.story_steps[step] = self.fake.sentence()
        return {step.value: self.story_steps[step] for step in MonomythSteps}
