from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from v1.mastermindv1 import get_next_nr_game
from core.db_init import collection
import random

app = FastAPI()


class Game(BaseModel):
    secret_code: str


class Guess(BaseModel):
    guess: str


@app.get('/favicon.ico')
async def favicon():
    favicon_path = 'favicon.ico'
    return FileResponse(favicon_path)


@app.get("/")
def get_root_page():
    return {"Hello": "World"}


@app.post("/game")
async def create_game():
    # k: number of elements picked randomly
    secret_code = "".join(random.choices(["R", "G", "B", "Y"], k=4))
    nr_game_id = get_next_nr_game()
    collection.insert_one({"secret_code": secret_code, "game_id": nr_game_id})
    return {"msg": f"Game created successfully. Game ID: {nr_game_id}"}


@app.get("/game/{id}")
async def get_game(game_id: int):
    # Implement logic to retrieve game information from database and updating guesses field
    return {"id": game_id, "secret_code": "RGGB", "guesses": []}


@app.post("/game/{id}/guess")
async def make_guess(game_id: int, guess: Guess):
    # Implement logic to retrieve game information and compare guess with secret code
    return {"id": id, "guess": guess.guess, "result": "RRBB"}
