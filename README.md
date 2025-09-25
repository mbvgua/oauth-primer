# Oauth Primer

### Table Of Contents
1. [Project description](#project-description)
2. [Project setup](#project-setup)
    1. [Setup on local device](#setup-on-local-device)
    2. [Setup with Docker](#setup-with-docker)

## Project Descrption

- A minimal project primarily aimed at understanding the implementation of [Oauth](https://en.wikipedia.org/wiki/OAuth). I have built it with python, using Flask as my framework of choice. A comprehensive list of all required modules can be found in the [`requirements.txt`](./requirements.txt) file.

## Project Setup

- The are two main ways to setup and run the application, which I have described below:
    - Local setup on your machine with python and pip
    - Setup with docker

### Setup on local device

1. Create a virtual environment. A common and well thought out name is `.venv`/`venv` e.t.c:

```bash
$ python -m venv .venv
```

2. Activate the virtual environment:

```bash
$ source .venv/bin/activate
```

> [!NOTE]
>
> This method only works for Unix based operating systems, i.e Linux and MacOs. If you are using Windows, try `.venv\Scripts\activate`

3. Next install all dependencies in the `requirements.txt` file:

```bash
(.venv)$ pip install -r requirements.txt
```

4. Finally, start the python server and navigate to `https://127.0.0.1:5000/` where you'll find the server running:

```bash
(.venv)$ python app.py
```

### Setup with Docker

1. Pull the docker image
```bash
$ docker pull mbvgua/oauth-primer:v1
```

2. Run the container:
```bash
$ docker run -p 5000:5000 mbvgua/oauth-primer:v1
```

3. Navigate to `https:127.0.0.1:5000/` where the server will be running

## Todos

- Add mechansim to check validity of email and password in `auth` module
- Add the admin dashboard    
- Change db from sqlite3 to MySql    
- Add mechanism to send emails to user once account has been created    
