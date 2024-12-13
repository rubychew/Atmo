# Atmo
### Secure Web Development CA 2

### 1. Instructions
#### 1.1 Description
This application utilises Docker for its application development environment. Server side code is written with the FastAPI framework which runs on Python. The Dockerfile specifies the version of Python to be used in the Docker Container, so you should not need to worry about this or versions of any other server side dependencies, which themselves are versioned in requirements.txt.

#### 1.2 Requirements
In order to build and run the docker container for the application you will need Docker installed and the Docker Engine to be running. The easiest way to do this is to install [Docker Desktop](https://docs.docker.com/desktop/). This project also makes use of Docker Compose and it is included with Docker Desktop by default.

Nearly all dependencies are supplied in requirements.txt at the root of file tree. The main exception is for the CSS which uses Tailwind which uses the Tailwind supplied cdn for development. Therefore you will need an active internet connection for the application UI to render as intended.

#### 1.3 Building the Docker Image and Running the Application
Once Docker Desktop is running Docker Engine will also be running in the background as a daemon.  Navigate to the root directory of the project `/Atmo`. One command only should be needed to build the image, intall dependcies and run the server for the first time.

```bash
docker-compose up --build
```

At this point you should be able to navigate to the home page of the application by going to [localhost](http://localhost:8080).

If you wish to stop the application press `ctrl c`. To restart a second time you will not need to rebuild. One Docker Engine is running, simply enter:
```
docker-compose up
```


There a number of accounts already in the database. They have either standard, admin, or owner privileges. See table below for reference. Standard users can only see and manage their own files. Admins and owners can access the Admin area and manage standard users. Only the owner can elevate the privileges of a standard user to admin. Any user who registers is set to standard user by default. **The application currently only accepts sign-up with a ncirl.ie domain.** Passwords can be between 8 to 20 characters inclusive and must have and uppercase, lowercase, number and special character. Not all special characters will be accepted.

|#|Username|Email|Privilege|Password|
|-|--------|-----|---------|--------|
|1|Alice|alice@ncirl.ie|standard|P@ssword123|
|2|Bob|bob@ncirl.ie|owner|P@ssword123|
|3|Carla|carla@ncirl.ie|admin|P@ssword123|
|4|Dan|dan@ncirl.ie|standard|P@ssword123|
|5|Emma|emma@ncirl.ie|standard|P@ssword123|
|6|Fran|fran@ncirl.ie|standard|P@ssword123|
|7|Greg|greg@ncirl.ie|standard|P@ssword123|
|8|Helen|helen@ncirl.ie|standard|P@ssword123|