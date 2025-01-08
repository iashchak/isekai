from enum import Enum
from transitions import Machine
import random

import pandas as pd
import os
from faker import Faker
import numpy as np

from app.utils.helpers import select_random_item

DATAPATH = os.path.join(os.path.dirname(__file__),
                        "..", "..", "..", "data", "v2")

attributes = {
    os.path.splitext(f)[0]: pd.read_csv(os.path.join(DATAPATH, f))
    for f in os.listdir(DATAPATH)
    if f.endswith(".csv")
}


def biased_sample_series(data: pd.Series, base: float = 0.5, cutoff: int = None) -> pd.Series:
    if cutoff is None or cutoff > len(data):
        cutoff = len(data)

    # Генерируем вероятности для каждого количества элементов
    probabilities = np.array([base**i for i in range(1, cutoff + 1)])
    probabilities /= probabilities.sum()  # Нормализуем вероятности

    # Выбираем количество элементов на основе этих вероятностей
    count = np.random.choice(range(1, cutoff + 1), p=probabilities)

    # Перемешиваем данные и берем первые count элементов
    sampled_data = data.sample(
        frac=1, random_state=np.random.randint(0, 1e6))  # Перемешивание
    return sampled_data.head(count)


class HeroGenerationSteps(Enum):
    INITIAL = "INITIAL"
    GENDER = "GENDER"
    FEMALE_NAME = ("FEMALE_NAME",)
    MALE_NAME = ("MALE_NAME",)
    OCCUPATION = "OCCUPATION"
    TIMEKILLER = "TIMEKILLER"
    RACE = "RACE"
    HAREM_WITH_GIRLS = "HAREM_WITH_GIRLS"
    HAREM_WITH_BOYS = "HAREM_WITH_BOYS"
    REINCARNATION_CAUSE = "REINCARNATION_CAUSE"
    devine_bleesing = "devine_bleesing"
    SKILL = "SKILL"
    UNIQUE_ITEM = "UNIQUE_ITEM"
    WEAKNESS = "WEAKNESS"


class HeroGenerator(Machine):
    _transitions = [
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.INITIAL,
            "dest": HeroGenerationSteps.GENDER,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.GENDER,
            "dest": HeroGenerationSteps.MALE_NAME,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.GENDER,
            "dest": HeroGenerationSteps.FEMALE_NAME,
            "unless": "is_male",
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.MALE_NAME,
            "dest": HeroGenerationSteps.OCCUPATION,
            "conditions": "is_male",
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.FEMALE_NAME,
            "dest": HeroGenerationSteps.OCCUPATION,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.OCCUPATION,
            "dest": HeroGenerationSteps.devine_bleesing,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.devine_bleesing,
            "dest": HeroGenerationSteps.SKILL,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.SKILL,
            "dest": HeroGenerationSteps.UNIQUE_ITEM,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.UNIQUE_ITEM,
            "dest": HeroGenerationSteps.WEAKNESS,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.WEAKNESS,
            "dest": HeroGenerationSteps.TIMEKILLER,
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.TIMEKILLER,
            "dest": HeroGenerationSteps.HAREM_WITH_BOYS,
            "unless": "is_male",
        },
        {
            "trigger": "proceed",
            "source": HeroGenerationSteps.TIMEKILLER,
            "dest": HeroGenerationSteps.HAREM_WITH_GIRLS,
            "conditions": "is_male",
        },
    ]

    def __init__(self, random_seed: int = None):
        self.random_seed = random_seed
        self.gender = None
        self.name = None
        self.occupation = None
        self.timekiller = None
        self.harem = None
        self.devine_bleesing = None
        self.skill = None
        self.unique_item = None
        self.weakness = None
        self.fake = Faker("ja-JP")
        super().__init__(
            states=HeroGenerationSteps,
            transitions=self._transitions,
            initial=HeroGenerationSteps.INITIAL,
            send_event=True,
        )

    @property
    def is_male(self):
        return self.gender == "M"

    def reset_random_seed(self):
        if self.random_seed is not None:
            random.seed(self.random_seed)
            Faker.seed(self.random_seed)
            np.random.seed(self.random_seed)

        if self.may_trigger("to_INITIAL"):
            self.trigger("to_INITIAL")

        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_GENDER(self, event):
        self.gender = random.choice(["M", "F"])
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_FEMALE_NAME(self, event):
        self.name = self.fake.romanized_name_female()
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_MALE_NAME(self, event):
        self.name = self.fake.romanized_name_male()
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_OCCUPATION(self, event):
        self.occupation = ", ".join(
            [
                string.strip()
                for string in select_random_item(
                    attributes["occupation"]["occupation"]
                ).values
            ]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_TIMEKILLER(self, event):
        self.timekiller = ", ".join(
            [
                string.strip()
                for string in select_random_item(
                    attributes["timekiller"]["timekiller"]
                ).values
            ]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_HAREM_WITH_BOYS(self, event):
        self.harem = ", ".join(
            [self.fake.romanized_name_male()
             for _ in range(random.randint(0, 10))]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_HAREM_WITH_GIRLS(self, event):
        self.harem = ", ".join(
            [self.fake.romanized_name_female()
             for _ in range(random.randint(0, 10))]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_devine_bleesing(self, event):
        self.devine_bleesing = ", ".join(
            [
                string.strip()
                for string in biased_sample_series(
                    attributes["devine_bleesing"]["devine_bleesing"], base=0.5
                ).values
            ]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_SKILL(self, event):
        self.skill = ", ".join(
            [
                string.strip()
                for string in biased_sample_series(
                    attributes["skill"]["skill"], base=0.5
                ).values
            ]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_UNIQUE_ITEM(self, event):
        self.unique_item = ", ".join(
            [
                string.strip()
                for string in biased_sample_series(
                    attributes["unique_item"]["unique_item"], base=0.5
                ).values
            ]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def on_enter_WEAKNESS(self, event):
        self.weakness = ", ".join(
            [
                string.strip()
                for string in biased_sample_series(
                    attributes["weakness"]["weakness"], base=0.5
                ).values
            ]
        )
        if self.may_trigger("proceed"):
            self.trigger("proceed")

    def generate_hero(self, random_seed: int = None):
        if random_seed is not None:
            self.random_seed = random_seed

        self.reset_random_seed()

        return {
            "gender": self.gender,
            "name": self.name,
            "occupation": self.occupation,
            "timekiller": self.timekiller,
            "harem": self.harem,
            "devine_bleesing": self.devine_bleesing,
            "skill": self.skill,
            "unique_item": self.unique_item,
            "weakness": self.weakness,
            "_seed": self.random_seed,
        }
