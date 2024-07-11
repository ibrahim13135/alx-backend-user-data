## Understanding Basic Authentication in Flask with Flask-HTTPAuth

### Overview

Authentication is a mechanism to verify the identity of a user or process. Basic Authentication involves sending a username and password with each request to a server. This guide covers how to implement Basic Authentication in Flask using the `Flask-HTTPAuth` extension.


### `@app.errorhandler`

The `@app.errorhandler` decorator in Flask allows you to specify a custom error handler for a particular HTTP status code.

#### Example

Let's create custom error handlers for 401 (Unauthorized) and 403 (Forbidden) status codes.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403

@app.route('/unauthorized')
def trigger_unauthorized():
    abort(401)

@app.route('/forbidden')
def trigger_forbidden():
    abort(403)

if __name__ == "__main__":
    app.run(debug=True)
```

#### Output

1. **Accessing `/unauthorized`:**

   ```sh
   curl http://127.0.0.1:5000/unauthorized
   ```

   ```json
   {
     "error": "Unauthorized"
   }
   ```

   Status code: `401 Unauthorized`

2. **Accessing `/forbidden`:**

   ```sh
   curl http://127.0.0.1:5000/forbidden
   ```

   ```json
   {
     "error": "Forbidden"
   }
   ```

   Status code: `403 Forbidden`

### `@app.before_request`

The `@app.before_request` decorator is used to register a function to run before each request. This is useful for tasks like checking authentication before handling a request.

#### Example

Let's use `@app.before_request` to require an authentication token for certain routes.

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.before_request
def require_auth():
    if request.endpoint != 'public' and not request.headers.get("Authorization"):
        abort(401)

@app.route('/public')
def public():
    return jsonify({"message": "This is a public endpoint."})

@app.route('/private')
def private():
    return jsonify({"message": "This is a private endpoint."})

if __name__ == "__main__":
    app.run(debug=True)
```

#### Output

1. **Accessing `/public`:**

   ```sh
   curl http://127.0.0.1:5000/public
   ```

   ```json
   {
     "message": "This is a public endpoint."
   }
   ```

2. **Accessing `/private` without Authorization header:**

   ```sh
   curl http://127.0.0.1:5000/private
   ```

   ```json
   {
     "error": "Unauthorized"
   }
   ```

   Status code: `401 Unauthorized`

3. **Accessing `/private` with Authorization header:**

   ```sh
   curl -H "Authorization: Bearer token" http://127.0.0.1:5000/private
   ```

   ```json
   {
     "message": "This is a private endpoint."
   }
   ```

### `require_auth`, `authorization_header`, and `current_user`

These methods are often used in the context of custom authentication implementations.

#### `require_auth`

This function checks whether a request requires authentication based on the requested endpoint.

#### `authorization_header`

This function retrieves the `Authorization` header from the request, typically to extract a token.

#### `current_user`

This function extracts and returns the current authenticated user based on the token provided.

#### Example

Let's implement these methods and integrate them with `@app.before_request`.

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

def require_auth():
    if request.endpoint != 'public' and not authorization_header():
        abort(401)

def authorization_header():
    return request.headers.get("Authorization")

def current_user():
    token = authorization_header()
    # Dummy implementation: In reality, you would decode the token and verify the user
    if token == "Bearer valid_token":
        return {"username": "valid_user"}
    return None

@app.before_request
def before_request():
    require_auth()

@app.route('/public')
def public():
    return jsonify({"message": "This is a public endpoint."})

@app.route('/private')
def private():
    user = current_user()
    if not user:
        abort(403)
    return jsonify({"message": f"Hello, {user['username']}!"})

if __name__ == "__main__":
    app.run(debug=True)
```

#### Output

1. **Accessing `/public`:**

   ```sh
   curl http://127.0.0.1:5000/public
   ```

   ```json
   {
     "message": "This is a public endpoint."
   }
   ```

2. **Accessing `/private` without Authorization header:**

   ```sh
   curl http://127.0.0.1:5000/private
   ```

   ```json
   {
     "error": "Unauthorized"
   }
   ```

   Status code: `401 Unauthorized`

3. **Accessing `/private` with invalid token:**

   ```sh
   curl -H "Authorization: Bearer invalid_token" http://127.0.0.1:5000/private
   ```

   ```json
   {
     "error": "Forbidden"
   }
   ```

   Status code: `403 Forbidden`

4. **Accessing `/private` with valid token:**

   ```sh
   curl -H "Authorization: Bearer valid_token" http://127.0.0.1:5000/private
   ```

   ```json
   {
     "message": "Hello, valid_user!"
   }
   ```

These examples demonstrate how to use `@app.errorhandler` for custom error handling and how to implement authentication checks using `@app.before_request` along with helper functions like `require_auth`, `authorization_header`, and `current_user`.

### Basic Authentication Example

Here's a step-by-step example of implementing Basic Authentication in Flask:

1. **Setup Flask and Flask-HTTPAuth**:
    ```python
    from flask import Flask
    from flask_httpauth import HTTPBasicAuth
    from werkzeug.security import generate_password_hash, check_password_hash

    app = Flask(__name__)
    auth = HTTPBasicAuth()
    ```

2. **Define Users**:
    Create a dictionary to store usernames and their hashed passwords:
    ```python
    users = {
        "john": generate_password_hash("hello"),
        "susan": generate_password_hash("bye")
    }
    ```

3. **Verify Password**:
    Define a function to verify the username and password:
    ```python
    @auth.verify_password
    def verify_password(username, password):
        if username in users and check_password_hash(users.get(username), password):
            return username
    ```

4. **Protect Routes**:
    Use the `@auth.login_required` decorator to protect routes:
    ```python
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.current_user())
    ```

5. **Run the App**:
    ```python
    if __name__ == '__main__':
        app.run()
    ```

### Complete Basic Authentication Example

Here is the complete code with explanations:

```python
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Create a dictionary to store usernames and their hashed passwords
users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

# Define a function to verify the username and password
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Protect the route with basic authentication
@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

# Run the Flask app
if __name__ == '__main__':
    app.run()
```

### Output

- When you run this app and access the root URL (`/`), you will be prompted for a username and password.
- Entering the correct credentials (e.g., `john` and `hello`) will display "Hello, john!".

### Explanation

1. **Setup**:
   - `Flask`: The main framework.
   - `HTTPBasicAuth`: The extension for handling Basic Authentication.
   - `generate_password_hash` and `check_password_hash`: Functions from `werkzeug.security` to hash and verify passwords.

2. **Users Dictionary**:
   - Stores usernames as keys and hashed passwords as values.

3. **verify_password Function**:
   - Checks if the provided username exists and verifies the password using `check_password_hash`.

4. **Protected Route**:
   - The `index` route is protected by the `@auth.login_required` decorator, ensuring only authenticated users can access it.

### Digest Authentication Example

Digest Authentication is more secure than Basic Authentication. Here's an example:

1. **Setup Flask and HTTPDigestAuth**:
    ```python
    from flask import Flask
    from flask_httpauth import HTTPDigestAuth

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key here'
    auth = HTTPDigestAuth()
    ```

2. **Define Users**:
    Create a dictionary to store usernames and passwords:
    ```python
    users = {
        "john": "hello",
        "susan": "bye"
    }
    ```

3. **Get Password**:
    Define a function to get the password for a given username:
    ```python
    @auth.get_password
    def get_pw(username):
        if username in users:
            return users.get(username)
        return None
    ```

4. **Protect Routes**:
    Use the `@auth.login_required` decorator to protect routes:
    ```python
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.username())
    ```

5. **Run the App**:
    ```python
    if __name__ == '__main__':
        app.run()
    ```

### Complete Digest Authentication Example

Here is the complete code:

```python
from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.username())

if __name__ == '__main__':
    app.run()
```

### Token Authentication Example

Token Authentication is commonly used for API authentication. Here’s an example:

1. **Setup Flask and HTTPTokenAuth**:
    ```python
    from flask import Flask
    from flask_httpauth import HTTPTokenAuth

    app = Flask(__name__)
    auth = HTTPTokenAuth(scheme='Bearer')
    ```

2. **Define Tokens**:
    Create a dictionary to store tokens and their associated users:
    ```python
    tokens = {
        "secret-token-1": "john",
        "secret-token-2": "susan"
    }
    ```

3. **Verify Token**:
    Define a function to verify the token:
    ```python
    @auth.verify_token
    def verify_token(token):
        if token in tokens:
            return tokens[token]
    ```

4. **Protect Routes**:
    Use the `@auth.login_required` decorator to protect routes:
    ```python
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.current_user())
    ```

5. **Run the App**:
    ```python
    if __name__ == '__main__':
        app.run()
    ```

### Complete Token Authentication Example

Here is the complete code:

```python
from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()
```

### Explanation

- **Setup**:
  - `HTTPTokenAuth`: The extension for handling token-based authentication. The `scheme` argument defines the authentication scheme (e.g., `Bearer`).

- **Tokens Dictionary**:
  - Stores tokens as keys and associated usernames as values.

- **verify_token Function**:
  - Checks if the provided token exists in the `tokens` dictionary and returns the associated username.

- **Protected Route**:
  - The `index` route is protected by the `@auth.login_required` decorator, ensuring only authenticated users can access it.

### Conclusion

By following these examples, you can implement Basic, Digest, and Token authentication in your Flask applications using `Flask-HTTPAuth`. This provides a foundational understanding of authentication mechanisms and their implementation in Flask.




## Understanding Basic Authentication in Flask with Flask-HTTPAuth

### Overview

Authentication is a mechanism to verify the identity of a user or process. Basic Authentication involves sending a username and password with each request to a server. This guide covers how to implement Basic Authentication in Flask using the `Flask-HTTPAuth` extension.

### Basic Authentication Example

Here's a step-by-step example of implementing Basic Authentication in Flask:

1. **Setup Flask and Flask-HTTPAuth**:
    ```python
    from flask import Flask
    from flask_httpauth import HTTPBasicAuth
    from werkzeug.security import generate_password_hash, check_password_hash

    app = Flask(__name__)
    auth = HTTPBasicAuth()
    ```

2. **Define Users**:
    Create a dictionary to store usernames and their hashed passwords:
    ```python
    users = {
        "john": generate_password_hash("hello"),
        "susan": generate_password_hash("bye")
    }
    ```

3. **Verify Password**:
    Define a function to verify the username and password:
    ```python
    @auth.verify_password
    def verify_password(username, password):
        if username in users and check_password_hash(users.get(username), password):
            return username
    ```

4. **Protect Routes**:
    Use the `@auth.login_required` decorator to protect routes:
    ```python
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.current_user())
    ```

5. **Run the App**:
    ```python
    if __name__ == '__main__':
        app.run()
    ```

### Complete Basic Authentication Example

Here is the complete code with explanations:

```python
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Create a dictionary to store usernames and their hashed passwords
users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

# Define a function to verify the username and password
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Protect the route with basic authentication
@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

# Run the Flask app
if __name__ == '__main__':
    app.run()
```

### Output

- When you run this app and access the root URL (`/`), you will be prompted for a username and password.
- Entering the correct credentials (e.g., `john` and `hello`) will display "Hello, john!".

### Explanation

1. **Setup**:
   - `Flask`: The main framework.
   - `HTTPBasicAuth`: The extension for handling Basic Authentication.
   - `generate_password_hash` and `check_password_hash`: Functions from `werkzeug.security` to hash and verify passwords.

2. **Users Dictionary**:
   - Stores usernames as keys and hashed passwords as values.

3. **verify_password Function**:
   - Checks if the provided username exists and verifies the password using `check_password_hash`.

4. **Protected Route**:
   - The `index` route is protected by the `@auth.login_required` decorator, ensuring only authenticated users can access it.

### Digest Authentication Example

Digest Authentication is more secure than Basic Authentication. Here's an example:

1. **Setup Flask and HTTPDigestAuth**:
    ```python
    from flask import Flask
    from flask_httpauth import HTTPDigestAuth

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key here'
    auth = HTTPDigestAuth()
    ```

2. **Define Users**:
    Create a dictionary to store usernames and passwords:
    ```python
    users = {
        "john": "hello",
        "susan": "bye"
    }
    ```

3. **Get Password**:
    Define a function to get the password for a given username:
    ```python
    @auth.get_password
    def get_pw(username):
        if username in users:
            return users.get(username)
        return None
    ```

4. **Protect Routes**:
    Use the `@auth.login_required` decorator to protect routes:
    ```python
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.username())
    ```

5. **Run the App**:
    ```python
    if __name__ == '__main__':
        app.run()
    ```

### Complete Digest Authentication Example

Here is the complete code:

```python
from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.username())

if __name__ == '__main__':
    app.run()
```

### Token Authentication Example

Token Authentication is commonly used for API authentication. Here’s an example:

1. **Setup Flask and HTTPTokenAuth**:
    ```python
    from flask import Flask
    from flask_httpauth import HTTPTokenAuth

    app = Flask(__name__)
    auth = HTTPTokenAuth(scheme='Bearer')
    ```

2. **Define Tokens**:
    Create a dictionary to store tokens and their associated users:
    ```python
    tokens = {
        "secret-token-1": "john",
        "secret-token-2": "susan"
    }
    ```

3. **Verify Token**:
    Define a function to verify the token:
    ```python
    @auth.verify_token
    def verify_token(token):
        if token in tokens:
            return tokens[token]
    ```

4. **Protect Routes**:
    Use the `@auth.login_required` decorator to protect routes:
    ```python
    @app.route('/')
    @auth.login_required
    def index():
        return "Hello, {}!".format(auth.current_user())
    ```

5. **Run the App**:
    ```python
    if __name__ == '__main__':
        app.run()
    ```

### Complete Token Authentication Example

Here is the complete code:

```python
from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()
```

### Explanation

- **Setup**:
  - `HTTPTokenAuth`: The extension for handling token-based authentication. The `scheme` argument defines the authentication scheme (e.g., `Bearer`).

- **Tokens Dictionary**:
  - Stores tokens as keys and associated usernames as values.

- **verify_token Function**:
  - Checks if the provided token exists in the `tokens` dictionary and returns the associated username.

- **Protected Route**:
  - The `index` route is protected by the `@auth.login_required` decorator, ensuring only authenticated users can access it.

### Conclusion

By following these examples, you can implement Basic, Digest, and Token authentication in your Flask applications using `Flask-HTTPAuth`. This provides a foundational understanding of authentication mechanisms and their implementation in Flask.







### `@app.errorhandler`

The `@app.errorhandler` decorator in Flask allows you to specify a custom error handler for a particular HTTP status code.

#### Example

Let's create custom error handlers for 401 (Unauthorized) and 403 (Forbidden) status codes.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403

@app.route('/unauthorized')
def trigger_unauthorized():
    abort(401)

@app.route('/forbidden')
def trigger_forbidden():
    abort(403)

if __name__ == "__main__":
    app.run(debug=True)
```

#### Output

1. **Accessing `/unauthorized`:**

   ```sh
   curl http://127.0.0.1:5000/unauthorized
   ```

   ```json
   {
     "error": "Unauthorized"
   }
   ```

   Status code: `401 Unauthorized`

2. **Accessing `/forbidden`:**

   ```sh
   curl http://127.0.0.1:5000/forbidden
   ```

   ```json
   {
     "error": "Forbidden"
   }
   ```

   Status code: `403 Forbidden`

### `@app.before_request`

The `@app.before_request` decorator is used to register a function to run before each request. This is useful for tasks like checking authentication before handling a request.

#### Example

Let's use `@app.before_request` to require an authentication token for certain routes.

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.before_request
def require_auth():
    if request.endpoint != 'public' and not request.headers.get("Authorization"):
        abort(401)

@app.route('/public')
def public():
    return jsonify({"message": "This is a public endpoint."})

@app.route('/private')
def private():
    return jsonify({"message": "This is a private endpoint."})

if __name__ == "__main__":
    app.run(debug=True)
```

#### Output

1. **Accessing `/public`:**

   ```sh
   curl http://127.0.0.1:5000/public
   ```

   ```json
   {
     "message": "This is a public endpoint."
   }
   ```

2. **Accessing `/private` without Authorization header:**

   ```sh
   curl http://127.0.0.1:5000/private
   ```

   ```json
   {
     "error": "Unauthorized"
   }
   ```

   Status code: `401 Unauthorized`

3. **Accessing `/private` with Authorization header:**

   ```sh
   curl -H "Authorization: Bearer token" http://127.0.0.1:5000/private
   ```

   ```json
   {
     "message": "This is a private endpoint."
   }
   ```

### `require_auth`, `authorization_header`, and `current_user`

These methods are often used in the context of custom authentication implementations.

#### `require_auth`

This function checks whether a request requires authentication based on the requested endpoint.

#### `authorization_header`

This function retrieves the `Authorization` header from the request, typically to extract a token.

#### `current_user`

This function extracts and returns the current authenticated user based on the token provided.

#### Example

Let's implement these methods and integrate them with `@app.before_request`.

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

def require_auth():
    if request.endpoint != 'public' and not authorization_header():
        abort(401)

def authorization_header():
    return request.headers.get("Authorization")

def current_user():
    token = authorization_header()
    # Dummy implementation: In reality, you would decode the token and verify the user
    if token == "Bearer valid_token":
        return {"username": "valid_user"}
    return None

@app.before_request
def before_request():
    require_auth()

@app.route('/public')
def public():
    return jsonify({"message": "This is a public endpoint."})

@app.route('/private')
def private():
    user = current_user()
    if not user:
        abort(403)
    return jsonify({"message": f"Hello, {user['username']}!"})

if __name__ == "__main__":
    app.run(debug=True)
```

#### Output

1. **Accessing `/public`:**

   ```sh
   curl http://127.0.0.1:5000/public
   ```

   ```json
   {
     "message": "This is a public endpoint."
   }
   ```

2. **Accessing `/private` without Authorization header:**

   ```sh
   curl http://127.0.0.1:5000/private
   ```

   ```json
   {
     "error": "Unauthorized"
   }
   ```

   Status code: `401 Unauthorized`

3. **Accessing `/private` with invalid token:**

   ```sh
   curl -H "Authorization: Bearer invalid_token" http://127.0.0.1:5000/private
   ```

   ```json
   {
     "error": "Forbidden"
   }
   ```

   Status code: `403 Forbidden`

4. **Accessing `/private` with valid token:**

   ```sh
   curl -H "Authorization: Bearer valid_token" http://127.0.0.1:5000/private
   ```

   ```json
   {
     "message": "Hello, valid_user!"
   }
   ```

These examples demonstrate how to use `@app.errorhandler` for custom error handling and how to implement authentication checks using `@app.before_request` along with helper functions like `require_auth`, `authorization_header`, and `current_user`.
