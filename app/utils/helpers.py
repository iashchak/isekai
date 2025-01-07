import random
import numpy as np
import pandas as pd
from faker import Faker
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends, HTTPException, status, Query

def select_reverse_exponential_items(items: pd.Series,
                                    k: float = 3,
                                    p_zero: float = 0.4) -> pd.Series:
    """
    Select a random number of items (from 0 up to len(items)) according
    to a "reverse exponential"-like scheme:
      - with probability p_zero, return 0 items;
      - probabilities for returning i>0 items decay roughly like (1 - p_zero)**(i^k);
      - we then sample exactly r items from the original Series, once r is chosen.
    """
    n = len(items)
    if n == 0:
        return pd.Series(dtype=items.dtype)

    probs = []
    for i in range(n):
        if i == 0:
            probs.append(p_zero)
        else:
            probs.append(p_zero * (1 - p_zero)**(i**k))
    tail = 1.0 - sum(probs)
    tail = max(tail, 0.0)
    probs.append(tail)
    probs = np.array(probs)
    probs = probs / probs.sum()
    r = np.random.choice(np.arange(n + 1), p=probs)

    if r == 0:
        return pd.Series(dtype=items.dtype)
    return items.sample(r)

def select_random_item(items: pd.Series, k: int = 1) -> pd.Series:
    """
    Selects a random item from the series.
    """
    return items.sample(k)

def generate_random_japaneese_name(is_male: bool = None) -> str:
    """
    Generates a random japaneese name.
    """
    fake = Faker('ja_JP')
    if is_male is None:
        return fake.romanized_name()
    elif is_male:
        return fake.romanized_name_male()
    else:
        return fake.romanized_name_female()
    

# Функция проверки учетных данных
def verify_credentials(credentials: HTTPBasicCredentials):
    """
    Validates username and password for Basic Authentication.
    """
    correct_username = "isekai-lover"
    correct_password = "isekai-lover"  # Replace with a secure password
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )