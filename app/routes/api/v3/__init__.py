from fastapi import APIRouter
from .hero_generator import HeroGenerator
from .story_generator import StoryGenerator

router = APIRouter()

hero = HeroGenerator()
story = StoryGenerator()


@router.get("/generate", description="Generates a random hero with all attributes.")
async def generate_hero(random_seed: int = None):
    """Generate a random hero."""
    hero.set_random_seed(random_seed)
    hero_data = hero.generate_hero()
    story_data = story.generate_story()
    hero_data["hero_path"] = " -> ".join(story_data.values())
    return hero_data
