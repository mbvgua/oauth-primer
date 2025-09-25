# start with a base version with python pre-installed
FROM python:3.13.7-alpine3.22

# open container for interation with host machine
EXPOSE 5000

# set standard working directory
WORKDIR /usr/src/app

# copy the ./requirements.txt file earlier on for caching
# resulting in faster build times
COPY ./requirements* .

# # TODO: find out if this is necesary in a container

# # create and activate the python virtual environment
# RUN python -m venv .venv
# RUN source .venv/bin/activate

# install required modules
RUN pip install -r requirements.txt

# copy app source code
COPY . .

# start the app
CMD ["python","app.py"]

