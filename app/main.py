from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pymongo import ReturnDocument
from app.v1.mastermindv1 import get_next_nr_game, check_guess, NR_CHAR
from app.core.db_init import collection
import random
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Guess(BaseModel):
    guess: str


@app.get('/favicon.ico')
async def favicon():
    favicon_path = 'favicon.ico'
    return FileResponse(favicon_path)


@app.get("/")
def get_root_page():
    return {"Hello": "World"}


@app.post("/game", status_code=201)
async def create_game():
    log.info("")
    # k: number of elements picked randomly
    secret_code = "".join(random.choices(["R", "G", "B", "Y"], k=NR_CHAR))
    nr_game_id = get_next_nr_game()
    log.info(f"[create_game] Creating game nr {nr_game_id}")
    collection.insert_one({"secret_code": secret_code, "game_id": nr_game_id})
    return {"msg": f"Game created successfully. Game ID: {nr_game_id}, secret_code {secret_code}"}


@app.get("/game/{game_id}", status_code=200)
async def get_game(game_id: int):
    log.info(f"[get_game] game id: {game_id}")
    game_info = collection.find_one({"game_id": game_id}, {"_id": False, "secret_code": False})
    guesses = game_info.get("guesses", [])
    b_pegs = game_info.get("b_pegs", 0)
    w_pegs = game_info.get("w_pegs", 0)
    return {"id": game_id, "Previous guesses": guesses, "black pegs": b_pegs, "white pegs": w_pegs}


@app.post("/game/{game_id}/guess", status_code=201)
async def make_guess(game_id: int, guess: Guess):
    guess.guess = guess.guess.upper()
    log.info(f"[make_guess] game id: {game_id}, guess: {guess.guess}")
    game_info = collection.find_one_and_update({"game_id": game_id},
                                               {"$push": {"guesses": guess.guess}},
                                               projection={"_id": False, "secret_code": True},
                                               return_document=ReturnDocument.AFTER)
    if game_info["secret_code"] == guess.guess:
        return {"id": game_id, "secret_code": guess.guess, "msg": "success"}
    else:
        b_pegs, w_pegs = check_guess(guess.guess, game_info["secret_code"])
        return {"id": game_id, "msg": "keep trying", "black pegs": b_pegs, "white pegs": w_pegs}


@app.delete("/game/{game_id}/delete", status_code=204)
async def delete_game(game_id: int):
    log.info(f"[delete_game] game id: {game_id}")
    _ = collection.find_one_and_delete({"game_id": game_id}, projection={"_id": False})
