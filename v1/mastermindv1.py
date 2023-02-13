from core.db_init import collection


def get_next_nr_game():
    last_game = collection.find_one(sort=[("game_id", -1)])
    last_game_id = last_game["game_id"] + 1 if last_game else 0
    return last_game_id
