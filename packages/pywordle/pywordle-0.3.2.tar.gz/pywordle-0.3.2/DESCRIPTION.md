# PyWordle

This package can help you playing the [Wordle](https://www.powerlanguage.co.uk/wordle/) game. It will not play for you. You will still have to choose the best strategy.

## Installation

The tool can easily be installed on a computer where a recent (>=3.10) version of Python is present.

```bash
python3 -m venv venv
. venv/bin/activate
pip install pywordle
```

## Usage

Each time that you want to enter a new word, you will ask the tool to provide a list of candidates. When you have selected a word, type it in as well as the result provided by the `Wordle` game. The code values for the result colours are:

* Dark gray: 0
* Yellow: 1
* Green: 2

Here is an example:

```bash
$ wordle --letters=etaions --unique
Here is the list of 37 possibilities: {'aeons': 2.72, 'onset': 2.87, 'saint': 4.43, 'tinea': 0, 'oaten': 0, 'antes': 3.17, 'siena': 2.4, 'atone': 3.11, 'tines': 2.7, 'steno': 1.97, 'stoae': 0, 'anise': 2.3, 'taino': 0, 'stain': 3.78, 'stoai': 0, 'notes': 4.36, 'sotie': 0, 'iotas': 2.68, 'tenia': 2.73, 'neats': 3.93, 'nates': 0, 'satin': 3.12, 'etnas': 2.43, 'senti': 1.97, 'antis': 4.33, 'stone': 4.68, 'seton': 1.73, 'tsine': 0, 'entia': 0, 'eosin': 1.74, 'ostia': 1.82, 'tones': 4.27, 'tains': 2.2, 'inset': 1.73, 'noise': 4.6, 'stane': 0, 'stein': 3.38}
Please enter the word played:
noise
Please enter the result:
20001
Saving result for 'noise': [2, 0, 0, 0, 1]
```

The result will be stored in today's game file and be used next time you call the tool, limiting the possibilities. Just type `Enter`, if you do not want to choose a word just yet. Each day a file `games/YYYYMMDD.json` will be created to hold your progress.

All the command line options can be found with the `--help` option.

```bash
$ wordle --help
usage: Propose words for the Wordle game. [-h] [--large] [--stats] [--none] [--unique] [--check] [--verbose] [--letters LETTERS] [--minfrequency MINFREQUENCY]

options:
  -h, --help            show this help message and exit
  --large               Uses the large file of English words.
  --stats               Displays some stats about the found words.
  --none                Use none of the previously used letters.
  --unique              Do not repeat letters in a word.
  --check               Check that the word is valid.
  --verbose             Print progress.
  --sort                Make sure the words are in alphabetic order.
  --letters LETTERS     The set of letters to be used.
  --language {en,fr,es}
                        The language of the game
  --minfrequency MINFREQUENCY
                        A minimum frequency for the proposed words, either 0 (not found) or between 1 and 7.

```

### Letters

The `--letters` is useful to start the game with a word that is using the most common English letters to have the best chances to find letters of the solution word. It also could be a good idea to add the `--unique` option to avoid repeating a letter.

```bash
wordle --letters=etaionshr --unique
```

### None

This is a different strategy. Instead of looking for a possible word, you are trying to look for information on letters that you have not used yet today. This is not possible if you have selected the `Hard Mode`. It only makes sense to use the option for the second and possibly third word. Again the `--unique` option will give you more information.

```bash
wordle --none --unique
```

### Stats

This will give you some statistics in the list of proposed words. First you will get the most used letters in that list. Then you will get the words that used the most used letters. This is another strategy to give you more chance to have valuable information.

```bash
$ wordle --letters=etaion --unique --stats
Here is the list of 6 possibilities: {'tinea': 0, 'oaten': 0, 'atone': 3.11, 'taino': 0, 'tenia': 2.73, 'entia': 0}
10 most used letters in the words: a, n, t, e, i, o, b, c, d, f
5 most scored words: tinea, tenia, entia, oaten, atone
Please enter the word played:

No play recorded.
```

### Using the Words API

In order to check the validity and frequency of the words with a call to the [Words API](https://github.com/dwyl/english-words), you need to store a valid [Rapid API](https://rapidapi.com) key in `RAPIDAPI_KEY` environment variable. It is free for up to 2500 words per day. Once a word is checked, it is stored locally so it will not be checked again the next days. When there is no more "null" values in your JSON word file, you do not need to check the Words API anymore.

```bash
export RAPIDAPI_KEY="{YourKey}"
wordle --check
```

### Frequency

When checking a word in the API, we store its frequency. The solution of the Wordle game tends to be a word with a high frequency.

```bash
wordle --minfrequency=5
```

### Large English word list

By default the tool will rely on a list that contains less than 4300 words of 5 letters. The good news is that most are valid but a few are missing. With the `--large` option, you will use a list with nearly 16000 words of 5 letters. It's exhaustive but unfortunately it also contains many invalid words. This is where the Words API will become handy. But beware of your daily quota.

It is critical to choose at the first run of the tool if you decide to start from the large list or not. After that, the option will be ignored and we will only use the generated JSON file: `words/words.en.json`. If you delete it to start again, you will lose the benefit of all the checks you have done with the Words API.

```bash
wordle --large
```

### French words

The list of 5 letters French words was retrieved from [ListesDeMots](https://www.listesdemots.net/mots5lettres.htm).

### Spanish words

The list of Spanish words was retrieved from [an-array-of-spanish-words](https://github.com/words/an-array-of-spanish-words/blob/master/index.json).
