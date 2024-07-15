
### SQLAlchemy Concepts

#### 1. Declarative Base

**Definition**: The `declarative_base()` function creates a base class for defining models that automatically map to database tables.

**Example**:

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

#### 2. Model Declaration

**Definition**: Each model represents a table in the database. You define the table name using `__tablename__`, and define columns with types such as `Integer`, `String`, etc.

**Example**:

```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
```

#### 3. Relationships

**Definition**: Use `relationship()` to define relationships between models (e.g., one-to-many, many-to-many). Bidirectional relationships can be set using `back_populates`.

**Example**:

```python
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = 'users'
    # ... other fields ...
    posts = relationship("Post", back_populates="user")
```

#### 4. Lazy Loading

**Definition**: Using `lazy='dynamic'` allows relationships that may return many records to be filtered efficiently.

**Example**:

```python
class User(Base):
    __tablename__ = 'users'
    posts = relationship("Post", back_populates="user", lazy='dynamic')
```

#### 5. Creating Tables

**Definition**: Use `Base.metadata.create_all(engine)` to create tables based on the defined models in the database.

**Example**:

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///a.db", echo=True)
Base.metadata.create_all(engine)
```

### Tasks Overview

#### 0. User Model

**Task**: Create a `User` model for the `users` table.

**Implementation**:

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
```

#### 1. Create User

**Task**: Implement `add_user` method in the `DB` class.

**Implementation**:

```python
class DB:
    def add_user(self, user: User) -> None:
        self._session.add(user)
        self._session.commit()
```

**Example**:

```python
user = User(email='bob@bob.com', hashed_password='hashed_password')
db.add_user(user)
```

#### 2. Find User

**Task**: Implement `find_user_by` method.

**Implementation**:

```python
from sqlalchemy.exc import NoResultFound

class DB:
    def find_user_by(self, **kwargs):
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise ValueError("User not found")
```

**Example**:

```python
user = db.find_user_by(email='bob@bob.com')
```

#### 3. Update User

**Task**: Implement `update_user`.

**Implementation**:

```python
class DB:
    def update_user(self, user_id: int, **kwargs):
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()
```

**Example**:

```python
db.update_user(user.id, session_id='new_session_id')
```

#### 4. Hash Password

**Task**: Define `_hash_password` method.

**Implementation**:

```python
import bcrypt

def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
```

**Example**:

```python
hashed_password = _hash_password('myPassword')
```

#### 5. Register User

**Task**: Implement `Auth.register_user`.

**Implementation**:

```python
class Auth:
    def register_user(self, email: str, password: str) -> User:
        if self._db.find_user_by(email=email):
            raise ValueError("User already exists")
        hashed_password = _hash_password(password)
        new_user = User(email=email, hashed_password=hashed_password)
        self._db.add_user(new_user)
        return new_user
```

**Example**:

```python
try:
    user = auth.register_user(email='bob@bob.com', password='MySuperPwd')
except ValueError as err:
    print(f"could not create a new user: {err}")
```

#### 6. Basic Flask App

**Task**: Set up a basic Flask app.

**Implementation**:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the User Authentication Service!")
```

**Run the app**:

```bash
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### 7. User Registration Endpoint

**Task**: Create a POST `/users` route.

**Implementation**:

```python
@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify(email=user.email, message="user created"), 201
    except ValueError as err:
        return jsonify(message=str(err)), 400
```

#### 8. Credentials Validation

**Task**: Implement `Auth.valid_login`.

**Implementation**:

```python
class Auth:
    def valid_login(self, email: str, password: str) -> bool:
        user = self._db.find_user_by(email=email)
        return user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
```

**Example**:

```python
is_valid = auth.valid_login('bob@bob.com', 'MySuperPwd')
print(is_valid)  # True or False
```

### Exception Handling

**Task**: Handle exceptions effectively.

**Example**:

```python
from sqlalchemy.exc import NoResultFound, InvalidRequestError

try:
    user = db.find_user_by(email='unknown@bob.com')
except NoResultFound:
    print("User not found.")
except InvalidRequestError:
    print("Invalid query.")
```

### Flask Integration

**Task**: Import the `Auth` class and handle requests properly.

**Example**:

```python
from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
auth = Auth()

@app.route('/users', methods=['POST'])
def register_user():
    # Registration logic here
```

### Summary Table

| Task                      | Description                                          |
|---------------------------|------------------------------------------------------|
| User Model                | Defines user table with required fields              |
| Create User               | Adds a new user to the database                       |
| Find User                 | Retrieves a user by specific attributes               |
| Update User               | Updates user attributes in the database               |
| Hash Password             | Hashes a password using bcrypt                        |
| Register User             | Registers a new user and checks for duplicates        |
| Basic Flask App           | Sets up a basic Flask application                     |
| User Registration Endpoint | Creates a route to register new users                |
| Credentials Validation    | Validates user credentials during login              |

If you need further details on any specific task or concept, just let me know!



Sure! Here’s a breakdown of the user authentication service with explanations, separated into individual code sections for clarity.

### 1. **Setting Up the `auth.py` Module**

This module contains the core logic for user authentication.

#### **Code: `auth.py`**

```python
import uuid
import bcrypt
from sqlalchemy.exc import NoResultFound

class Auth:
    def __init__(self, db):
        self._db = db

    def _generate_uuid(self):
        """Generate a new UUID."""
        return str(uuid.uuid4())
```

#### **Explanation:**
- **`import uuid`**: Imports the `uuid` module to generate unique identifiers for users and sessions.
- **`import bcrypt`**: Imports the `bcrypt` library for hashing passwords securely.
- **`class Auth`**: Defines the `Auth` class that encapsulates authentication methods.
- **`__init__(self, db)`**: Initializes the class with a database connection.
- **`_generate_uuid(self)`**: A private method that generates and returns a new UUID as a string.

---

### 2. **Hashing Passwords**

#### **Code: Hashing Function**

```python
    def _hash_password(self, password: str) -> str:
        """Hash a password."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
```

#### **Explanation:**
- **`_hash_password(self, password: str)`**: This method takes a plaintext password, hashes it using bcrypt, and returns the hashed password as a string. It encodes the password to bytes and generates a salt to secure the hash.

---

### 3. **Creating a Session**

#### **Code: Create Session Method**

```python
    def create_session(self, email: str) -> str:
        """Create a session for a user."""
        user = self._db.find_user_by(email=email)
        if not user:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
```

#### **Explanation:**
- **`create_session(self, email: str)`**: This method retrieves a user by their email, generates a new session ID, updates the user's session ID in the database, and returns it. If no user is found, it returns `None`.

---

### 4. **Validating User Login**

#### **Code: Validate Login Method**

```python
    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials."""
        user = self._db.find_user_by(email=email)
        return user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
```

#### **Explanation:**
- **`valid_login(self, email: str, password: str)`**: This method checks if the user exists and if the provided password matches the stored hashed password using bcrypt. It returns `True` if valid; otherwise, `False`.

---

### 5. **Getting User by Session ID**

#### **Code: Get User from Session ID Method**

```python
    def get_user_from_session_id(self, session_id: str):
        """Get user by session ID."""
        if session_id is None:
            return None
        return self._db.find_user_by(session_id=session_id)
```

#### **Explanation:**
- **`get_user_from_session_id(self, session_id: str)`**: This method retrieves a user based on their session ID. If the session ID is `None`, it returns `None`.

---

### 6. **Destroying a Session**

#### **Code: Destroy Session Method**

```python
    def destroy_session(self, user_id: int):
        """Destroy user session."""
        self._db.update_user(user_id, session_id=None)
```

#### **Explanation:**
- **`destroy_session(self, user_id: int)`**: This method updates the user’s session ID in the database to `None`, effectively logging them out.

---

### 7. **Generating Reset Password Token**

#### **Code: Generate Reset Token Method**

```python
    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token."""
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError("User not found")
        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
```

#### **Explanation:**
- **`get_reset_password_token(self, email: str)`**: This method generates a reset token for a user and updates their record in the database. If the user does not exist, it raises a `ValueError`.

---

### 8. **Updating User Password**

#### **Code: Update Password Method**

```python
    def update_password(self, reset_token: str, password: str):
        """Update user password."""
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError("Invalid token")
        hashed_password = self._hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
```

#### **Explanation:**
- **`update_password(self, reset_token: str, password: str)`**: This method updates a user’s password using their reset token. It hashes the new password and sets the reset token to `None`. If the token is invalid, it raises a `ValueError`.

---

### 9. **Setting Up the `app.py` Module**

This module defines the Flask application and the routes for the authentication service.

#### **Code: `app.py`**

```python
from flask import Flask, jsonify, request, abort, redirect
from models import DB, User
from auth import Auth

app = Flask(__name__)
db = DB()  # Assume DB is properly initialized
auth = Auth(db)
```

#### **Explanation:**
- **`from flask import Flask, jsonify, request, abort, redirect`**: Imports necessary components from Flask to create the application and handle HTTP requests.
- **`db = DB()`**: Initializes the database connection.
- **`auth = Auth(db)`**: Creates an instance of the `Auth` class, passing the database connection.

---

### 10. **User Registration Route**

#### **Code: User Registration**

```python
@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify(email=user.email, message="User created"), 201
    except ValueError as err:
        return jsonify(message=str(err)), 400
```

#### **Explanation:**
- **`@app.route('/users', methods=['POST'])`**: Defines a route to register a new user.
- **`register_user()`**: Handles user registration. It calls `auth.register_user()` and returns a JSON response indicating success or failure.

---

### 11. **Login Route**

#### **Code: Login**

```python
@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify(email=email, message="Logged in")
    response.set_cookie('session_id', session_id)
    return response
```

#### **Explanation:**
- **`@app.route('/sessions', methods=['POST'])`**: Defines a route to log in a user.
- **`login()`**: Validates user credentials and creates a session. Sets the session ID in a cookie and returns a success message.

---

### 12. **Logout Route**

#### **Code: Logout**

```python
@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    auth.destroy_session(user.id)
    return redirect('/')
```

#### **Explanation:**
- **`@app.route('/sessions', methods=['DELETE'])`**: Defines a route to log out a user.
- **`logout()`**: Destroys the user session and redirects to the home page. If no user is found, it returns a 403 Forbidden status.

---

### 13. **Profile Route**

#### **Code: Profile**

```python
@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify(email=user.email)
```

#### **Explanation:**
- **`@app.route('/profile', methods=['GET'])`**: Defines a route to retrieve user profile information.
- **`profile()`**: Returns the user's email if the session ID is valid; otherwise, it returns a 403 Forbidden status.

---

### 14. **Reset Password Route (Token Generation)**

#### **Code: Reset Password Token Generation**

```python
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify(email=email, reset_token=reset_token)
    except ValueError:
        abort(403)
```

#### **Explanation:**
- **`@app.route('/reset_password', methods=['POST'])`**: Defines a route to generate a reset password token.
- **`reset_password()`**

: Generates a reset token and returns it if the email is valid; otherwise, returns a 403 Forbidden status.

---

### 15. **Update Password Route**

#### **Code: Update Password**

```python
@app.route('/reset_password', methods=['PUT'])
def update_password_endpoint():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        auth.update_password(reset_token, new_password)
        return jsonify(email=email, message="Password updated")
    except ValueError:
        abort(403)
```

#### **Explanation:**
- **`@app.route('/reset_password', methods=['PUT'])`**: Defines a route to update the user's password using the reset token.
- **`update_password_endpoint()`**: Calls the `update_password` method and returns a success message or a 403 Forbidden status if the token is invalid.

---

### 16. **Running the Application**

#### **Code: Run the Flask App**

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### **Explanation:**
- **`if __name__ == '__main__':`**: Ensures the app runs only when the script is executed directly.
- **`app.run(host='0.0.0.0', port=5000)`**: Starts the Flask application, making it accessible on all interfaces at port 5000.

---

### Example Usage

Here are examples of how to use the API:

1. **Register User**:
   ```bash
   curl -X POST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'
   ```

2. **Log In**:
   ```bash
   curl -X POST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd'
   ```

3. **Get Profile**:
   ```bash
   curl -X GET localhost:5000/profile --cookie "session_id=your_session_id"
   ```

4. **Reset Password**:
   ```bash
   curl -X POST localhost:5000/reset_password -d 'email=bob@bob.com'
   ```

5. **Update Password**:
   ```bash
   curl -X PUT localhost:5000/reset_password -d 'email=bob@bob.com' -d 'reset_token=your_token' -d 'new_password=newSuperPwd'
   ```

### Summary Table of API Endpoints

| Endpoint             | Method   | Description                                   |
|----------------------|----------|-----------------------------------------------|
| `/users`             | POST     | Register a new user                           |
| `/sessions`          | POST     | Log in a user and create a session           |
| `/sessions`          | DELETE   | Log out a user                                |
| `/profile`           | GET      | Retrieve user profile                          |
| `/reset_password`    | POST     | Generate a password reset token               |
| `/reset_password`    | PUT      | Update user password using the reset token    |

