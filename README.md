# Domain Inspiration Tool

This is a quick command-line tool that can be used to generate a set of synonyms
from some input, and then to check if the resulting set corresponds to domain names
that are potentially available for use.

I tossed this together for my own use-- so use it at your own risk or whatever.

## Installation

I'm running Python 3.9.15 for this build and have created a virtualenv.

You can create the virtualenv in the `venv` directory with the following command.

```bash
$ python -m venv venv
```

Don't forget to activate it. I'm assuming that you're on a UNIX-like environment
in this particular case.

```bash
$ source venv/bin/activate
```

You should be able to install most of the dependencies using the following command.
In this case, I'm using pip version 23.0.

```bash
$ pip install -r requirements.txt
```

You might need to make sure that SQLite is available for Python. In my case, I
needed to install it for my FreeBSD 13.1 instance.

```bash
$ sudo pkg install databases/py-sqlite3
```

You'll also likely need to have the NLTK WordNet database downloaded. You can do
this in the Python shell.

```python
>>> import nltk
>>> nltk.download('wordnet')
```

If all else fails, please try turning it off and back on again.

## Usage

You should start off by initializing the database.

```bash
$ python -m dominsp init
```

This will prompt you to choose a location to save your stuff. Or use the default,
that's cool too.

Then, go add some preliminary words. For example, here I'll use `dog` and `cat`
as a starting point.

```bash
$ python -m dominsp add dog
$ python -m dominsp add cat
```

Then, you'll want to process them. Use this command to do that.

```bash
$ python -m dominsp process
```

That'll take a bit probably. You won't really get a response until it's done, or
unless it errors out. Who knows, we're all subject to the Halting Problem. In any
case, it'll tell you if it's done.

You can list all of the results if you choose.

```bash
$ python -m dominsp list
```

That'll give you a thrown-together table of all retrieved synonyms. There's a status
code assigned to each of them. In brief:

| Status Code | Description                                                                                                                                   |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 0           | You added this word to the database, but it hasn't been processed yet.                                                                        |
| 1           | You may or may not have added this word. It's either a retrieved synonym or a word you added, but the domain hasn't been checked yet.         |
| 2           | This word corresponded to a `.COM` domain name. Sorry, you can't claim it without beating the domain owner in a fight to the death. Probably. |
| 3           | Congrats, this domain has not been claimed so the annoying domain parkers haven't jacked up the price. Yet.                                   |

In reality, the status codes aren't all that important. More likely, you'll want
to cut straight to the chase-- a listing of domains that are available (for now).
You can get that with the following command.

```bash
$ python -m dominsp list-available
```

That'll give you a list of the domains that were available at the time of query.
I haven't built a way to reset the list for re-checking, but the database file
is easy to manually edit. It's just JSON. Enjoy.

One more thing. You are able to combine words-- but there's a limitation, because
this can get pretty intensive if the word lists are long. Each set of two words
can be combined exactly once using the following command.

```bash
$ python -m dominsp combine
```

Words will also be combined with themselves. So for example, if you combine the
words `cat` and `dog`, you'll end up with:

- catcat
- catdog
- dogcat
- dogdog

So that's obviously something like O(n^2) right off the bat in terms of complexity.
You'll need to re-process new synonyms after you use it. Use it wisely.

## Licensing

I've released this under the MIT License. That holds true unless the licensing
police come after me for some unforseen reason. I tossed this together using inspiration
from [this blog post](https://realpython.com/python-typer-cli/) written by Leodanis
Pozo Ramos. Credit where credit is due.
