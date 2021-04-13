# Test project

## Introduction

This is an app from [the official Django tutorial](https://docs.djangoproject.com/en/3.1/intro/).
You should implement new features:

## Features description

### Question creation

A user, as a guest, should be able to create new questions (NOT using the Django admin interface).
Each question must have minimum 1 and maximum 10 answers.
The system should store an IP address of a user that created a question.

### No double voting

Users shouldn't be able to vote several times for the same question.
As a user, I'd like to see the available questions even if I have already voted.
No sophisticated measures and checks are needed.
Just if I voted I shouldn't see the vote option for that question.

### Navigation

Simple implemention of the navigation between pages, and from the main page.
So everything (e.g., see questions, create new, vote, etc) can be done without the need to type the URL manually.

### Tests & code style

The question creation covered by automated tests, which run by `make test`.
The code followed PEP 8.
The linting run by `make lint`.

### Logging

Simple print log all main actions (e.g., creating a new question, voting, etc) to the console. For the sake of simplicity not used django logging.

## Setup

Python 3 and SQLite are required.

```sh
pip install -r requirements.txt
make migrate
```

To run a local server:

```sh
make serve-local
```
