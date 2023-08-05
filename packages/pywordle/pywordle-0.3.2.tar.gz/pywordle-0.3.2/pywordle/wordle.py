#!/usr/bin/env python
"""
Play Wordle game
https://www.powerlanguage.co.uk/wordle/

Usage:
poetry install
poetry run wordle --help
"""

from argparse import ArgumentParser, Namespace
from collections import OrderedDict
from datetime import datetime
from importlib.resources import open_text
from json import dump, loads
from os import getenv, makedirs
from os.path import join
from string import ascii_letters
import sys
from typing import Any, Dict, List, Generator, Callable, Union, Optional

from marshmallow import Schema, fields, post_load
from pytz import timezone
from requests import get

WORDS_DIR = "words"
ARGS = Namespace()
WORDS_API: Dict[str, int] = {"counter": 0, "quota": 2500}


# pylint: disable=no-member, no-self-use


def parse_arguments() -> None:
    """
    Parse the command line arguments.
    """
    parser = ArgumentParser("Propose words for the Wordle game.")
    parser.add_argument("--large", action="store_true", help="Uses the large file of english words.")
    parser.add_argument("--stats", action="store_true", help="Displays some stats about the found words.")
    parser.add_argument("--none", action="store_true", help="Use none of the previously used letters.")
    parser.add_argument("--unique", action="store_true", help="Do not repeat letters in a word.")
    parser.add_argument("--check", action="store_true", help="Check that the word is valid.")
    parser.add_argument("--verbose", action="store_true", help="Print progress.")
    parser.add_argument("--sort", action="store_true", help="Make sure the words are in alphabetic order.")
    parser.add_argument("--letters", help="The set of letters to be used.")
    parser.add_argument("--language", choices=["en", "fr", "es"], default="en", help="The language of the game")
    parser.add_argument(
        "--minfrequency",
        type=float,
        help="A minimum frequency for the proposed words, either 0 (not found) or between 1 and 7.",
    )
    parser.parse_args(namespace=ARGS)
    if ARGS.check and getenv("RAPIDAPI_KEY") is None:
        print(
            "You need to provide a valid Rapid API key in RAPIDAPI_KEY environment variable",
            "to be able to check the existence and the usage frequency of the words.",
        )
        sys.exit(1)


class Play:
    """
    This represent a played word with its result.
    For each letter is the corresponding code:
    0: letter not in word
    1: letter in word in a different position
    2: letter in word in that position
    """

    word: str
    result: List[int]

    def __init__(self, word: str, result: List[int]):
        self.word = word
        self.result = result

    def is_valid(self, word: str) -> bool:  # NOSONAR
        """
        Check if the new word would give this result for the current word.
        """
        if len(self.word) != len(word):
            return False
        letters = list(self.word)
        newletters = list(word)
        # First handle the exact match
        for index, letter in enumerate(letters):
            if self.result[index] == 2:
                if newletters[index] != letter:  # Exact match is missing
                    return False
                letters[index] = "_"
                newletters[index] = "_"
        # Now handle the non exact match
        for index, letter in enumerate(letters):
            if self.result[index] == 1:
                if newletters[index] == letter:  # This is an exact match where it should not
                    return False
                if letter not in newletters:  # We should find this letter in the solution
                    return False
                letters[index] = "_"
                newindex = newletters.index(letter)
                newletters[newindex] = "_"
        # Finally handle the miss
        for index, letter in enumerate(letters):
            if self.result[index] == 0 and letter in newletters:  # There should be no match
                return False
        # It's all good, we have a match
        return True

    def is_none(self, word: str) -> bool:
        """
        Check if the proposed word has none of the letters of the played word.
        """
        for letter in word:
            # Letter is never used before
            if letter in self.word:
                return False
        return True


class Game:
    """
    This is a full game session with the list of words played already.
    """

    played: List[Play]

    def __init__(self, played: List[Play]):
        self.played = played

    def is_valid(self, word: str) -> bool:
        """
        Check each word played to see if the provided one is a match.
        """
        for play in self.played:
            if not play.is_valid(word):
                return False
        return True

    def is_none(self, word: str) -> bool:
        """
        Check each word played to see if the provided one uses any of the letters.
        """
        for play in self.played:
            if not play.is_none(word):
                return False
        return True


class PlaySchema(Schema):
    """
    Marshmallow schema of the Play object.
    """

    word = fields.Str()
    result = fields.List(fields.Integer)

    @post_load
    def make_play(self, data: Any, **_: Any) -> Play:
        """
        This mill create a Play object when invoking a load() on the schema.
        """
        return Play(**data)


class GameSchema(Schema):
    """
    Marshmallow schema of the Game object.
    """

    played = fields.List(fields.Nested(PlaySchema))

    @post_load
    def make_game(self, data: Any, **_: Any) -> Game:
        """
        This will create a Game object when invoking a load() on the schema.
        """
        return Game(**data)


def get_game(gamefilename: str) -> Union[Game, Any]:
    """
    Get the current game progress from a JSON file.
    """
    try:
        with open(gamefilename, mode="r", encoding="utf_8") as gfile:
            return GameSchema().loads(gfile.read())
    except FileNotFoundError:
        # If the game file was not found, we create it
        # First we make sure that the games directory exists
        makedirs("games", exist_ok=True)
        emptygame: dict[str, List[Any]] = {"played": []}
        with open(gamefilename, mode="w", encoding="utf_8") as gfile:
            dump(emptygame, gfile, indent=4)
        return GameSchema().load(emptygame)


def get_words_txt(language: str) -> Generator[str, None, None]:
    """
    Read the words from the words.{language}.txt file.
    It is now a ressource provided by the package.
    """
    wordsfilename = f"words.{language}.txt"
    with open_text("pywordle.words", wordsfilename) as wfile:
        for line in wfile:
            yield line.split("\n")[0]


def save_words(words: Dict[str, Optional[int]]) -> None:
    """
    Save the words
    """
    # Make sure the words directory exists
    makedirs(WORDS_DIR, exist_ok=True)
    with open(join(WORDS_DIR, f"words.{ARGS.language}.json"), mode="w", encoding="utf_8") as jsonfile:
        dump(words, jsonfile, indent=4)


def get_words(language: str, sort: bool) -> Dict[str, Optional[int]]:
    """
    Read the words from the local JSON file that already has the already fetched
    frequency from Words API.
    If empty, create one from the text file.
    """
    # Get the list of words from the local JSON file
    try:
        with open(join(WORDS_DIR, f"words.{language}.json"), mode="r", encoding="utf_8") as jsonfile:
            words: Dict[str, Optional[int]] = loads(jsonfile.read())
    except FileNotFoundError:
        # If not found we initialize it with the content of the text file
        words = {word: None for word in get_words_txt(language) if len(word) == 5}
        save_words(words)

    if sort:
        words = dict(OrderedDict(sorted(words.items(), key=lambda item: item[0])))

    # Return the words
    return words


def wordsapi(word: str) -> Optional[int]:
    """
    Get the frequency from the Words API.
    The frequency can be:
    >0 : valid frequency
    0: word known to Words API but no frequency
    None: word unknown to Words API
    """
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"

    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": getenv("RAPIDAPI_KEY"),
    }

    response = get(url, headers=headers)

    # We got a call
    WORDS_API["counter"] += 1

    if response.status_code == 200:
        frequency: Optional[int] = loads(response.text).get("frequency", 0)
    else:
        frequency = None

    verbose(f"Checked the Words API for '{word}': {frequency}")

    return frequency


def filterapi(selected: Dict[str, Optional[int]], words: Dict[str, Optional[int]]) -> Dict[str, Optional[int]]:
    """
    Check the Words API, but first see if we didn't do it already.
    """

    unknown: List[str] = []

    try:

        # Check each selected words
        for word, frequency in selected.items():

            # We already have the frequency
            if frequency is not None:
                continue

            # We already reached the quota
            if WORDS_API["counter"] >= WORDS_API["quota"]:
                continue

            # Let's ask the API about it.
            frequency = wordsapi(word)

            # Update the dictionaries of words
            if frequency is None:  # Not known by the Words API
                unknown.append(word)  # To be removed later, outside the loop
            else:
                selected[word] = frequency
                words[word] = frequency

        # Remove the words unkown to the API
        for word in unknown:
            words.pop(word)
            selected.pop(word)

        # Update the words file
        save_words(words)

    except KeyboardInterrupt:
        # Remove the words unkown to the API
        for word in unknown:
            words.pop(word)
        # We want to make sure we save the good work
        save_words(words)
        # Tell the user and exit
        print("\nFilter with the Words API stopped manually by you!")
        sys.exit(1)

    return selected


def stats(words: Dict[str, Optional[int]]) -> None:
    """
    Print various stats about the list of words.
    """
    # Count the usage if each letters in the list of words
    counter = {letter: 0 for letter in ascii_letters}
    for word in words.keys():
        for letter in word:
            try:
                counter[letter] += 1
            except KeyError:
                print(f"The word {word} contains non alpha letter: {letter}")

    # Display the 10 most used letters
    countersorted = sorted(counter.items(), key=lambda item: -item[1])
    mostusedletters = [item[0] for item in countersorted[:10]]
    print(f"10 most used letters in the words: {', '.join(mostusedletters)}")

    # Scores each word with the frequency of its letters
    score = {}
    for word in words.keys():
        score[word] = 0
        for letter in word:
            score[word] += counter[letter]

    # Display the 5 most highest scored words
    scoresorted = sorted(score.items(), key=lambda item: -item[1])
    mostscoredword = [item[0] for item in scoresorted[:5]]
    print(f"5 most scored words: {', '.join(mostscoredword)}")


def verbose(text: str) -> None:
    """
    Print a message on the console in verbose mode.
    """
    if ARGS.verbose:
        print(text)


def composedofletters(word: str, letters: str) -> bool:
    """
    Check if a word only contains the provided letters.
    """
    for letter in word:
        if letter not in letters:
            return False
    return True


def filterwords(
    words: Dict[str, Optional[int]], predicate: Callable[[str, Optional[int]], bool]
) -> Dict[str, Optional[int]]:
    """
    Filter a generator of words according to the given predicate.
    """
    return {word: frequency for word, frequency in words.items() if predicate(word, frequency)}


def saveplay(gamefilename: str, game: Game) -> None:
    """
    Records the word that was just played and the result given by Wordle.
    """
    print("Please enter the word played: ")
    word = input()
    if not word:
        print("No play recorded.")
        return
    word = word.lower()
    if len(word) != 5 or not word.isalpha():
        print(f"Invalid word '{word}'. It should be purely alphabetic and 5 characters long.")
        return
    print("Please enter the result:")
    resultstr = input()
    if not resultstr:
        print("No play recorded.")
        return
    try:
        result = [max(min(int(i), 2), 0) for i in resultstr]
    except ValueError:
        print(f"Invalid result '{resultstr}'. It should be a string of 0, 1 and 2 (Ex: 00120).")
        return
    if len(result) != 5:
        print(f"Invalid result '{resultstr}'. There should be 5 values.")
        return

    print(f"Saving result for '{word}': {result}")
    game.played.append(Play(word=word, result=result))
    with open(gamefilename, mode="w", encoding="utf_8") as gamefile:
        dump(GameSchema().dump(game), gamefile, indent=4)

    if result == [2, 2, 2, 2, 2]:
        print("You WON!!!!")


def main() -> None:
    """
    Module's entry point.
    """
    parse_arguments()

    game_file = f"games/{datetime.now(timezone('CET')).strftime('%Y%m%d')}.{ARGS.language}.json"

    words = get_words(ARGS.language, ARGS.sort)
    selected = words

    if ARGS.letters:
        verbose(f"Only use the letters '{ARGS.letters}'")
        selected = filterwords(selected, lambda word, frequency: composedofletters(word, ARGS.letters))

    if ARGS.unique:
        verbose("Only propose words with no letter repetition")
        selected = filterwords(selected, lambda word, frequency: len(word) == len(set(word)))

    # read the current game status
    game = get_game(game_file)

    # Are we looking for a valid word or one that uses none of the letters used before?
    if ARGS.none:
        verbose("Keep the words with only new letters")
        selected = filterwords(selected, lambda word, frequency: game.is_none(word))
    else:
        verbose("Keep the valid words only")
        selected = filterwords(selected, lambda word, frequency: game.is_valid(word))

    # Check if words exist with Words API (only available with the english language)
    if ARGS.check and ARGS.language == "en":
        verbose("Check the existence and frequency with the API")
        selected = filterapi(selected, words)

    if ARGS.minfrequency:
        verbose(f"Keep only words of at least {ARGS.minfrequency} frequency")
        selected = filterwords(selected, lambda word, frequency: bool(frequency and frequency >= ARGS.minfrequency))

    # Show the result
    print(f"Here is the list of {len(selected)} possibilities: {selected}")

    # Show the stats
    if ARGS.stats:
        stats(selected)

    # Save the game play if any
    saveplay(game_file, game)


if __name__ == "__main__":
    main()
