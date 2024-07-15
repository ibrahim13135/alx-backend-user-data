### Quickstart with Requests Library

The Requests library is a simple and elegant HTTP library for Python, built for human beings. Here's a quickstart guide to get you up and running with some basic functionalities of the Requests library.

#### Installation

Make sure that Requests is installed and up-to-date. You can install it using pip:

```bash
$ pip install requests
```

#### Making a Request

To make an HTTP request, you start by importing the Requests module:

```python
import requests
```

Let's make a GET request to GitHub’s public timeline:

```python
r = requests.get('https://api.github.com/events')
```

This `r` object is a `Response` object that contains all the information returned by the server.

#### HTTP Methods

Requests’ simple API makes all forms of HTTP requests straightforward. Here are examples for each HTTP method:

```python
# GET request
r = requests.get('https://api.github.com/events')

# POST request
r = requests.post('https://httpbin.org/post', data={'key': 'value'})

# PUT request
r = requests.put('https://httpbin.org/put', data={'key': 'value'})

# DELETE request
r = requests.delete('https://httpbin.org/delete')

# HEAD request
r = requests.head('https://httpbin.org/get')

# OPTIONS request
r = requests.options('https://httpbin.org/get')
```

#### Passing Parameters in URLs

You can pass parameters in the URL’s query string by providing a dictionary to the `params` keyword argument.

```python
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)
```

**Output:**
```
https://httpbin.org/get?key2=value2&key1=value1
```

You can also pass a list of items as a value:

```python
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)
```

**Output:**
```
https://httpbin.org/get?key1=value1&key2=value2&key2=value3
```

#### Response Content

You can read the content of the server’s response. For example, let's consider the GitHub timeline:

```python
import requests

r = requests.get('https://api.github.com/events')
print(r.text)
```

**Output:**
```json
'[{"repository":{"open_issues":0,"url":"https://github.com/...
```

#### Handling Response Encoding

Requests automatically decodes content from the server based on the HTTP headers. You can check and change the encoding used by Requests:

```python
print(r.encoding)  # Default encoding
r.encoding = 'ISO-8859-1'  # Changing the encoding
```

If you need to handle custom encodings, register it with the `codecs` module and set `r.encoding` to your custom codec name.

#### Example Code

Here's a complete example to demonstrate these functionalities:

```python
import requests

# GET request
response = requests.get('https://api.github.com/events')
print("GET Request URL:", response.url)
print("Response Text:", response.text[:200])  # Printing first 200 chars

# POST request
response = requests.post('https://httpbin.org/post', data={'key': 'value'})
print("POST Request URL:", response.url)
print("Response Text:", response.text[:200])  # Printing first 200 chars

# Passing parameters in URLs
payload = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://httpbin.org/get', params=payload)
print("GET Request with Params URL:", response.url)
print("Response Text:", response.text[:200])  # Printing first 200 chars

# Handling response encoding
response.encoding = 'ISO-8859-1'
print("Changed Encoding:", response.encoding)
print("Response Text with Changed Encoding:", response.text[:200])  # Printing first 200 chars
```

**Output:**
```
GET Request URL: https://api.github.com/events
Response Text: [{"id":"1234567890","type":"PushEvent","actor":{"id":1234567,"login":"username",...

POST Request URL: https://httpbin.org/post
Response Text: {
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "key": "value"
  },
  "headers": ...

GET Request with Params URL: https://httpbin.org/get?key2=value2&key1=value1
Response Text: {
  "args": {
    "key1": "value1",
    "key2": "value2"
  },
  "headers": ...

Changed Encoding: ISO-8859-1
Response Text with Changed Encoding: [{"id":"1234567890","type":"PushEvent","actor":{"id":1234567,"login":"username",...
```

This example covers basic usage of the Requests library, including making different types of requests, passing parameters, handling response content, and managing encodings.



### Advanced Usage of the Requests Library

The Requests library in Python makes it easy to send HTTP requests and handle the responses. Here are some advanced functionalities, including handling binary and JSON responses, streaming content, and customizing headers.

#### Binary Response Content

You can access the response body as bytes for non-text requests using `r.content`. This is useful when dealing with binary data such as images.

```python
import requests
from PIL import Image
from io import BytesIO

r = requests.get('https://api.github.com/events')
print(r.content[:100])  # Printing the first 100 bytes of the response

# Create an image from the binary data
i = Image.open(BytesIO(r.content))
i.show()
```

**Output:**
```
b'[{"repository":{"open_issues":0,"url":"https://github.com/...
```

#### JSON Response Content

Requests has a built-in JSON decoder for handling JSON data:

```python
import requests

r = requests.get('https://api.github.com/events')
print(r.json()[:1])  # Printing the first element of the JSON response
```

**Output:**
```json
[{'repository': {'open_issues': 0, 'url': 'https://github.com/...'}}]
```

To ensure that the response was successful and handle JSON decoding errors, you can use `r.raise_for_status()` and handle exceptions:

```python
try:
    r.raise_for_status()
    data = r.json()
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except requests.exceptions.JSONDecodeError as json_err:
    print(f'JSON decode error occurred: {json_err}')
else:
    print(data[:1])
```

#### Raw Response Content

For raw socket responses, set `stream=True` in your initial request:

```python
r = requests.get('https://api.github.com/events', stream=True)
print(r.raw)  # Output the raw HTTP response object
print(r.raw.read(10))  # Read the first 10 bytes
```

**Output:**
```
<urllib3.response.HTTPResponse object at 0x101194810>
b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'
```

To save streamed content to a file:

```python
with open('output.bin', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
```

#### Custom Headers

To add custom HTTP headers to a request, pass a dictionary to the `headers` parameter:

```python
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}

r = requests.get(url, headers=headers)
print(r.request.headers)
```

**Output:**
```
{
    'User-Agent': 'my-app/0.0.1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}
```

### Example Code

Here's a complete example demonstrating these advanced features:

```python
import requests
from PIL import Image
from io import BytesIO

# Binary response content
r = requests.get('https://api.github.com/events')
print("Binary Content:", r.content[:100])

# Create an image from binary data
i = Image.open(BytesIO(r.content))
i.show()

# JSON response content
try:
    r.raise_for_status()
    data = r.json()
    print("JSON Content:", data[:1])
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except requests.exceptions.JSONDecodeError as json_err:
    print(f'JSON decode error occurred: {json_err}')

# Raw response content with streaming
r = requests.get('https://api.github.com/events', stream=True)
print("Raw HTTP Response Object:", r.raw)
print("First 10 Bytes of Raw Response:", r.raw.read(10))

# Save streamed content to a file
with open('output.bin', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

# Custom headers
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
print("Request Headers:", r.request.headers)
```

### Notes
- **Binary Content Handling**: When dealing with non-text data, such as images, accessing the response body as bytes is essential.
- **JSON Handling**: The built-in JSON decoder simplifies working with JSON responses, and error handling ensures robustness.
- **Raw Content and Streaming**: For large responses, streaming content and saving it in chunks helps manage memory usage efficiently.
- **Custom Headers**: Adding custom headers allows you to specify additional information in your requests, such as user-agent strings or authentication tokens.

This example showcases advanced usage of the Requests library, covering various scenarios you might encounter when working with HTTP requests and responses.


### Advanced Usage of POST Requests with the Requests Library

The Requests library in Python simplifies sending HTTP POST requests with various types of data. Here's how to handle more complicated POST requests, including form-encoded data, JSON data, and multipart file uploads.

#### Sending Form-Encoded Data

To send form-encoded data, pass a dictionary to the `data` argument. The data will automatically be form-encoded.

```python
import requests

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post('https://httpbin.org/post', data=payload)
print(r.text)
```

**Output:**
```json
{
  ...
  "form": {
    "key2": "value2",
    "key1": "value1"
  },
  ...
}
```

#### Multiple Values for Each Key

If a form has multiple elements with the same key, you can use a list of tuples or a dictionary with lists as values.

```python
payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
r1 = requests.post('https://httpbin.org/post', data=payload_tuples)

payload_dict = {'key1': ['value1', 'value2']}
r2 = requests.post('https://httpbin.org/post', data=payload_dict)

print(r1.text)
print(r1.text == r2.text)  # Should print True
```

**Output:**
```json
{
  ...
  "form": {
    "key1": [
      "value1",
      "value2"
    ]
  },
  ...
}
```

#### Sending Non-Form-Encoded Data

To send data that is not form-encoded, pass a string instead of a dictionary. For JSON-encoded data, you can use the `json` parameter.

```python
import json
import requests

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}

# Manually encode payload as JSON
r = requests.post(url, data=json.dumps(payload))
print(r.request.headers)

# Automatically encode payload as JSON using the json parameter
r = requests.post(url, json=payload)
print(r.request.headers)
```

**Output:**
```json
{
  'Content-Type': 'application/json',
  'Content-Length': '18',
  'User-Agent': 'python-requests/2.25.1'
}
```

#### Multipart-Encoded File Uploads

To upload files as multipart form data, use the `files` parameter.

```python
url = 'https://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}

r = requests.post(url, files=files)
print(r.text)
```

**Output:**
```json
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}
```

You can explicitly set the filename, content type, and headers:

```python
files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
r = requests.post(url, files=files)
print(r.text)
```

**Output:**
```json
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}
```

#### Sending Strings as Files

You can send strings to be received as files.

```python
files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
r = requests.post(url, files=files)
print(r.text)
```

**Output:**
```json
{
  ...
  "files": {
    "file": "some,data,to,send\\nanother,row,to,send\\n"
  },
  ...
}
```

#### Streaming Large File Uploads

For very large file uploads, you may want to stream the request using the `requests-toolbelt` library.

**Note:** By default, Requests does not support streaming multipart form-data uploads.

**Warning:** Always open files in binary mode when uploading. This ensures the correct `Content-Length` header is provided.

```python
with open('largefile.zip', 'rb') as f:
    r = requests.post(url, files={'file': f})
```

### Example Code

Here's a complete example demonstrating various advanced POST request features:

```python
import requests
import json

# Form-encoded data
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post('https://httpbin.org/post', data=payload)
print("Form-Encoded Data:", r.text)

# Multiple values for each key
payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
r1 = requests.post('https://httpbin.org/post', data=payload_tuples)
payload_dict = {'key1': ['value1', 'value2']}
r2 = requests.post('https://httpbin.org/post', data=payload_dict)
print("Multiple Values (Tuples):", r1.text)
print("Multiple Values (Dict):", r2.text)
print("Responses Match:", r1.text == r2.text)

# JSON-encoded data
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}

# Manually encode payload as JSON
r = requests.post(url, data=json.dumps(payload))
print("JSON (Manual):", r.request.headers)

# Automatically encode payload as JSON using the json parameter
r = requests.post(url, json=payload)
print("JSON (Automatic):", r.request.headers)

# Multipart-encoded file upload
files = {'file': open('report.xls', 'rb')}
r = requests.post('https://httpbin.org/post', files=files)
print("Multipart-Encoded File Upload:", r.text)

# Set filename, content type, and headers
files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
r = requests.post('https://httpbin.org/post', files=files)
print("File with Custom Headers:", r.text)

# Send strings as files
files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
r = requests.post('https://httpbin.org/post', files=files)
print("String as File:", r.text)
```

### Notes
- **Form-Encoded Data**: Automatically encodes dictionaries into form-encoded data.
- **JSON Data**: Use the `json` parameter to automatically encode dictionaries into JSON.
- **Multipart File Uploads**: Easily upload files as multipart form-data.
- **Streaming Large Files**: Consider using `requests-toolbelt` for streaming large file uploads.

This example covers advanced usage scenarios for sending POST requests with the Requests library, providing flexibility for various use cases.



# Understanding Response Status Codes, Headers, and Cookies with Requests

When working with HTTP requests using the Requests library in Python, it’s crucial to understand how to handle response status codes, headers, and cookies. Here’s a detailed look at these concepts.

## Response Status Codes

You can easily check the status code of a response. A successful request typically returns a status code of 200.

```python
import requests

r = requests.get('https://httpbin.org/get')
print(r.status_code)  # Output: 200
```

### Status Code Lookup

Requests provides a convenient way to check the status code using the `requests.codes` object.

```python
is_ok = r.status_code == requests.codes.ok
print(is_ok)  # Output: True
```

### Handling Errors

If a request results in a client error (4XX) or server error (5XX), you can raise an exception using `raise_for_status()`.

```python
bad_r = requests.get('https://httpbin.org/status/404')
print(bad_r.status_code)  # Output: 404

try:
    bad_r.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e}")  # Output: 404 Client Error
```

If the status code is 200, calling `raise_for_status()` will not raise an exception:

```python
r.raise_for_status()  # No output or error
```

## Response Headers

Response headers can be accessed like a dictionary.

```python
print(r.headers)
```

### Example Output:
```json
{
    'content-encoding': 'gzip',
    'transfer-encoding': 'chunked',
    'connection': 'close',
    'server': 'nginx/1.0.4',
    'x-runtime': '148ms',
    'etag': '"e1ca502697e5c9317743dc078f67693f"',
    'content-type': 'application/json'
}
```

### Case-Insensitive Access

Headers can be accessed using any capitalization due to their case-insensitive nature.

```python
print(r.headers['Content-Type'])  # Output: 'application/json'
print(r.headers.get('content-type'))  # Output: 'application/json'
```

### Handling Multiple Header Values

If a server sends the same header multiple times, Requests combines them into a single mapping.

```python
# If multiple values were sent, they would be combined in the output
```

## Working with Cookies

### Accessing Cookies

If the response contains cookies, you can access them easily.

```python
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)

print(r.cookies['example_cookie_name'])  # Output: 'example_cookie_value'
```

### Sending Cookies

You can send your own cookies to the server using the `cookies` parameter.

```python
url = 'https://httpbin.org/cookies'
cookies = dict(cookies_are='working')

r = requests.get(url, cookies=cookies)
print(r.text)  # Output: '{"cookies": {"cookies_are": "working"}}'
```

### Using RequestsCookieJar

Cookies are managed using a `RequestsCookieJar`, which behaves like a dictionary but provides a more complete interface for multiple domains or paths.

```python
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')

url = 'https://httpbin.org/cookies'
r = requests.get(url, cookies=jar)
print(r.text)  # Output: '{"cookies": {"tasty_cookie": "yum"}}'
```

### Full Example

Here’s a complete example demonstrating how to check status codes, headers, and manage cookies:

```python
import requests

# Check response status code
response = requests.get('https://httpbin.org/get')
print(f"Status Code: {response.status_code}")

# Raise for status if there's an error
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTPError: {e}")

# View response headers
print("Response Headers:")
for header, value in response.headers.items():
    print(f"{header}: {value}")

# Accessing specific header
content_type = response.headers.get('Content-Type')
print(f"Content-Type: {content_type}")

# Sending cookies
url = 'https://httpbin.org/cookies'
cookies = {'cookies_are': 'working'}
cookie_response = requests.get(url, cookies=cookies)
print(cookie_response.text)

# Using RequestsCookieJar
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')

jar_response = requests.get(url, cookies=jar)
print(jar_response.text)
```

### Summary

- **Status Codes**: Use `response.status_code` and `raise_for_status()` to handle HTTP responses effectively.
- **Headers**: Access response headers using a dictionary-like interface and remember they are case-insensitive.
- **Cookies**: Manage cookies using dictionaries or `RequestsCookieJar` for more complex scenarios. 

This knowledge is essential for effective HTTP request handling with the Requests library in Python.


# Redirection and Error Handling with Requests

When using the Requests library in Python, understanding how to handle redirection and various exceptions is crucial for robust HTTP communication. Here’s a comprehensive look at these concepts.

## Redirection and History

By default, Requests automatically follows redirects for all HTTP methods except `HEAD`. You can track redirections using the `history` property of the `Response` object, which stores the responses encountered during the redirection process.

### Example: Following Redirects

For instance, GitHub redirects HTTP requests to HTTPS:

```python
import requests

r = requests.get('http://github.com/')
print(r.url)           # Output: 'https://github.com/'
print(r.status_code)   # Output: 200
print(r.history)       # Output: [<Response [301]>]
```

### Disabling Redirection

You can disable automatic redirection by setting `allow_redirects=False`:

```python
r = requests.get('http://github.com/', allow_redirects=False)
print(r.status_code)   # Output: 301
print(r.history)       # Output: []
```

### Handling HEAD Requests

You can also enable redirection for `HEAD` requests:

```python
r = requests.head('http://github.com/', allow_redirects=True)
print(r.url)           # Output: 'https://github.com/'
print(r.history)       # Output: [<Response [301]>]
```

## Timeouts

Using the `timeout` parameter allows you to specify how long to wait for a response before raising an exception. This is essential to prevent your program from hanging indefinitely:

```python
try:
    requests.get('https://github.com/', timeout=0.001)
except requests.exceptions.Timeout:
    print("Request timed out.")
```

### Important Note on Timeout

The `timeout` applies to the connection and response time, not the entire response download. It raises an exception if no bytes have been received for the specified duration.

## Errors and Exceptions

Requests can raise several exceptions in case of network issues or HTTP errors:

- **ConnectionError**: Raised for network-related errors (e.g., DNS failure, refused connection).
- **HTTPError**: Raised by `response.raise_for_status()` for unsuccessful HTTP status codes.
- **Timeout**: Raised if the request exceeds the specified timeout.
- **TooManyRedirects**: Raised if the request exceeds the configured number of maximum redirections.

All exceptions raised by Requests inherit from `requests.exceptions.RequestException`.

### Example of Exception Handling

Here’s how you can handle various exceptions:

```python
import requests

try:
    r = requests.get('https://httpbin.org/status/404')
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTPError: {e}")  # Output: HTTPError: 404 Client Error
except requests.exceptions.ConnectionError as e:
    print(f"ConnectionError: {e}")
except requests.exceptions.Timeout as e:
    print(f"Timeout: {e}")
except requests.exceptions.TooManyRedirects as e:
    print(f"TooManyRedirects: {e}")
except requests.exceptions.RequestException as e:
    print(f"RequestException: {e}")
```

## Summary

- **Redirection**: Requests automatically follows redirects, and you can track them using `Response.history`. Disable redirection by setting `allow_redirects=False`.
- **Timeouts**: Always use the `timeout` parameter to prevent hanging requests. It specifies the maximum wait time for a response.
- **Error Handling**: Use specific exception handling for network issues, HTTP errors, timeouts, and redirection limits to create robust applications.

By following these practices, you can ensure reliable and efficient HTTP communication using the Requests library in Python.



# Advanced Usage of Requests

This section explores advanced features of the Requests library, focusing on session management and related functionalities.

## Session Objects

The `Session` object allows you to persist certain parameters across multiple requests, such as cookies and headers. It utilizes connection pooling, which can significantly enhance performance when making several requests to the same host.

### Creating a Session

To create a session, simply instantiate a `Session` object:

```python
import requests

s = requests.Session()
```

### Persisting Cookies

You can persist cookies across requests using a `Session`:

```python
s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('https://httpbin.org/cookies')

print(r.text)
# Output: '{"cookies": {"sessioncookie": "123456789"}}'
```

### Setting Default Parameters

A `Session` can also hold default parameters for requests, such as authentication and custom headers:

```python
s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})

# Both 'x-test' and 'x-test2' are sent
response = s.get('https://httpbin.org/headers', headers={'x-test2': 'true'})
print(response.text)
```

### Merging Session and Method Parameters

When making a request, any parameters provided will be merged with those set at the session level. Method-level parameters will override session parameters:

```python
s = requests.Session()

r = s.get('https://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(r.text)
# Output: '{"cookies": {"from-my": "browser"}}'

r = s.get('https://httpbin.org/cookies')
print(r.text)
# Output: '{"cookies": {}}'
```

### Managing Cookies Manually

You can manually manipulate session cookies using utility functions:

```python
s.cookies.set('another_cookie', 'value')
print(s.cookies)
```

### Using Sessions as Context Managers

You can utilize sessions as context managers to ensure they are closed properly:

```python
with requests.Session() as s:
    s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
```

## Removing a Value from a Dictionary Parameter

If you need to omit session-level keys from a method-level parameter, set that key’s value to `None`:

```python
s = requests.Session()
s.headers.update({'Authorization': 'Bearer token'})

# Omit the Authorization header for this request
response = s.get('https://httpbin.org/headers', headers={'Authorization': None})
print(response.text)
```

### Accessing All Session Values

All values stored in a session are directly accessible. For detailed information, refer to the [Session API Documentation](https://docs.python-requests.org/en/latest/user/advanced/#session-objects).

## Summary

- **Session Management**: Use `Session` objects to persist parameters and enhance performance through connection pooling.
- **Default Parameters**: Set default authentication and headers for all requests made from the session.
- **Context Management**: Employ context managers for session handling to ensure proper closure.
- **Custom Cookies**: Manually manage cookies and omit session-level parameters as needed.

By leveraging these advanced features, you can create more efficient and flexible HTTP clients using the Requests library.



# Request and Response Objects in Requests

When using the Requests library, each call to `requests.get()` or similar functions involves creating two key objects: a **Request** object and a **Response** object.

## Request and Response Lifecycle

1. **Request Object**: This is constructed when you make a request to a server to fetch or query a resource.
2. **Response Object**: Once the server responds, a Response object is generated containing all the information returned by the server, along with the original Request object.

### Example of Making a Request

Here’s a simple example to get information from Wikipedia:

```python
import requests

r = requests.get('https://en.wikipedia.org/wiki/Monty_Python')
```

### Accessing Response Headers

To view the headers sent by the server, use:

```python
print(r.headers)
```

Output example:

```json
{
  'content-length': '56170',
  'content-type': 'text/html; charset=UTF-8',
  'server': 'Apache',
  ...
}
```

### Accessing Request Headers

To check the headers you sent to the server, access the request attribute:

```python
print(r.request.headers)
```

Output example:

```json
{
  'Accept-Encoding': 'identity, deflate, compress, gzip',
  'User-Agent': 'python-requests/1.2.0',
  ...
}
```

## Prepared Requests

When you receive a Response object, the `request` attribute contains a **PreparedRequest**. This is useful if you need to modify the body or headers before sending a request.

### Creating a Prepared Request

Here’s how to prepare a request:

```python
from requests import Request, Session

s = Session()

req = Request('POST', url, data=data, headers=headers)
prepped = req.prepare()

# Modify the request body
prepped.body = 'No, I want exactly this as the body.'

# Modify headers
del prepped.headers['Content-Type']

resp = s.send(prepped)

print(resp.status_code)
```

### Using Session to Prepare a Request

To ensure session-level state (like cookies) is applied, use `Session.prepare_request()`:

```python
s = Session()
req = Request('GET', url, data=data, headers=headers)

prepped = s.prepare_request(req)

# Modify the request body
prepped.body = 'Seriously, send exactly these bytes.'

# Add a custom header
prepped.headers['Keep-Dead'] = 'parrot'

resp = s.send(prepped)

print(resp.status_code)
```

### Environment Settings

Be cautious when using prepared requests as they may not consider your environment settings (like SSL certificates). To merge environment settings into your session:

```python
settings = s.merge_environment_settings(prepped.url, {}, None, None, None)
resp = s.send(prepped, **settings)

print(resp.status_code)
```

## Summary

- **Request and Response Objects**: Understand the lifecycle of requests and responses to better manage HTTP interactions.
- **Prepared Requests**: Use PreparedRequest for more control over the request details.
- **Session Management**: Leverage Sessions to maintain state, such as cookies, across multiple requests.
- **Environment Settings**: Always consider merging environment settings to avoid issues with SSL and other configurations.


# SSL Certificate Verification in Requests

Requests automatically verifies SSL certificates for HTTPS requests, similar to web browsers. By default, SSL verification is enabled.

## SSL Verification Behavior

When a certificate can't be verified, an exception is raised:

```python
requests.get('https://requestb.in')
# raises requests.exceptions.SSLError
```

However, for valid SSL setups, such as GitHub:

```python
response = requests.get('https://github.com')
print(response)  # <Response [200]>
```

## Custom CA Bundle

You can specify a custom CA bundle for verification:

```python
requests.get('https://github.com', verify='/path/to/certfile')
```

For persistent sessions:

```python
s = requests.Session()
s.verify = '/path/to/certfile'
```

### Note

If specifying a directory, ensure it’s processed with OpenSSL's `c_rehash` utility.

## Environment Variables

Set the `REQUESTS_CA_BUNDLE` environment variable to specify a trusted CA list. If not set, `CURL_CA_BUNDLE` will be used as a fallback.

## Disabling SSL Verification

To ignore SSL verification (not recommended for production):

```python
requests.get('https://kennethreitz.org', verify=False)
```

### Warning

Setting `verify=False` allows any TLS certificate, exposing your application to man-in-the-middle (MitM) attacks. Use it only in development or testing environments.

## Client-Side Certificates

To use a local client-side certificate:

```python
requests.get('https://kennethreitz.org', cert=('/path/client.cert', '/path/client.key'))
```

For persistent sessions:

```python
s = requests.Session()
s.cert = '/path/client.cert'
```

### Error Handling

An incorrect path or invalid certificate raises an `SSLError`:

```python
requests.get('https://kennethreitz.org', cert='/wrong_path/client.pem')
# raises SSLError
```

### Warning

The private key for the local certificate must be unencrypted, as Requests does not support encrypted keys.

## CA Certificates

Requests uses the `certifi` package for trusted certificates, ensuring up-to-date security without changing Requests versions. It's recommended to frequently update `certifi` to maintain security.

## Summary

- **SSL Verification**: Enabled by default; can raise exceptions for mismatches.
- **Custom CA Bundles**: Specify paths for trusted CAs.
- **Disabling Verification**: Use `verify=False` cautiously.
- **Client Certificates**: Support for specifying client-side certs.
- **Certificate Management**: Use `certifi` for up-to-date trusted certificates.


# Body Content Workflow in Requests

## Default Behavior

By default, the response body is downloaded immediately upon making a request. You can change this behavior by using the `stream` parameter:

```python
tarball_url = 'https://github.com/psf/requests/tarball/main'
r = requests.get(tarball_url, stream=True)
```

This way, only the response headers are downloaded initially, keeping the connection open for conditional content retrieval:

```python
if int(r.headers['content-length']) < TOO_LONG:
    content = r.content
```

## Controlled Content Retrieval

You can control the content workflow further using `Response.iter_content()` or `Response.iter_lines()`, or access the raw body through `Response.raw`.

### Important Note on Streaming

When using `stream=True`, ensure to consume all the data or call `Response.close` to prevent connection inefficiencies. It's advisable to use a context manager:

```python
with requests.get('https://httpbin.org/get', stream=True) as r:
    # Process the response here
```

## Keep-Alive Connections

Requests automatically manage keep-alive connections within a session, reusing connections for efficiency. However, ensure all body data is read to release connections back to the pool.

## Streaming Uploads

For large uploads, use a file-like object directly:

```python
with open('massive-body', 'rb') as f:
    requests.post('http://some.url/streamed', data=f)
```

### Warning

Always open files in binary mode to avoid errors with the `Content-Length` header.

## Chunk-Encoded Requests

Requests also supports chunked transfer encoding. To send a chunked request, provide a generator:

```python
def gen():
    yield 'hi'
    yield 'there'

requests.post('http://some.url/chunked', data=gen())
```

### Handling Chunked Responses

For chunked responses, iterate using `Response.iter_content()`. It's best to set `stream=True` for optimal handling:

```python
for chunk in r.iter_content(chunk_size=None):
    # Process each chunk
```

You can specify a `chunk_size` to control the maximum size of each chunk:

```python
for chunk in r.iter_content(chunk_size=1024):
    # Process each 1024-byte chunk
```


# POSTing Multiple Multipart-Encoded Files

To upload multiple files using the `requests` library in Python, you can send files as multipart-encoded in a single request. This is useful when an HTML form has a multiple file upload field, such as:

```html
<input type="file" name="images" multiple="true" required="true"/>
```

## Example Code

Here’s how to upload multiple image files:

```python
import requests

url = 'https://httpbin.org/post'
multiple_files = [
    ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
    ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))
]

r = requests.post(url, files=multiple_files)
print(r.text)
```

### Expected Output

The server will respond with a JSON object that includes information about the uploaded files:

```json
{
  ...
  "files": {
    "images": "data:image/png;base64,iVBORw..."
  },
  "Content-Type": "multipart/form-data; boundary=3131623adb2043caaeb5538cc7aa0b3a",
  ...
}
```

### Important Note

Always open files in binary mode (`'rb'`). This ensures the `Content-Length` header is accurately set to the number of bytes in the file, preventing errors that could occur if opened in text mode.

---

## Event Hooks

Requests supports a hook system to manipulate parts of the request process or signal event handling. One common hook is the `response` hook, which allows you to perform actions based on the response received from a request.

### Example: Using a Hook

You can assign a hook function to be executed upon receiving a response:

```python
def print_url(r, *args, **kwargs):
    print(r.url)

requests.get('https://httpbin.org/', hooks={'response': print_url})
```

#### Output

This will print the URL of the request:

```
https://httpbin.org/
<Response [200]>
```

### Multiple Hooks

You can attach multiple hooks to a single request by passing a list of functions:

```python
def record_hook(r, *args, **kwargs):
    r.hook_called = True
    return r

r = requests.get('https://httpbin.org/', hooks={'response': [print_url, record_hook]})
print(r.hook_called)  # True
```

### Using Hooks in a Session

You can also add hooks to a `Session` instance, which will apply to all requests made from that session:

```python
s = requests.Session()
s.hooks['response'].append(print_url)
s.get('https://httpbin.org/')
```

#### Output

```
https://httpbin.org/
<Response [200]>
```

---

## Custom Authentication

Requests allows you to implement custom authentication by creating a subclass of `AuthBase`. This is useful when standard authentication methods don’t fit your needs.

### Example: Custom Authentication

Here’s how to create a custom authentication mechanism:

```python
from requests.auth import AuthBase

class PizzaAuth(AuthBase):
    """Attaches HTTP Pizza Authentication to the given Request object."""
    def __init__(self, username):
        self.username = username

    def __call__(self, r):
        r.headers['X-Pizza'] = self.username
        return r
```

You can then use your custom authentication when making requests:

```python
response = requests.get('http://pizzabin.org/admin', auth=PizzaAuth('kenneth'))
print(response)
```

### Expected Output

If the authentication is successful, you might receive:

```
<Response [200]>
```

This indicates that the request was accepted by the server.

---

### Summary

Using the `requests` library, you can efficiently upload multiple files, utilize hooks for custom processing, and implement custom authentication schemes to suit your application’s needs.



### Streaming Requests with `Response.iter_lines()`

**Overview:**
When dealing with streaming APIs (like the Twitter Streaming API), you can use `Response.iter_lines()` to read the response line by line. This is useful for processing large amounts of data without loading everything into memory at once.

#### Example:
```python
import json
import requests

# Make a streaming request
r = requests.get('https://httpbin.org/stream/20', stream=True)

# Iterate over the response line by line
for line in r.iter_lines():
    if line:  # Filter out keep-alive new lines
        decoded_line = line.decode('utf-8')
        print(json.loads(decoded_line))
```

**Expected Output:**
You might see output similar to this, depending on the streaming content:
```json
{"number": 0}
{"number": 1}
{"number": 2}
...
{"number": 19}
```

### Using `decode_unicode=True`

When using `iter_lines()` or `iter_content()`, it’s good practice to specify `decode_unicode=True` to handle character encoding properly.

#### Example:
```python
r = requests.get('https://httpbin.org/stream/20', stream=True)

if r.encoding is None:
    r.encoding = 'utf-8'

for line in r.iter_lines(decode_unicode=True):
    if line:
        print(json.loads(line))
```

### Warning about `iter_lines()`

**Important Note:** `iter_lines()` is **not reentrant safe**, meaning calling it multiple times can lead to lost data. Instead, save the iterator and reuse it.

#### Example:
```python
lines = r.iter_lines()
first_line = next(lines)  # Save the first line

for line in lines:
    print(line)
```

### Proxies

If you need to route your requests through a proxy, you can specify a `proxies` dictionary.

#### Example:
```python
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}

response = requests.get('http://example.org', proxies=proxies)
print(response.status_code)  # Output should indicate the request status
```

### Using Proxies with a Session

To apply proxies to all requests made within a session, you can configure the session’s proxies.

#### Example:
```python
session = requests.Session()
session.proxies.update(proxies)

response = session.get('http://example.org')
print(response.status_code)  # Output should indicate the request status
```

### Environmental Proxies

You can set proxy configurations globally using environment variables.

#### Example:
```bash
export HTTP_PROXY="http://10.10.1.10:3128"
export HTTPS_PROXY="http://10.10.1.10:1080"
```

Then in Python:
```python
import requests

response = requests.get('http://example.org')
print(response.status_code)
```

### Using HTTP Basic Auth with Proxies

To authenticate with a proxy, include the username and password in the proxy URL.

#### Example:
```bash
export HTTPS_PROXY="http://user:pass@10.10.1.10:1080"
```

In Python:
```python
proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
response = requests.get('http://example.org', proxies=proxies)
print(response.status_code)
```

### Important Warnings

1. **Sensitive Information**: Storing sensitive information (like usernames and passwords) in environment variables is a security risk. Avoid doing this if possible.
   
2. **Overriding Proxies**: When using a session, environmental proxy settings can override your specified proxy settings. Always ensure to specify the `proxies` argument when necessary.

### Summary

This breakdown shows how to effectively use streaming requests and proxies with the `requests` library in Python. Each example illustrates practical usage, with expected outputs to help you understand what to anticipate when running the code.


### SOCKS Support

**Overview:**
Starting from version 2.10.0, the `requests` library supports SOCKS proxies. This requires additional third-party libraries, which can be installed via pip.

#### Installing Dependencies:
To enable SOCKS support, install the required dependencies:
```bash
$ python -m pip install requests[socks]
```

#### Using SOCKS Proxies:
Using a SOCKS proxy is straightforward, similar to using an HTTP proxy. Here’s how to configure it:

```python
proxies = {
    'http': 'socks5://user:pass@host:port',
    'https': 'socks5://user:pass@host:port'
}
response = requests.get('http://example.org', proxies=proxies)
print(response.status_code)
```

### DNS Resolution with SOCKS

- Using `socks5` will perform DNS resolution on the client side, which is generally preferred.
- If you want DNS resolution to happen on the proxy server instead, use `socks5h`:

```python
proxies = {
    'http': 'socks5h://user:pass@host:port',
    'https': 'socks5h://user:pass@host:port'
}
```

### Compliance

**Requests** aims to comply with relevant specifications and RFCs. This focus on compliance may lead to behaviors that seem unusual to users unfamiliar with the specifications.

### Handling Encodings

When receiving a response, the `requests` library determines the encoding to use for decoding the response body.

#### Encoding Detection Steps:

1. **HTTP Header Check**: Requests first looks for an encoding specified in the HTTP headers.
2. **Guessing Encoding**: If no encoding is provided in the headers, Requests uses `charset_normalizer` or `chardet` to guess the encoding.
   - If `chardet` is installed, it will be used for guessing the encoding.
   - If `chardet` is not installed, Requests defaults to using `charset_normalizer`.

#### Default Encoding:
If neither encoding is specified in the headers, and the `Content-Type` indicates text, Requests defaults to **ISO-8859-1** per RFC 2616.

### Setting the Encoding Manually

You can manually set the response encoding if needed:

```python
response = requests.get('http://example.org')
response.encoding = 'utf-8'  # Set to your desired encoding
print(response.text)
```

Alternatively, you can access the raw content directly:

```python
content = response.content  # Get raw bytes
```

### Summary of Key Points

| Feature            | Description                                           |
|--------------------|-----------------------------------------------------|
| **SOCKS Support**  | Requires installation of additional libraries.      |
| **Usage**          | Configured just like HTTP proxies with `socks5` or `socks5h`. |
| **DNS Resolution** | `socks5` for client-side resolution; `socks5h` for proxy-side. |
| **Encoding Detection** | Checks headers first, then uses guessing libraries. |
| **Default Encoding** | Follows ISO-8859-1 if no charset is specified.   |
| **Manual Encoding** | Can set `Response.encoding` or use `Response.content`. |


### HTTP Verbs

The `requests` library supports several HTTP verbs, including **GET, OPTIONS, HEAD, POST, PUT, PATCH, and DELETE**. Below are detailed examples of each verb using the GitHub API.

### 1. GET

**Purpose:** Retrieve data from a specified resource.

**Example:**
```python
import requests

r = requests.get('https://api.github.com/repos/psf/requests/git/commits/a050faf084662f3a352dd1a941f2c7c9f886d4ad')

if r.status_code == requests.codes.ok:
    print(r.headers['content-type'])  # Check content type
    commit_data = r.json()             # Parse JSON response
    print(commit_data.keys())           # Display keys in the response
```

**Output:**
```
application/json; charset=utf-8
['committer', 'author', 'url', 'tree', 'sha', 'parents', 'message']
```

### 2. OPTIONS

**Purpose:** Determine which HTTP methods are supported by a resource.

**Example:**
```python
verbs = requests.options(r.url)
print(verbs.status_code)  # Check response status
```

**Output:**
```
500 (if OPTIONS not implemented)
```

If it were implemented:
```python
# Example for another URL
verbs = requests.options('http://a-good-website.com/api/cats')
print(verbs.headers['allow'])  # Display allowed methods
```

**Output:**
```
GET,HEAD,POST,OPTIONS
```

### 3. POST

**Purpose:** Create a new resource.

**Example:**
```python
url = 'https://api.github.com/repos/psf/requests/issues/482/comments'
body = json.dumps({"body": "Sounds great! I'll get right on it!"})

from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('fake@example.com', 'not_a_real_password')

r = requests.post(url=url, data=body, auth=auth)
print(r.status_code)  # Check response status
print(r.json()['body'])  # Display posted comment
```

**Output:**
```
201
Sounds great! I'll get right on it!
```

### 4. PATCH

**Purpose:** Update an existing resource.

**Example:**
```python
comment_id = 5804413
url = f'https://api.github.com/repos/psf/requests/issues/comments/{comment_id}'
body = json.dumps({"body": "Sounds great! I'll get right on it once I feed my cat."})

r = requests.patch(url=url, data=body, auth=auth)
print(r.status_code)  # Check response status
```

**Output:**
```
200
```

### 5. DELETE

**Purpose:** Remove a specified resource.

**Example:**
```python
r = requests.delete(url=url, auth=auth)
print(r.status_code)  # Check response status
print(r.headers['status'])  # Check response headers
```

**Output:**
```
204
204 No Content
```

### 6. HEAD

**Purpose:** Retrieve headers from a resource without the body.

**Example:**
```python
r = requests.head(url=url, auth=auth)
print(r.headers)  # Display response headers
```

**Output:**
```
'x-ratelimit-remaining': '4995',
'x-ratelimit-limit': '5000',
...
```

### Summary Table of HTTP Verbs

| Verb   | Purpose                                | Example Usage                                    |
|--------|----------------------------------------|-------------------------------------------------|
| GET    | Retrieve data                         | `requests.get(url)`                             |
| OPTIONS| Check supported methods               | `requests.options(url)`                          |
| POST   | Create a new resource                 | `requests.post(url, data=body, auth=auth)`     |
| PATCH  | Update an existing resource           | `requests.patch(url, data=body, auth=auth)`    |
| DELETE | Remove a specified resource           | `requests.delete(url, auth=auth)`               |
| HEAD   | Retrieve headers                      | `requests.head(url, auth=auth)`                 |

### Conclusion

Using the `requests` library with different HTTP verbs allows you to interact effectively with APIs, like GitHub's. This breakdown provides clear examples and expected outputs for each HTTP verb!


### Custom Verbs

Sometimes, you may need to use HTTP verbs not covered by the standard set (GET, POST, etc.). For such cases, you can use the `.request` method to specify any HTTP method.

**Example: Using a Custom Verb (MKCOL)**

```python
import requests

url = 'https://example.com/your-endpoint'
data = {'key': 'value'}

r = requests.request('MKCOL', url, data=data)
print(r.status_code)  # Check response status
```

**Output:**
```
200  # Assuming the call was successful
```

### Link Headers

Many APIs use Link headers to facilitate pagination and make APIs more self-describing. GitHub's API uses these headers for navigating through pages of results.

**Example: Retrieving Link Headers**

```python
url = 'https://api.github.com/users/kennethreitz/repos?page=1&per_page=10'
r = requests.head(url=url)
print(r.headers['link'])  # Print Link header
```

**Output:**
```
<https://api.github.com/users/kennethreitz/repos?page=2&per_page=10>; rel="next", <https://api.github.com/users/kennethreitz/repos?page=6&per_page=10>; rel="last"
```

You can easily access the parsed links:

```python
print(r.links["next"])  # Access the 'next' link
print(r.links["last"])  # Access the 'last' link
```

**Output:**
```python
{'url': 'https://api.github.com/users/kennethreitz/repos?page=2&per_page=10', 'rel': 'next'}
{'url': 'https://api.github.com/users/kennethreitz/repos?page=7&per_page=10', 'rel': 'last'}
```

### Transport Adapters

Transport Adapters in `requests` allow you to define interaction methods for an HTTP service and apply configuration per service.

**Example: Mounting a Custom Transport Adapter**

You can create a custom adapter and mount it to a session:

```python
import requests

class MyAdapter(requests.adapters.HTTPAdapter):
    # Custom adapter implementation
    pass

s = requests.Session()
s.mount('https://github.com/', MyAdapter())
```

This mounts `MyAdapter` to any requests made to URLs starting with `https://github.com/`.

**Note:** The adapter will be selected based on the longest prefix match.

### Custom SSL Version with Transport Adapters

You can also create adapters for specific use cases, such as enforcing a particular SSL version.

**Example: Enforcing SSLv3**

Here’s how to create a transport adapter that uses SSLv3:

```python
import ssl
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter

class Ssl3HttpAdapter(HTTPAdapter):
    """Transport adapter that allows us to use SSLv3."""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_SSLv3)

# Usage
s = requests.Session()
s.mount('https://example.com/', Ssl3HttpAdapter())
```

### Summary Table

| Feature         | Description                                                   | Example                           |
|------------------|---------------------------------------------------------------|-----------------------------------|
| Custom Verbs      | Use any HTTP method with `.request`                           | `requests.request('MKCOL', url)` |
| Link Headers       | Handle pagination and self-describing APIs                    | `r.headers['link']`              |
| Transport Adapters | Customize HTTP interactions and apply specific configurations | `s.mount('https://github.com/', MyAdapter())` |

### Conclusion

Using custom verbs, handling link headers for pagination, and implementing transport adapters allows for flexible and powerful interactions with APIs in Python using the `requests` library!


Sure! Here’s a breakdown of **Automatic Retries**, **Blocking vs. Non-Blocking I/O**, **Header Ordering**, and **Timeouts** in the `requests` library.

### Automatic Retries

By default, the `requests` library does not automatically retry failed connections. However, you can implement automatic retries using the `urllib3.util.Retry` class within a `Session`.

**Example: Setting Up Automatic Retries**

```python
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter

s = Session()
retries = Retry(
    total=3,
    backoff_factor=0.1,
    status_forcelist=[502, 503, 504],
    allowed_methods={'POST'},
)

s.mount('https://', HTTPAdapter(max_retries=retries))
```

### Blocking vs. Non-Blocking I/O

By default, `requests` does not support non-blocking I/O. Calls to properties like `Response.content` will block until the entire response is downloaded. However, you can use streaming features to retrieve smaller amounts of data at a time, though these calls will still block.

**Alternative Libraries for Non-Blocking I/O:**

- **`requests-threads`**
- **`grequests`**
- **`requests-futures`**
- **`httpx`**

### Header Ordering

In certain cases, you might want to maintain the order of headers in your requests. You can achieve this by using `OrderedDict` for the headers.

**Example: Using `OrderedDict` for Headers**

```python
from collections import OrderedDict

headers = OrderedDict([
    ('Authorization', 'Bearer token'),
    ('Content-Type', 'application/json')
])

response = requests.get('https://example.com', headers=headers)
```

**Note:** If you set default headers on a `Session`, they will maintain their order, and you can override them as needed.

### Timeouts

Setting a timeout for requests is crucial to prevent your code from hanging indefinitely. By default, requests do not set a timeout unless specified.

**Types of Timeouts:**
- **Connect Timeout:** Time to establish a connection.
- **Read Timeout:** Time to wait for a server response after a connection is made.

**Example: Setting a Timeout**

```python
# Single value applies to both connect and read timeouts
response = requests.get('https://github.com', timeout=5)

# Tuple for separate connect and read timeouts
response = requests.get('https://github.com', timeout=(3.05, 27))
```

To wait indefinitely for a response, use `None`:

```python
response = requests.get('https://github.com', timeout=None)
```

**Important Notes:**
- The connect timeout applies to each connection attempt; if multiple addresses exist for a domain, this could lead to longer effective timeouts.
- Timeouts are not wall clock times; the real elapsed time may exceed specified timeout values due to connection retries or other factors.

### Summary Table

| Feature                     | Description                                          | Example                                         |
|-----------------------------|------------------------------------------------------|-------------------------------------------------|
| Automatic Retries            | Retry failed connections with backoff               | `Retry(total=3, backoff_factor=0.1)`           |
| Blocking I/O                | Requests block until the entire response is downloaded| Use streaming for partial retrieval              |
| Header Ordering              | Maintain order of headers using `OrderedDict`       | `headers=OrderedDict([...])`                   |
| Timeouts                    | Prevent hanging by specifying connection/read timeouts| `timeout=(3.05, 27)`                            |

### Conclusion

Using automatic retries, managing blocking I/O, ordering headers, and setting appropriate timeouts ensures robust and efficient interactions with web APIs using the `requests` library!
