from app.core.db_init import collection
NR_CHAR = 4


def get_next_nr_game():
    last_game = collection.find_one(sort=[("game_id", -1)])
    last_game_id = last_game["game_id"] + 1 if last_game else 0
    return last_game_id


def check_guess(guess: str, secret_code: str):
    exact_matches, color_matches = 0, 0
    for i in range(NR_CHAR):
        if guess[i] == secret_code[i]:
            exact_matches += 1
        elif guess[i] in secret_code:
            color_matches += 1
    return exact_matches, color_matches
