

Here are examples for the HTTP status codes from RFC 2616:

### Informational (1xx) Examples

#### 100 Continue
```python
import requests

response = requests.post('http://example.com/api', data={'key': 'value'}, headers={'Expect': '100-continue'})
# If the server responds with 100 Continue, the client continues sending the request body.
```

#### 101 Switching Protocols
```python
import requests

response = requests.get('http://example.com', headers={'Upgrade': 'websocket'})
# If the server responds with 101, it switches protocols as requested.
```

### Successful (2xx) Examples

#### 200 OK
```python
response = requests.get('https://api.github.com/repos/psf/requests')
if response.status_code == 200:
    data = response.json()
    print(data['full_name'])  # Outputs: psf/requests
```

#### 201 Created
```python
response = requests.post('https://api.github.com/repos/psf/requests/issues', json={'title': 'New Issue'})
if response.status_code == 201:
    print(response.headers['Location'])  # URL of the created resource
```

#### 202 Accepted
```python
response = requests.post('https://api.example.com/process', json={'data': 'value'})
if response.status_code == 202:
    print('Request accepted for processing.')
```

#### 203 Non-Authoritative Information
```python
response = requests.get('https://api.example.com/resource')
if response.status_code == 203:
    print('Received non-authoritative information.')
```

#### 204 No Content
```python
response = requests.delete('https://api.example.com/resource/123')
if response.status_code == 204:
    print('Resource deleted successfully.')
```

### Summary Table with Examples

| Status Code | Description                          | Example Code                                                |
|-------------|--------------------------------------|------------------------------------------------------------|
| **1xx**      | Informational                        |                                                            |
| 100         | Continue                             | `Expect: 100-continue` in headers during a POST request.  |
| 101         | Switching Protocols                 | `Upgrade: websocket` in headers for protocol switch.       |
| **2xx**      | Successful                           |                                                            |
| 200         | OK                                   | `requests.get('https://api.github.com/repos/...')`         |
| 201         | Created                              | `requests.post('.../issues', json={'title': 'New Issue'})` |
| 202         | Accepted                             | `requests.post('.../process', json={'data': 'value'})`    |
| 203         | Non-Authoritative Information        | `requests.get('.../resource')`                             |
| 204         | No Content                           | `requests.delete('.../resource/123')`                      |

Feel free to ask if you need more details or additional examples!### 10 Status Code Definitions

#### 10.1 Informational (1xx)

These codes indicate provisional responses and consist of a Status-Line and optional headers, terminated by an empty line.

**Key Points:**
- **1xx responses** should not be sent to HTTP/1.0 clients except in experimental conditions.
- Clients must be prepared to handle 1xx responses.

##### 10.1.1 100 Continue
- The client should continue with the request. This interim response indicates that the initial part of the request has been received.

##### 10.1.2 101 Switching Protocols
- The server agrees to switch protocols as specified in the `Upgrade` header. This is used for changing the application protocol on the connection.

---

#### 10.2 Successful (2xx)

These codes indicate that the client's request was successfully received, understood, and accepted.

##### 10.2.1 200 OK
- The request has succeeded. The response varies based on the request method:
  - **GET:** Returns the resource.
  - **HEAD:** Returns entity-header fields without the body.
  - **POST:** Returns an entity describing the result.
  - **TRACE:** Returns the received request message.

##### 10.2.2 201 Created
- The request has been fulfilled, resulting in a new resource being created. The location of the new resource is provided in the `Location` header.

##### 10.2.3 202 Accepted
- The request has been accepted for processing but is not completed. It allows for asynchronous operations without needing a persistent connection.

##### 10.2.4 203 Non-Authoritative Information
- The returned metadata is not the definitive set from the origin server but is from a local or third-party source. It may contain additional or fewer details.

##### 10.2.5 204 No Content
- The server has fulfilled the request but does not need to return a message body. It may return updated metadata via headers. The response must not include a message body.

---

### Summary Table of Status Codes

| Status Code | Description                          | Method(s)                 |
|-------------|--------------------------------------|---------------------------|
| **1xx**      | Informational                        |                           |
| 100         | Continue                             | Any                       |
| 101         | Switching Protocols                 | Any                       |
| **2xx**      | Successful                           |                           |
| 200         | OK                                   | GET, HEAD, POST, TRACE    |
| 201         | Created                              | POST                      |
| 202         | Accepted                             | Any                       |
| 203         | Non-Authoritative Information        | Any                       |
| 204         | No Content                           | Any                       |

### Conclusion

Understanding these status codes is crucial for effectively handling HTTP responses in web applications and APIs!


Here are examples for the HTTP status codes from RFC 2616:

### Informational (1xx) Examples

#### 100 Continue
```python
import requests

response = requests.post('http://example.com/api', data={'key': 'value'}, headers={'Expect': '100-continue'})
# If the server responds with 100 Continue, the client continues sending the request body.
```

#### 101 Switching Protocols
```python
import requests

response = requests.get('http://example.com', headers={'Upgrade': 'websocket'})
# If the server responds with 101, it switches protocols as requested.
```

### Successful (2xx) Examples

#### 200 OK
```python
response = requests.get('https://api.github.com/repos/psf/requests')
if response.status_code == 200:
    data = response.json()
    print(data['full_name'])  # Outputs: psf/requests
```

#### 201 Created
```python
response = requests.post('https://api.github.com/repos/psf/requests/issues', json={'title': 'New Issue'})
if response.status_code == 201:
    print(response.headers['Location'])  # URL of the created resource
```

#### 202 Accepted
```python
response = requests.post('https://api.example.com/process', json={'data': 'value'})
if response.status_code == 202:
    print('Request accepted for processing.')
```

#### 203 Non-Authoritative Information
```python
response = requests.get('https://api.example.com/resource')
if response.status_code == 203:
    print('Received non-authoritative information.')
```

#### 204 No Content
```python
response = requests.delete('https://api.example.com/resource/123')
if response.status_code == 204:
    print('Resource deleted successfully.')
```



### 10.2.6 205 Reset Content

**Description:**
The server has fulfilled the request, and the user agent should reset the document view that caused the request. This is commonly used in form submissions where the server processes the input and suggests clearing the form afterward.

**Example:**
```python
import requests

response = requests.post('https://api.example.com/form-submit', data={'name': 'Alice'})
if response.status_code == 205:
    print("Form submitted successfully. Please reset the form.")
```

**Expected Output:**
```
Form submitted successfully. Please reset the form.
```

---

### 10.2.7 206 Partial Content

**Description:**
The server has fulfilled a partial GET request. The client must include a `Range` header to specify the desired byte range of the resource. The response includes the `Content-Range` header to indicate which part of the resource is being sent.

**Example:**
```python
url = 'https://example.com/largefile.zip'
headers = {'Range': 'bytes=0-999'}  # Requesting the first 1000 bytes
response = requests.get(url, headers=headers)

if response.status_code == 206:
    print(f"Partial content received: {response.headers['Content-Range']}")
    print(response.content[:50])  # Display first 50 bytes of content
```

**Expected Output:**
```
Partial content received: bytes 0-999/5000
b'...<binary data>...'  # Actual binary data truncated for display
```

---

### 10.3 Redirection (3xx)

This class of status codes indicates that further action is needed by the user agent to fulfill the request.

---

### 10.3.1 300 Multiple Choices

**Description:**
The requested resource corresponds to multiple representations, and the user must choose one. The server provides a list of available options.

**Example:**
```python
url = 'https://api.example.com/resource'
response = requests.get(url)

if response.status_code == 300:
    print("Multiple choices available:")
    # Assume the response includes a list in the body
    choices = response.json()
    for choice in choices:
        print(choice['title'], choice['url'])
```

**Expected Output:**
```
Multiple choices available:
Choice 1 http://example.com/choice1
Choice 2 http://example.com/choice2
```

---

### 10.3.2 301 Moved Permanently

**Description:**
The requested resource has been permanently moved to a new URI. Future references should use the new URI, indicated by the `Location` header.

**Example:**
```python
url = 'http://old.example.com/resource'
response = requests.get(url)

if response.status_code == 301:
    print("Resource has moved permanently to:", response.headers['Location'])
```

**Expected Output:**
```
Resource has moved permanently to: http://new.example.com/resource
```

### Summary Table

| Status Code | Description                          | Example Code                                                | Expected Output                                |
|-------------|--------------------------------------|------------------------------------------------------------|------------------------------------------------|
| **205**      | Reset Content                        | `requests.post(...).status_code == 205`                   | `Form submitted successfully. Please reset the form.` |
| **206**      | Partial Content                     | `requests.get(..., headers={'Range': 'bytes=0-999'})`    | `Partial content received: bytes 0-999/5000` |
| **300**      | Multiple Choices                    | `requests.get(...).status_code == 300`                     | `Multiple choices available: Choice 1 ...`    |
| **301**      | Moved Permanently                   | `requests.get(...).status_code == 301`                     | `Resource has moved permanently to: ...`       |



### 10.3.3 302 Found

**Description:**
The requested resource temporarily resides under a different URI. The client should continue to use the original URI for future requests. This response is typically not cacheable unless specified by headers.

**Example:**
```python
import requests

response = requests.get('https://api.example.com/resource')
if response.status_code == 302:
    print("Resource temporarily moved to:", response.headers['Location'])
```

**Expected Output:**
```
Resource temporarily moved to: http://temp.example.com/resource
```

---

### 10.3.4 303 See Other

**Description:**
The response can be found under a different URI, which should be accessed using a GET method. This is often used for redirecting after a POST request.

**Example:**
```python
response = requests.post('https://api.example.com/form-submit', data={'name': 'Bob'})
if response.status_code == 303:
    print("See other resource at:", response.headers['Location'])
```

**Expected Output:**
```
See other resource at: http://example.com/another-resource
```

---

### 10.3.5 304 Not Modified

**Description:**
The client performed a conditional GET request, but the document has not been modified. The server responds with this status, indicating that the cached version can be used.

**Example:**
```python
url = 'https://api.example.com/resource'
headers = {'If-None-Match': 'some-etag-value'}
response = requests.get(url, headers=headers)

if response.status_code == 304:
    print("Resource not modified; using cached version.")
```

**Expected Output:**
```
Resource not modified; using cached version.
```

### Summary Table

| Status Code | Description          | Example Code                                                   | Expected Output                                  |
|-------------|----------------------|---------------------------------------------------------------|--------------------------------------------------|
| **302**      | Found                | `requests.get(...).status_code == 302`                       | `Resource temporarily moved to: ...`             |
| **303**      | See Other            | `requests.post(...).status_code == 303`                      | `See other resource at: ...`                     |
| **304**      | Not Modified         | `requests.get(..., headers={'If-None-Match': 'etag'})`     | `Resource not modified; using cached version.`    |




### 10.3.6 305 Use Proxy

**Description:**
The requested resource must be accessed through the proxy specified in the Location field. This response must only be generated by origin servers.

**Example:**
```python
response = requests.get('https://api.example.com/resource')
if response.status_code == 305:
    print("Access the resource via proxy at:", response.headers['Location'])
```

**Expected Output:**
```
Access the resource via proxy at: http://proxy.example.com
```

---

### 10.3.7 306 (Unused)

**Description:**
The 306 status code is reserved and was previously used in earlier versions of the specification but is no longer utilized.

**Example:**
```python
response = requests.get('https://api.example.com/resource')
if response.status_code == 306:
    print("This status code is reserved and unused.")
```

**Expected Output:**
```
This status code is reserved and unused.
```

---

### 10.3.8 307 Temporary Redirect

**Description:**
The requested resource resides temporarily under a different URI. The client should continue to use the original URI for future requests.

**Example:**
```python
response = requests.get('https://api.example.com/resource')
if response.status_code == 307:
    print("Temporary redirect to:", response.headers['Location'])
```

**Expected Output:**
```
Temporary redirect to: http://temp.example.com/resource
```

---

### 10.4 Client Error 4xx

**Description:**
The 4xx class of status codes indicates that the client seems to have made an error. The server should provide an explanation of the error.

---

#### 10.4.1 400 Bad Request

**Description:**
The server could not understand the request due to malformed syntax.

**Example:**
```python
response = requests.post('https://api.example.com/resource', data={'invalid_key': 'value'})
if response.status_code == 400:
    print("Bad request:", response.json())
```

**Expected Output:**
```
Bad request: {'error': 'Malformed syntax in request'}
```

---

#### 10.4.2 401 Unauthorized

**Description:**
The request requires user authentication. The server responds with a WWW-Authenticate header.

**Example:**
```python
response = requests.get('https://api.example.com/protected-resource')
if response.status_code == 401:
    print("Unauthorized access:", response.headers['WWW-Authenticate'])
```

**Expected Output:**
```
Unauthorized access: Basic realm="Access to the protected resource"
```

---

#### 10.4.3 402 Payment Required

**Description:**
This code is reserved for future use.

**Example:**
```python
response = requests.get('https://api.example.com/premium-content')
if response.status_code == 402:
    print("Payment required for this resource.")
```

**Expected Output:**
```
Payment required for this resource.
```

---

#### 10.4.4 403 Forbidden

**Description:**
The server understood the request but is refusing to fulfill it. The request should not be repeated.

**Example:**
```python
response = requests.get('https://api.example.com/forbidden-resource')
if response.status_code == 403:
    print("Forbidden:", response.json())
```

**Expected Output:**
```
Forbidden: {'error': 'Access to this resource is denied'}
```

---

#### 10.4.5 404 Not Found

**Description:**
The server has not found anything matching the Request-URI.

**Example:**
```python
response = requests.get('https://api.example.com/nonexistent-resource')
if response.status_code == 404:
    print("Not found:", response.json())
```

**Expected Output:**
```
Not found: {'error': 'Resource not found'}
```

### Summary Table

| Status Code | Description          | Example Code                                                   | Expected Output                                  |
|-------------|----------------------|---------------------------------------------------------------|--------------------------------------------------|
| **305**      | Use Proxy            | `requests.get(...).status_code == 305`                       | `Access the resource via proxy at: ...`         |
| **306**      | (Unused)            | `requests.get(...).status_code == 306`                       | `This status code is reserved and unused.`       |
| **307**      | Temporary Redirect    | `requests.get(...).status_code == 307`                       | `Temporary redirect to: ...`                    |
| **400**      | Bad Request          | `requests.post(...).status_code == 400`                      | `Bad request: ...`                               |
| **401**      | Unauthorized         | `requests.get(...).status_code == 401`                       | `Unauthorized access: ...`                       |
| **402**      | Payment Required      | `requests.get(...).status_code == 402`                       | `Payment required for this resource.`            |
| **403**      | Forbidden            | `requests.get(...).status_code == 403`                       | `Forbidden: ...`                                 |
| **404**      | Not Found            | `requests.get(...).status_code == 404`                       | `Not found: ...`                                 |



### 10.4.6 405 Method Not Allowed

**Description:**
The method specified in the Request-Line is not allowed for the resource identified by the Request-URI. The response must include an `Allow` header with a list of valid methods.

**Example:**
```python
response = requests.post('https://api.example.com/resource')
if response.status_code == 405:
    print("Method not allowed. Allowed methods:", response.headers['Allow'])
```

**Expected Output:**
```
Method not allowed. Allowed methods: GET, OPTIONS
```

---

### 10.4.7 406 Not Acceptable

**Description:**
The resource is unable to generate response entities acceptable according to the `Accept` headers in the request.

**Example:**
```python
response = requests.get('https://api.example.com/resource', headers={'Accept': 'application/xml'})
if response.status_code == 406:
    print("Not acceptable. Available options:", response.json())
```

**Expected Output:**
```
Not acceptable. Available options: {'available': ['application/json', 'text/html']}
```

---

### 10.4.8 407 Proxy Authentication Required

**Description:**
The client must authenticate itself with the proxy. The proxy must return a `Proxy-Authenticate` header.

**Example:**
```python
response = requests.get('https://api.example.com/resource', proxies={'http': 'http://proxy.example.com'})
if response.status_code == 407:
    print("Proxy authentication required:", response.headers['Proxy-Authenticate'])
```

**Expected Output:**
```
Proxy authentication required: Basic realm="Proxy access"
```

---

### 10.4.9 408 Request Timeout

**Description:**
The client did not produce a request within the time that the server was prepared to wait.

**Example:**
```python
response = requests.get('https://api.example.com/resource', timeout=1)
if response.status_code == 408:
    print("Request timed out. Please try again.")
```

**Expected Output:**
```
Request timed out. Please try again.
```

---

### 10.4.10 409 Conflict

**Description:**
The request could not be completed due to a conflict with the current state of the resource.

**Example:**
```python
response = requests.put('https://api.example.com/resource', json={'data': 'conflicting data'})
if response.status_code == 409:
    print("Conflict:", response.json())
```

**Expected Output:**
```
Conflict: {'error': 'Conflict with existing resource state'}
```

---

### 10.4.11 410 Gone

**Description:**
The requested resource is no longer available, and no forwarding address is known.

**Example:**
```python
response = requests.get('https://api.example.com/old-resource')
if response.status_code == 410:
    print("Resource is gone:", response.json())
```

**Expected Output:**
```
Resource is gone: {'error': 'This resource is no longer available'}
```

---

### 10.4.12 411 Length Required

**Description:**
The server refuses to accept the request without a defined `Content-Length`.

**Example:**
```python
response = requests.post('https://api.example.com/resource', data='{"key": "value"}', headers={'Content-Length': ''})
if response.status_code == 411:
    print("Length required: Please specify Content-Length.")
```

**Expected Output:**
```
Length required: Please specify Content-Length.
```

---

### 10.4.13 412 Precondition Failed

**Description:**
One or more request-header fields evaluated to false when tested on the server.

**Example:**
```python
response = requests.get('https://api.example.com/resource', headers={'If-Match': 'invalid-etag'})
if response.status_code == 412:
    print("Precondition failed:", response.json())
```

**Expected Output:**
```
Precondition failed: {'error': 'Precondition failed on the request'}
```

---

### 10.4.14 413 Request Entity Too Large

**Description:**
The server is refusing to process the request because the request entity is larger than the server is willing to process.

**Example:**
```python
response = requests.post('https://api.example.com/upload', data='large data'*10000)
if response.status_code == 413:
    print("Request entity too large.")
```

**Expected Output:**
```
Request entity too large.
```

### Summary Table

| Status Code | Description                | Example Code                                                      | Expected Output                                  |
|-------------|----------------------------|------------------------------------------------------------------|--------------------------------------------------|
| **405**      | Method Not Allowed          | `requests.post(...).status_code == 405`                         | `Method not allowed. Allowed methods: ...`      |
| **406**      | Not Acceptable             | `requests.get(...).status_code == 406`                          | `Not acceptable. Available options: ...`         |
| **407**      | Proxy Authentication Required| `requests.get(...).status_code == 407`                         | `Proxy authentication required: ...`            |
| **408**      | Request Timeout             | `requests.get(...).status_code == 408`                          | `Request timed out. Please try again.`           |
| **409**      | Conflict                   | `requests.put(...).status_code == 409`                          | `Conflict: ...`                                 |
| **410**      | Gone                       | `requests.get(...).status_code == 410`                          | `Resource is gone: ...`                          |
| **411**      | Length Required            | `requests.post(...).status_code == 411`                         | `Length required: ...`                           |
| **412**      | Precondition Failed        | `requests.get(...).status_code == 412`                          | `Precondition failed: ...`                       |
| **413**      | Request Entity Too Large    | `requests.post(...).status_code == 413`                         | `Request entity too large.`                       |


### 10.4.15 414 Request-URI Too Long

**Description:**
The server is refusing to service the request because the Request-URI is longer than it is willing to interpret. This can occur due to improper request conversions or excessive redirection.

**Example:**
```python
response = requests.get('https://api.example.com/resource?param=' + 'a' * 5000)
if response.status_code == 414:
    print("Request-URI is too long.")
```

**Expected Output:**
```
Request-URI is too long.
```

---

### 10.4.16 415 Unsupported Media Type

**Description:**
The server is refusing to service the request because the entity format is not supported by the requested resource for the specified method.

**Example:**
```python
response = requests.post('https://api.example.com/resource', data='{"key": "value"}', headers={'Content-Type': 'text/plain'})
if response.status_code == 415:
    print("Unsupported media type.")
```

**Expected Output:**
```
Unsupported media type.
```

---

### 10.4.17 416 Requested Range Not Satisfiable

**Description:**
The server returns this status if the Range request-header field indicates a range not satisfiable by the current resource.

**Example:**
```python
response = requests.get('https://api.example.com/resource', headers={'Range': 'bytes=1000-2000'})
if response.status_code == 416:
    print("Requested range not satisfiable:", response.headers.get('Content-Range'))
```

**Expected Output:**
```
Requested range not satisfiable: bytes */500
```

---

### 10.4.18 417 Expectation Failed

**Description:**
The expectation given in an `Expect` request-header field could not be met by the server.

**Example:**
```python
response = requests.post('https://api.example.com/resource', headers={'Expect': '100-continue'})
if response.status_code == 417:
    print("Expectation failed.")
```

**Expected Output:**
```
Expectation failed.
```

---

### 10.5 Server Error 5xx

**Description:**
Response status codes beginning with "5" indicate that the server has encountered an error or is incapable of performing the request.

---

### 10.5.1 500 Internal Server Error

**Description:**
The server encountered an unexpected condition preventing it from fulfilling the request.

**Example:**
```python
response = requests.get('https://api.example.com/trigger-error')
if response.status_code == 500:
    print("Internal server error occurred.")
```

**Expected Output:**
```
Internal server error occurred.
```

---

### 10.5.2 501 Not Implemented

**Description:**
The server does not support the functionality required to fulfill the request.

**Example:**
```python
response = requests.request('PATCH', 'https://api.example.com/resource')
if response.status_code == 501:
    print("Not implemented.")
```

**Expected Output:**
```
Not implemented.
```

---

### 10.5.3 502 Bad Gateway

**Description:**
The server received an invalid response from an upstream server while acting as a gateway or proxy.

**Example:**
```python
response = requests.get('https://api.example.com/proxy')
if response.status_code == 502:
    print("Bad gateway.")
```

**Expected Output:**
```
Bad gateway.
```

---

### 10.5.4 503 Service Unavailable

**Description:**
The server is temporarily unable to handle the request due to overload or maintenance. The response may include a `Retry-After` header.

**Example:**
```python
response = requests.get('https://api.example.com/resource')
if response.status_code == 503:
    retry_after = response.headers.get('Retry-After', 'no retry time specified')
    print("Service unavailable. Retry after:", retry_after)
```

**Expected Output:**
```
Service unavailable. Retry after: 3600
```

---

### 10.5.5 504 Gateway Timeout

**Description:**
The server did not receive a timely response from the upstream server it needed to access to complete the request.

**Example:**
```python
response = requests.get('https://api.example.com/gateway')
if response.status_code == 504:
    print("Gateway timeout.")
```

**Expected Output:**
```
Gateway timeout.
```

---

### 10.5.6 505 HTTP Version Not Supported

**Description:**
The server does not support the HTTP protocol version used in the request.

**Example:**
```python
response = requests.get('https://api.example.com/resource', headers={'HTTP-Version': 'HTTP/1.0'})
if response.status_code == 505:
    print("HTTP version not supported.")
```

**Expected Output:**
```
HTTP version not supported.
```

### Summary Table

| Status Code | Description                      | Example Code                                                      | Expected Output                                  |
|-------------|----------------------------------|------------------------------------------------------------------|--------------------------------------------------|
| **414**      | Request-URI Too Long            | `requests.get(...).status_code == 414`                         | `Request-URI is too long.`                       |
| **415**      | Unsupported Media Type           | `requests.post(...).status_code == 415`                         | `Unsupported media type.`                         |
| **416**      | Requested Range Not Satisfiable  | `requests.get(...).status_code == 416`                          | `Requested range not satisfiable: ...`           |
| **417**      | Expectation Failed               | `requests.post(...).status_code == 417`                         | `Expectation failed.`                             |
| **500**      | Internal Server Error            | `requests.get(...).status_code == 500`                          | `Internal server error occurred.`                 |
| **501**      | Not Implemented                  | `requests.request(...).status_code == 501`                      | `Not implemented.`                                |
| **502**      | Bad Gateway                       | `requests.get(...).status_code == 502`                          | `Bad gateway.`                                    |
| **503**      | Service Unavailable              | `requests.get(...).status_code == 503`                          | `Service unavailable. Retry after: ...`          |
| **504**      | Gateway Timeout                  | `requests.get(...).status_code == 504`                          | `Gateway timeout.`                                |
| **505**      | HTTP Version Not Supported       | `requests.get(...).status_code == 505`                          | `HTTP version not supported.`                     |
