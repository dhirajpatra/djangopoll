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
No sophisticated measures and checks are needed.
Just if I voted I shouldn't see the vote option for that question.

### Navigation
You should implement the navigation between pages, and from the main page.
So everything (e.g., see questions, create new, vote, etc) can be done without the need to type the URL manually.

### Tests & code style
The question creation should be covered by automated tests, which must be run by `make test`.
The code should follow PEP 8.

The linting must be run by `make lint`.

### Logging
You should log all main actions (e.g., creating a new question, voting, etc) to the console.



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

## Delivery
You should create a new private GitHub repository and send an invitation to [@maltsev](https://github.com/maltsev).
Then commit the initial code you downloaded to the master branch and create a new pull request against it with your changes.
Then assign it to me for a review.
Make sure you receive notifications from Github as I'll submit the review on the pull request page.

Ping me at [kirill@edaider.com](mailto:kirill@edaider.com) if you have any questions!
