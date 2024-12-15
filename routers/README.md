# Routers

### 1.1 Overview
There are 3 routers in the application.

1. `auth.py` respgitonsible for:
    - Login.
    - User account creation. Here, password complexity will be enforced and the domain used for the email will be restricted.
    - Session cookie creation and distribution. This uses Json Web Tokens to create the cookie. The secret and algorithm for which is stored in the `.env` file. Attributes for the cookie are also set in this file.
    - Logout and removal of the session cookie.

2. `audio_files.py` responsible for:
    - Authorising access to audio files.
    - Files will displayed only if the user sends the jwt token to the server
3. `admin.py` responsible for:
    - Authorising access to the admin area. Only owners and admin are allowed to view this area and they can both delete users.
    - Authorising access to a edit a user's account info.
    - Authorising update of a user's permissions. Only owners are allowed to perform this action.

