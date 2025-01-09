from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.routes.v3.hero_generator import HeroGenerator
from app.routes.v3.story_generator import StoryGenerator
from app.utils.helpers import verify_credentials

router = APIRouter()

hero = HeroGenerator()
story = StoryGenerator()

security = HTTPBasic()


@router.get("/generate", description="Generates a random hero with all attributes.")
async def generate_hero(random_seed: int = None, credentials: HTTPBasicCredentials = Depends(security)):
    """Generate a random hero."""
    verify_credentials(credentials)
    hero.set_random_seed(random_seed)
    hero_data = hero.generate_hero()
    return hero_data


@router.get("/generate_story", description="Generates a random story with 17 steps of Campbell's monomyth.")
async def generate_story(credentials: HTTPBasicCredentials = Depends(security)):
    """Generate a random story."""
    verify_credentials(credentials)
    story_data = story.generate_story()
    return story_data
