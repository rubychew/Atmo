FROM python:3.13.1

# set a working directory inside the container's own file system
WORKDIR /app

# install dependencies
# dependencies don't change that often so copy them separately and docker
# will cache them, so you won't have to reinstall them
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
# this copies everything from the root folder, main.py etc.
COPY . /app

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]