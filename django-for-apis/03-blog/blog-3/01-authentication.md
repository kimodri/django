The previous chapter is about authorization this chapter is about authentication and that is having the user create their account for us to authenticate them.

There are four built-in authentication options:
- basic
- session
- token 
- default

By the end of this we will have created API endpoints for sign up log in and log out

**How is this differen from permission?**
- Well someone can be permitted but not authenticated (they can access yes but it's not guaranteed if they are not authenticated)

## Basic Authentication
- When a client makes an HTTP request, it is forced to send an approved authentication credential before access is granted

The flow looks like this:
1. Client makes an HTTP request
2. Server responds with an HTTP response containing `401 (Unauthorized)` status code and `WWW-Authenticate` HTTP header with details on how to authorize 
3. Client sends credentials back via `Authorization` HTTP header
4. Server checks credentials and responds with either `200 OK` or `403 Forbidden` status code

Flow diagram:
![basic-auth](../../assets/basic-auth.jpeg)

- The authorization credentials sent are the unencrypted `base64` encoded version of `<username>:<password>`

## Session Authentication
- Monolithic websites, like traditional Django, have long used an alternative authentication scheme that is a combination of sessions and cookies. At a high level, the client authenticates with its credentials (username/password)and then receives a session ID from the server which is stored as a cookie. This session ID is then passed in the header of every future HTTP request.
- When the session ID is passed, the server uses it to look up a session object containing all avaialble information for a given user including credentials

### Not Secure
The session ID can be stolen. This is the exact concern you brought up, and it's a valid one. 


### Making Session Authentication More Secure

To mitigate these risks, developers use several techniques to protect the session ID:

* ...
* **IP Address and User-Agent Binding:** The server can check if the incoming requests' IP address and browser (user-agent) match the ones that were used when the session was created. If there's a mismatch, the session can be invalidated.

This is a **stateful** becayse a record must be kept and maintained on both the server (the session object) and the client the session ID

1. A user enters their log in credentials (typically username/password)
2. The server verifies the credentials are correct and generates a session object that is then stored in the database
3. The server sends the client a session ID—not the session object itself which is stored as a cookie on the browser
4. On all future requests the session ID is included as an HTTP header and, if verified by the database, the request proceeds
5. Once a user logs out of an application, the session ID is destroyed by both the client and server
6. If the user later logs in again, a new session ID is generated and stored as a cookie on the client

### There are several downsides however:
-  session ID is only valid within the browser where log in was performed; it will not work across multiple domains (Website vs mobile)
- Do not use this for any API that will have multiple front-ends

Imagine a company, "GadgetCo," with both a website and a native mobile app.

#### Scenario: The Problem of Shared Authentication

A user, Alex, logs into the GadgetCo **website** on their desktop browser. The server generates a unique **session ID** and sends it to the browser as a cookie. The browser stores this cookie and automatically includes it with every subsequent request to GadgetCo's server. This works perfectly. Alex can browse products and add items to their cart seamlessly.

Later, Alex opens the GadgetCo **mobile app** on their smartphone. To check out the items they added on the website, Alex expects to be logged in automatically, but they're not. They have to log in again.

This is because the session ID issued to the browser is a **cookie** tied to the specific domain (`gadgetco.com`). A native mobile app is a separate client; it's not a web browser and doesn't have access to the cookies stored by the browser. The session ID is not portable between these two different environments. The server has no way of knowing who Alex is when the mobile app sends a request because the app doesn't have the session ID from the browser.

The problem escalates for a public **API** that developers use to build third-party applications. If GadgetCo built their API to only accept session IDs from a web browser, it would be useless to any client that isn't a browser, like a smart TV app, a command-line tool, or a different company's software.

#### Why This Happens

Traditional session authentication is inherently tied to the web browser's cookie mechanism. The browser is responsible for storing the session ID and sending it with each request to the server. Other types of clients, like mobile apps, don't use this same mechanism.

This is why modern architectures often use **token-based authentication**, like **JSON Web Tokens (JWTs)**. A JWT can be sent in the header of an HTTP request, regardless of the client (browser, mobile app, etc.), making it a more flexible solution for a multi-platform environment.

## Token Authentication
- This is a stateless 
- Once the client sends the initial user credentials to the server a unique token is generated and then stored by the client as either a cookie or in local storage
- This token is passed in the header of each incoming HTTP and the server uses it to verify that a user is authenticated
- The server itself does not keep a record of the user just whether a token is valid or not

### Secutiry Issue
Tokens stored in both cookies and local storage are vulnerable to XSS attacks
- The best practice is to store tokens in a cookie with the `httpOnly` and `Secure` cookie flags

### Flow
The flow looks like this:
![token-auth](../../assets/token-auth.jpeg)

### Benefits
- Tokens can be shared thus can be used in more than one front ends

### Django and Token Auth
The DRF's built-in `TokenAuthentication` is deliberately quite basic:
- It does not support setting tokens to expire
- Also generates one token per user, so a user on a website and then later a mobile app will use the same token

## Default Authentication
Remember that the default authentication from DRF is the combination of basic and session and therefore to do that you need to get to `django_project/settings.py`

```python
# django_project/settings.py
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated", 
    ],

    "DEFAULT_AUTHENTICATION_CLASSES": [  # new
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}
```
Why use both?

DRF processes the `DEFAULT_AUTHENTICATION_CLASSES` list in a specific order:

> "REST framework will attempt to authenticate with each class in the list, and will set `request.user` and `request.auth` using the return value of the **first class that successfully authenticates**."

This is a key part of how DRF provides flexibility. The order of the classes in your `settings.py` file is what determines the priority.

When a request arrives at your API:

1.  DRF looks at the first class in the list, which is `SessionAuthentication`.
2.  It checks the request for a valid Django session cookie.
3.  **Scenario A (Browser User):** If a session cookie is found (because a user logged in via the Browsable API), `SessionAuthentication` succeeds. DRF sets the user and authentication info and stops. The rest of the list is ignored.
4.  **Scenario B (Non-Browser Client):** If no session cookie is found (because the request came from a mobile app, CLI tool, or another service), `SessionAuthentication` fails.
5.  DRF then moves to the next class in the list, `BasicAuthentication`.
6.  It checks the request for a `Basic` authentication header.
7.  **If a `Basic` header is found:** It attempts to authenticate the user with the provided credentials. If successful, the user is authenticated, and DRF stops.

This "first one wins" approach is what allows your API to handle multiple authentication schemes without any conflicts. It's not that `BasicAuthentication` works *with* `SessionAuthentication`, but rather that it works as a **backup** when `SessionAuthentication` isn't used. Your earlier understanding was perfectly correct; they are separate methods for different client types. The initial confusing statement you found was simply a very poor way of explaining this fallback mechanism.

## Implementing Token Auth

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated", # remember this is bad
    ],

    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
```
- We keep `SessionAuthentication` since we still need it for our brosable API 
- We also need to add the `authtoken` app which generates the tokens on the server
- Since we made changes to app we need to sync our database: `python manage.py migrate`
- After doing that you can see tokens in the admin page but it has nothing because However, the tokens are only generated *after* there is an API call for a user to log in.

Using both `SessionAuthentication` and `TokenAuthentication` in DRF works the same way as the previous example. DRF will check for each method in the listed order, using the first one that successfully authenticates the request.

---

### How it Works

1.  **Request Arrives:** A request comes into your API.
2.  **`SessionAuthentication` Check:** DRF first checks for a valid Django session cookie.
    * **If a session cookie is present and valid:** The request is authenticated. This is what happens when a **web browser user** is logged in to the Browsable API.
    * **If no session cookie is found or it is invalid:** DRF moves on to the next authentication class.
3.  **`TokenAuthentication` Check:** DRF then looks for a token in the `Authorization` header, which should be formatted as `Authorization: Token <token_string>`.
    * **If a token is found and is valid:** The request is authenticated. This is the method used by **external clients** like mobile apps or other services.
    * **If no token is found or it is invalid:** Authentication fails, and DRF will return an error (e.g., HTTP 401 Unauthorized).

### Why Use Both?

This configuration is very common and provides a versatile API for two distinct types of clients:

* **Browser-Based Clients (SessionAuthentication):** Developers and administrators can easily interact with the API using a standard web browser and the DRF Browsable API. They just log in, and the browser handles the rest. 
* **Headless Clients (TokenAuthentication):** Any application that is not a browser (mobile apps, IoT devices, scripts, etc.) can authenticate by including a single token in the header of each request. This is a secure and simple way for automated clients to access the API.

### What if I just use a Token Based?
If you use **only** `TokenAuthentication`, users will not be able to log in through the DRF Browsable API's web interface. Instead, they will need to use a separate API endpoint to get a token, which they will then have to manually include in every subsequent request.

-----

### Workflow for a Token-Only API

1.  **Obtain a Token:** A new user must first make a **POST** request to a specific login or token-obtaining endpoint on your API. This request will include their username and password in the body.
      * **Example Request:**
        ```
        POST /api/auth-token/
        Content-Type: application/json

        {
          "username": "johndoe",
          "password": "password123"
        }
        ```
2.  **Server Response:** The server will receive the credentials, validate them, and if they are correct, it will generate a unique token for that user. It then sends this token back in the response.
      * **Example Response:**
        ```
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
        }
        ```
3.  **Store the Token:** The client (e.g., a mobile app, a JavaScript frontend, a script) is responsible for storing this token securely. It could be in a browser's local storage, a mobile device's keychain, or a configuration file for a script.
4.  **Authenticated Requests:** For all future API calls to protected endpoints, the client must include this token in the `Authorization` header.
      * **Example Request:**
        ```
        GET /api/profile/ HTTP/1.1
        Host: api.example.com
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        ```
        If the token is missing or invalid, the API will reject the request with a `401 Unauthorized` error.

This process is ideal for **headless APIs** that serve non-browser clients, but it makes interacting with the API via a web browser less straightforward. It's why many DRF setups use both **SessionAuthentication** (for the developer-friendly Browsable API) and **TokenAuthentication** (for external clients) side-by-side.

