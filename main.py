from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pymongo import ReturnDocument
from v1.mastermindv1 import get_next_nr_game, check_guess, NR_CHAR
from core.db_init import collection
import random
import logging

app = FastAPI()
log = logging.getLogger("my-api")


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
    secret_code = "".join(random.choices(["R", "G", "B", "Y"], k=NR_CHAR))
    nr_game_id = get_next_nr_game()
    return {"msg": f"Game created successfully. Game ID: {nr_game_id}, secret_code {secret_code}"}


@app.get("/game/{game_id}")
async def get_game(game_id: int):
    game_info = collection.find_one({"game_id": game_id}, {"_id": False, "secret_code": False})
    guesses = game_info.get("guesses", [])
    b_pegs = game_info.get("b_pegs", 0)
    w_pegs = game_info.get("w_pegs", 0)
    return {"id": game_id, "Previous guesses": guesses, "black pegs": b_pegs, "white pegs": w_pegs}


@app.post("/game/{game_id}/guess")
async def make_guess(game_id: int, guess: Guess):
    log.info(f"game id: {game_id}, guess: {guess.guess}")
    game_info = collection.find_one_and_update({"game_id": game_id},
                                               {"$push": {"guesses": guess.guess}},
                                               projection={"_id": False, "secret_code": True},
                                               return_document=ReturnDocument.AFTER)
    if game_info["secret_code"] == guess.guess:
        return {"id": game_id, "secret_code": guess.guess, "msg": "success"}
    else:
        b_pegs, w_pegs = check_guess(guess.guess, game_info["secret_code"])
        return {"id": game_id, "msg": "keep trying", "black pegs": b_pegs, "white pegs": w_pegs}
