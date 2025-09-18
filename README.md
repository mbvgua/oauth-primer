# Oauth Primer

Project aimed at understanding the implemenatation of Oauth on user website. It is coded primarily in `Flask`. A comprehensive list of all modules and packages used, can be found in the [`requirements.txt`](./requirements.txt) file

# Setup

1. To get started, you need to first create a virtual environment. A common and well thought out name is `.venv`/`.env`/`flask_venv` e.t.c:

```bash
python -m venv .venv
```

2. Next you need to activate the virtual environment:

```bash
source .venv/bin/activate
```

> [!NOTE]
>
> This method only works for Unix based operating systems, i.e Linux and MacOs. If you are using Windows, look for altenative means to startup you virtual environment.

3. Next, you install all dependencies in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

4. Finally, you will start the python server, and using the link outputted in the logs, navigate to the select web url:

```bash
python app.py
```
> [!NOTE]
>
> You will need to run the `python app.py` command twice! The first one will create the database, then the second one creates the server.
>
> The server will be running on address: `https://127.0.0.1:5000/`, due to the `openSSL` module.
>
> For a smooth worlflow as demonstarted above, First ensure that you have `python 3.*` and `pip` installed.
