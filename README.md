# Rules of the game
The goal of the game is to guess the randomly generated code consisting of 4 colors from the following: red (R), green (G), blue (B), and yellow (Y).

Each time a guess is sent, the API will respond with the number of black and white pegs obtained in that guess.

**Black peg**: obtained when a color is correctly guessed in the correct position

**White peg**: obtained when a color is correctly guessed in the incorrect position
The game ends when the code is correctly guessed or after a determined number of attempts.
# Mastermind API
This API provides a RESTful interface to play the game Mastermind. It consists of three endpoints:

## Endpoints
### POST /game
Creates a new game of Mastermind. The secret code is generated randomly, and consists of four characters, each one being one of 'R', 'G', 'B', or 'Y'. The secret code is stored in the database and is compared against the user's guesses.

### GET /game/{game_id}
Retrieves the current state of the game. The game is identified by a unique ID, which is passed as a parameter in the URL. The response contains the following information:

- game_id: the unique identifier for the game.
- secret_code: the secret code for the game, represented as a string of four characters.
- guesses: a list of the user's guesses, each one represented as a string of four characters.
- feedback: a list of feedback for each guess, represented as a string of four characters. Each character represents the feedback for one of the four positions in the guess. A 'B' means that the color is correct and in the right position, while a 'W' means that the color is correct but in the wrong position.
### POST /game/{game_id}/guess
Makes a new guess for an ongoing game. The guess is passed in the request body as a JSON object, with the following format:

```
  "guess": "RRBB"
```
The response contains the same information as the GET /game/{game_id} endpoint, updated with the new guess and its feedback.
### DELETE /game/{game_id}/delete
Delete an existing game identified by a unique ID, which is passed as a parameter in the URL.

# How to run a FASTAPI code
To run a FASTAPI code, you will need to have the following prerequisites installed:

- Python 3.6 or higher
- FastAPI and its dependencies

Once you have the prerequisites installed, follow the steps below to run your FASTAPI code:

1. Clone or download the repository containing the FASTAPI code.
2. Change to the directory where the code is located in your local machine.
3. Create a virtual environment (optional but recommended) to keep the dependencies required for this project separate from your global Python environment.
````commandline
python3 -m venv venv
source venv/bin/activate
````
4. Install the dependencies required for this project using the following command:
````commandline
pip install -r requirements.txt
````
5. Run the FASTAPI code using the following command:
````commandline
uvicorn main:app --reload
````
6. The code should start running and you should see output similar to the following:
````commandline
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
````
7. Open your web browser and navigate to http://127.0.0.1:8000 to access the FASTAPI endpoint
8. In order to get the api fully working we need a MongoDB instance installed with a database called 
``mastermind`` with a collection ``games``.

# Docker
## IMPORTANT
This hasn't been tested yet on the last part of the docker because my personal computer wasn't able to virtualize due to limitations of the BIOS.

## Generate a new container _(this must be done where the Dockerfile is)_
### Build Docker image
````
docker build -t mastermindapi .
````
### Start Docker container
````
docker run -d --name containermastermind -p 80:80 mastermindapi
````

```-d``` is to see logs from Docker
