### A Minimal Flask Application Explained

Let's break down a minimal Flask application step by step.

#### Code
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

#### Explanation

1. **Import Flask**: The first step is to import the `Flask` class from the `flask` module. This class will be the foundation of our web application.

    ```python
    from flask import Flask
    ```

2. **Create an Instance of the Flask Class**: We create an instance of the `Flask` class. This instance will be our WSGI (Web Server Gateway Interface) application.

    ```python
    app = Flask(__name__)
    ```

    - **`__name__`**: The first argument is the name of the application’s module or package. Using `__name__` is a common practice because it ensures Flask knows where to find resources like templates and static files.

3. **Define a Route**: We use the `route()` decorator to bind a URL to a function.

    ```python
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    ```

    - **`@app.route('/')`**: This decorator tells Flask that the `hello_world` function should be called when the root URL ("/") is accessed.
    - **Function**: The `hello_world` function returns the string "Hello, World!" which will be displayed in the user's browser.

#### Running the Application

1. **Save the Code**: Save the code in a file named `hello.py`.

2. **Set the FLASK_APP Environment Variable**: Before running the application, you need to set the `FLASK_APP` environment variable to the name of your file.

    - On macOS/Linux:
      ```bash
      export FLASK_APP=hello.py
      ```
    - On Windows (Command Prompt):
      ```cmd
      set FLASK_APP=hello.py
      ```
    - On Windows (PowerShell):
      ```powershell
      $env:FLASK_APP = "hello.py"
      ```

3. **Run the Application**: Use the `flask run` command to start the development server.

    ```bash
    flask run
    ```

    This will start a development server on `http://127.0.0.1:5000/`. When you visit this URL in your browser, you should see "Hello, World!".

#### Making the Server Externally Visible

By default, the server is only accessible from your own computer. To make it publicly accessible, use the `--host=0.0.0.0` option:

```bash
flask run --host=0.0.0.0
```

This command tells Flask to listen on all public IP addresses.

#### Debug Mode

For development, enabling debug mode is very useful. It allows the server to automatically reload on code changes and provides a debugger for errors.

1. **Set the FLASK_ENV Environment Variable**:

    - On macOS/Linux:
      ```bash
      export FLASK_ENV=development
      ```
    - On Windows (Command Prompt):
      ```cmd
      set FLASK_ENV=development
      ```
    - On Windows (PowerShell):
      ```powershell
      $env:FLASK_ENV = "development"
      ```

2. **Run the Application in Debug Mode**:

    ```bash
    flask run
    ```

    This enables the following:
    - The debugger is activated.
    - The automatic reloader is enabled.
    - Debug mode is enabled.

#### Common Issues

1. **Old Version of Flask**: If you're using a version of Flask older than 0.11, the `flask` command and `python -m flask` might not exist. Consider upgrading Flask.

2. **Invalid Import Name**: Ensure the `FLASK_APP` environment variable is set correctly to the name of your module.

3. **Debug Mode Security**: Never use debug mode in production as it allows the execution of arbitrary code, which poses a significant security risk.

#### Example Output

When you run the application and visit `http://127.0.0.1:5000/` in your browser, you should see:

```
Hello, World!
```

#### Screenshots and Debugger

When the debugger is triggered (e.g., due to an error), it provides a web-based interactive traceback. This can help you debug the issue directly from the browser. More details can be found in the [Werkzeug documentation](https://werkzeug.palletsprojects.com/en/2.1.x/debugger/).

For more information on running and deploying Flask applications, refer to the [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/).


### Routing in Flask

Flask allows you to create meaningful URLs for your web application, which makes it user-friendly and easy to navigate. Here's an in-depth look at routing and URL management in Flask.

#### Basic Routing

The `route()` decorator in Flask binds a function to a URL, allowing you to define how different URLs are handled.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World!'
```

- **`@app.route('/')

- **`@app.route('/')`**: This binds the `index` function to the root URL (`/`), which means when a user visits the root URL, they will see "Index Page".
- **`@app.route('/hello')`**: This binds the `hello` function to the `/hello` URL, displaying "Hello, World!" when visited.

#### Variable Rules

Flask allows dynamic URL building by using variable rules. These variables are passed as keyword arguments to your view functions.

```python
from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)
```

- **`<username>`**: This allows any text without a slash.
- **`<int:post_id>`**: This expects an integer.
- **`<path:subpath>`**: This allows a string with slashes.

**Example Outputs:**
- Visiting `/user/john` would return `User john`.
- Visiting `/post/123` would return `Post 123`.
- Visiting `/path/to/somewhere` would return `Subpath to/somewhere`.

#### Converter Types

Flask provides several built-in converters:
- `string`: Default, accepts any text without a slash.
- `int`: Accepts positive integers.
- `float`: Accepts positive floating-point values.
- `path`: Like `string` but also accepts slashes.
- `uuid`: Accepts UUID strings.

#### Unique URLs / Redirection Behavior

URLs can be designed with or without trailing slashes to control redirection behavior.

```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

- **`/projects/`**: Visiting `/projects` will redirect to `/projects/`.
- **`/about`**: Visiting `/about/` will produce a 404 error.

This helps maintain unique URLs and avoids duplicate content.

#### URL Building

The `url_for()` function is used to build URLs for a specific function, which helps in managing URLs efficiently.

```python
from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
```

**Example Outputs:**
- `url_for('index')` results in `/`.
- `url_for('login')` results in `/login`.
- `url_for('login', next='/')` results in `/login?next=/`.
- `url_for('profile', username='John Doe')` results in `/user/John%20Doe`.

#### HTTP Methods

Flask routes can handle different HTTP methods by specifying the `methods` argument in the `route()` decorator.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
```

- **`methods=['GET', 'POST']`**: This route can handle both GET and POST requests.

By default, Flask routes handle GET requests. If GET is present, Flask automatically adds support for the HEAD method and handles HEAD requests according to the HTTP RFC. OPTIONS is also automatically implemented.

### Summary

Flask's routing system is powerful and flexible, allowing you to create dynamic and meaningful URLs for your web application. The `route()` decorator, variable rules, URL building, and HTTP method handling make it easy to design and manage your application's URLs effectively.



### Static Files

Dynamic web applications often need to serve static files such as CSS and JavaScript. In Flask, you can easily serve these files during development by creating a folder named `static` in your project directory. Flask will serve files from this folder at the `/static` URL endpoint.

#### Example
To generate a URL for a static file, use the `url_for()` function with the special 'static' endpoint:

```python
url_for('static', filename='style.css')
```

If your CSS file is located at `static/style.css`, the above code will generate the URL `/static/style.css`.

### Rendering Templates

Generating HTML directly in Python can be cumbersome and insecure. Flask uses the Jinja2 template engine to make this process easier and more secure.

#### Rendering a Template

To render a template, use the `render_template()` function. You need to provide the name of the template file and any variables to pass to the template:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

Flask looks for templates in the `templates` folder. Depending on your project structure, this folder can be in different locations:

- **Case 1: Module Structure**
  ```
  /application.py
  /templates
      /hello.html
  ```

- **Case 2: Package Structure**
  ```
  /application
      /__init__.py
      /templates
          /hello.html
  ```

#### Example Template

Create a simple HTML template (`hello.html`) using Jinja2 syntax:

```html
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}
```

This template uses conditional statements to display different greetings based on whether the `name` variable is provided.

#### Template Features

- **Automatic Escaping**: Jinja2 automatically escapes HTML to prevent injection attacks. If you have trusted HTML, use the `Markup` class or the `|safe` filter to mark it as safe.

  ```python
  from markupsafe import Markup
  Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
  # Output: Markup(u'<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
  ```

- **Access to Flask Contexts**: Inside templates, you have access to Flask's `request`, `session`, `g` objects, and the `get_flashed_messages()` function.

- **Template Inheritance**: Jinja2 supports template inheritance, which allows you to define base templates that other templates can extend. This is useful for maintaining consistent layout elements like headers, navigation, and footers across multiple pages.

#### Example Using Markup Class

Here's an example of how to use the `Markup` class to safely handle HTML in Python:

```python
from markupsafe import Markup

# Example of escaping HTML
escaped_html = Markup.escape('<blink>hacker</blink>')
print(escaped_html)
# Output: Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')

# Example of stripping tags
clean_text = Markup('<em>Marked up</em> &raquo; HTML').striptags()
print(clean_text)
# Output: 'Marked up \xbb HTML'
```

### Summary

Flask makes it easy to manage static files and render dynamic HTML using templates. By using the `url_for()` function for static files and the `render_template()` function for templates, you can create a robust and secure web application with a clean and maintainable codebase. For more advanced templating features, refer to the [Jinja2 Template Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/).






### Accessing Request Data

In web applications, it's essential to handle data sent by clients to the server. Flask provides this information through the global `request` object. This might seem challenging in a threaded environment, but Flask uses context locals to manage it.

#### Context Locals

Flask's global objects are proxies to objects local to a specific context. This allows Flask to handle requests in a thread-safe manner. When a request starts, Flask binds the current application and WSGI environment to the active context (e.g., a thread).

For most cases, you don't need to worry about this. However, for unit testing, you may need to manually create and bind a request context. This can be done using `test_request_context()`.

##### Example:

```python
from flask import Flask, request

app = Flask(__name__)

with app.test_request_context('/hello', method='POST'):
    assert request.path == '/hello'
    assert request.method == 'POST'
```

Alternatively, you can use `request_context()` with a WSGI environment:

```python
from flask import Flask, request

app = Flask(__name__)
environ = {
    'REQUEST_METHOD': 'POST',
    'PATH_INFO': '/hello'
}

with app.request_context(environ):
    assert request.method == 'POST'
```

### The Request Object

The `request` object contains data related to the current HTTP request. You can import it from the `flask` module:

```python
from flask import request
```

#### Accessing Form Data

To access form data from a POST or PUT request, use the `form` attribute:

```python
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            return log_the_user_in(username)
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)
```

If a key doesn't exist in the `form` attribute, a `KeyError` is raised, resulting in an HTTP 400 error if not handled.

#### Accessing URL Parameters

To get parameters submitted in the URL (`?key=value`), use the `args` attribute:

```python
searchword = request.args.get('key', '')
```

Using `get()` is recommended to avoid `KeyError`.

#### File Uploads

To handle file uploads, set the `enctype="multipart/form-data"` attribute in your HTML form. Access uploaded files via the `files` attribute on the `request` object.

##### Example:

```python
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
```

Uploaded files can be saved to the server using the `save()` method. Always use `secure_filename()` to sanitize file names.

### Summary

Flask's `request` object and context locals allow you to handle client data efficiently and securely. Whether you're accessing form data, URL parameters, or file uploads, Flask provides simple and effective tools to manage these operations. For more details, refer to the [Flask Request Documentation](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request).


### Handling Cookies

#### Reading Cookies

Flask provides an easy way to access cookies sent by the client through the `cookies` attribute of the `request` object. The `request.cookies.get(key)` method fetches the value of a cookie by its key without raising a `KeyError` if the key doesn't exist.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    username = request.cookies.get('username')
    return f'Hello {username}' if username else 'Hello, Guest'

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- When a request is made to the root URL (`/`), the application checks for a cookie named `username`.
- If the cookie is present, it greets the user by their username. If not, it greets them as "Guest".

**Output:**
- If the client has a cookie `username` with the value "Alice", the output will be:
  ```
  Hello Alice
  ```
- If the cookie is not present, the output will be:
  ```
  Hello, Guest
  ```

#### Storing Cookies

To set cookies, use the `set_cookie` method on the response object. This is done by first creating a response object using `make_response`.

```python
from flask import Flask, make_response, render_template

app = Flask(__name__)

@app.route('/')
def index():
    resp = make_response('Setting a cookie')
    resp.set_cookie('username', 'Alice')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- The `make_response` function creates a response object with the string 'Setting a cookie'.
- The `set_cookie` method sets a cookie `username` with the value "Alice".
- The response object is then returned to the client, setting the cookie in the user's browser.

**Output:**
- The client will receive a response "Setting a cookie" and their browser will store a cookie `username` with the value "Alice".

### Redirects and Errors

#### Redirecting

To redirect users to a different endpoint, use the `redirect` function along with `url_for` to dynamically build the URL.

```python
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return 'This is the login page'

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- When a request is made to the root URL (`/`), the user is redirected to the `/login` endpoint.
- The `redirect` function creates a response that redirects the client to the URL generated by `url_for('login')`.

**Output:**
- Visiting `http://localhost:5000/` will redirect the user to `http://localhost:5000/login`, displaying:
  ```
  This is the login page
  ```

#### Aborting

To abort a request and return an HTTP error code, use the `abort` function.

```python
from flask import Flask, abort

app = Flask(__name__)

@app.route('/login')
def login():
    abort(401)  # Unauthorized access

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- When a request is made to the `/login` endpoint, the `abort(401)` function raises a 401 Unauthorized error.
- This immediately stops the request and returns an HTTP 401 response to the client.

**Output:**
- Visiting `http://localhost:5000/login` will display a default 401 Unauthorized error page.

#### Custom Error Pages

To customize error pages, use the `errorhandler` decorator.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
```

Create a template named `404.html` in the `templates` directory:

```html
<!-- templates/404.html -->
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Page Not Found</title>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>Sorry, the page you are looking for does not exist.</p>
</body>
</html>
```

**Explanation:**
- When a 404 error occurs, the `page_not_found` function renders the custom `404.html` template.
- The response status code is set to 404.

**Output:**
- Visiting a non-existent URL like `http://localhost:5000/nonexistent` will display the custom 404 page:
  ```
  404 - Page Not Found
  Sorry, the page you are looking for does not exist.
  ```

### About Responses

Flask automatically converts the return value from a view function into a response object. The conversion logic depends on the type of the return value.

#### Returning a String

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- Returning a string from a view function creates a response object with the string as the response body, a 200 OK status code, and a `text/html` MIME type.

**Output:**
- Visiting `http://localhost:5000/` will display:
  ```
  Hello, World!
  ```

#### Returning a Dictionary

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data')
def data():
    return {'name': 'Alice', 'age': 30}

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- Returning a dictionary from a view function automatically calls `jsonify` to create a JSON response.

**Output:**
- Visiting `http://localhost:5000/data` will display:
  ```json
  {
    "name": "Alice",
    "age": 30
  }
  ```

#### Returning a Tuple

```python
from flask import Flask

app = Flask(__name__)

@app.route('/tuple')
def tuple_response():
    return 'Hello, World!', 201, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- Returning a tuple allows you to specify the response body, status code, and headers.

**Output:**
- Visiting `http://localhost:5000/tuple` will display:
  ```
  Hello, World!
  ```
- The status code will be 201 Created and the `Content-Type` header will be `text/plain`.

### APIs with JSON

For APIs, returning a dictionary automatically creates a JSON response. For more control, use the `jsonify` function.

#### Example with Dictionary

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route("/me")
def me_api():
    user = {
        "username": "Alice",
        "theme": "light",
        "image": url_for("static", filename="images/profile.png")
    }
    return user

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- Returning a dictionary from the `me_api` function creates a JSON response with the user's details.

**Output:**
- Visiting `http://localhost:5000/me` will display:
  ```json
  {
    "username": "Alice",
    "theme": "light",
    "image": "/static/images/profile.png"
  }
  ```

#### Example with `jsonify()`

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users")
def users_api():
    users = [
        {"username": "Alice", "age": 30},
        {"username": "Bob", "age": 25}
    ]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- Using `jsonify` ensures the response is properly formatted as JSON.

**Output:**
- Visiting `http://localhost:5000/users` will display:
  ```json
  [
    {
      "username": "Alice",
      "age": 30
    },
    {
      "username": "Bob",
      "age": 25
    }
  ]
  ```

These examples cover reading and setting cookies, handling redirects and errors, understanding response types, and creating JSON APIs in Flask, with detailed explanations and expected outputs.



### Sessions in Flask

Sessions in Flask allow you to store information specific to a user across different requests. Sessions are implemented on top of cookies and are signed cryptographically to ensure data integrity. Here's how to use sessions:

#### Setting Up Sessions

To use sessions, you need to set a secret key, which is used for signing the cookies.

```python
from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- `app.secret_key`: This sets the secret key, which is necessary for session management.
- `session['username']`: Stores the username in the session.
- `session.pop('username', None)`: Removes the username from the session.

**Output:**
- Visiting `http://localhost:5000/` will display:
  ```
  You are not logged in
  ```
- After logging in through `http://localhost:5000/login` with a username, it will display:
  ```
  Logged in as <username>
  ```
- Logging out will redirect back to `http://localhost:5000/` and display:
  ```
  You are not logged in
  ```

#### Generating Secret Keys

Use the following command to generate a random secret key:

```bash
$ python -c 'import os; print(os.urandom(16))'
```

Example output:
```
b'_5#y2L"F4Q8z\n\xec]/'
```

### Message Flashing

Flask provides a simple way to give feedback to users using message flashing. Flash messages are stored in the session and displayed on the next request.

```python
from flask import Flask, flash, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flash')
def flash_message():
    flash('This is a flash message!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

Create a template named `index.html`:

```html
<!-- templates/index.html -->
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Flash Messages</title>
</head>
<body>
    <h1>Home Page</h1>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
</body>
</html>
```

**Explanation:**
- `flash('This is a flash message!')`: Records a flash message.
- `get_flashed_messages()`: Retrieves and displays flash messages.

**Output:**
- Visiting `http://localhost:5000/flash` will flash a message and redirect to the home page, displaying:
  ```
  - This is a flash message!
  ```

### Logging

Flask comes with a preconfigured logger that you can use for logging messages at various levels.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.debug('This is a debug message')
    app.logger.warning('This is a warning')
    app.logger.error('This is an error')
    return 'Check your console for logged messages.'

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation:**
- `app.logger.debug('message')`: Logs a debug message.
- `app.logger.warning('message')`: Logs a warning message.
- `app.logger.error('message')`: Logs an error message.

**Output:**
- Visiting `http://localhost:5000/` will log messages to the console:
  ```
  * Debug: This is a debug message
  * Warning: This is a warning
  * Error: This is an error
  ```

### Using Flask Extensions

Flask extensions provide additional functionality to your Flask applications. For example, Flask-SQLAlchemy integrates SQLAlchemy with Flask.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

**Explanation:**
- `app.config['SQLALCHEMY_DATABASE_URI']`: Sets the database URI.
- `db.create_all()`: Creates the database tables.

**Output:**
- Running the application will create a SQLite database `test.db` with a `User` table.

### Deploying to a Web Server

When you're ready to deploy your Flask app, refer to the [Deployment Options](https://flask.palletsprojects.com/en/2.0.x/deploying/) in the Flask documentation for detailed instructions on deploying to various environments, such as Gunicorn, Nginx, and others.
