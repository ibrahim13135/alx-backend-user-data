## HTTP header Authorization

The HTTP Authorization request header provides credentials that authenticate a user agent with a server, allowing access to a protected resource.

### Process
1. **Initial Request**: The user agent attempts to access a protected resource without credentials.
2. **Server Response**: The server responds with a 401 Unauthorized message, including at least one `WWW-Authenticate` header.
3. **User Agent Action**: The user agent selects the most secure authentication scheme, prompts the user for their credentials, and re-requests the resource with the encoded credentials in the `Authorization` header.

### Cross-Origin Redirects
This header is stripped from cross-origin redirects.

### General HTTP Authentication Framework
This header can be used with several authentication schemes.

### Header Type
- **Type**: Request header
- **Forbidden Header Name**: No

### Syntax
```HTTP
Authorization: <auth-scheme> <authorization-parameters>
```

### Examples

#### Basic Authentication
```HTTP
Authorization: Basic <credentials>
```

#### Digest Authentication
```HTTP
Authorization: Digest username=<username>,
    realm="<realm>",
    uri="<url>",
    algorithm=<algorithm>,
    nonce="<nonce>",
    nc=<nc>,
    cnonce="<cnonce>",
    qop=<qop>,
    response="<response>",
    opaque="<opaque>"
```

### Directives

#### `<auth-scheme>`
Defines how the credentials are encoded. Common schemes: Basic, Digest, Negotiate, AWS4-HMAC-SHA256.

#### `Basic`
- **`<credentials>`**: Encoded according to the specified scheme.

#### `Digest`
- **`<response>`**: Hex digits proving the user knows a password. Encodes username, password, realm, cnonce, qop, nc, etc.
- **`username`**: User's name in plain text or hash code. Use `username*` if special characters are present.
- **`username*`**: Formatted using RFC5987 if `username` can't encode the name and `userhash` is false.
- **`uri`**: Effective Request URI.
- **`realm`**: Realm of the requested username/password.
- **`opaque`**: Value from the `WWW-Authenticate` response.
- **`algorithm`**: Used to calculate the digest. Must be supported by the `WWW-Authenticate` response.
- **`qop`**: Quality of protection applied to the message (`auth` or `auth-int`).
- **`cnonce`**: ASCII-only string for mutual authentication and message integrity protection.
- **`nc`**: Hexadecimal count of requests with the current `cnonce`.
- **`userhash`** (Optional): `true` if the username has been hashed. Default is `false`.

### Example of Basic Authentication
For "Basic" authentication:
1. Combine username and password with a colon: `aladdin:opensesame`.
2. Encode the string in base64: `YWxhZGRpbjpvcGVuc2VzYW1l`.

```HTTP
Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l
```

**Warning**: Base64-encoding can be easily reversed, so Basic authentication is insecure. Always use HTTPS with authentication.

### See Also
- **HTTP authentication**: For configuring Apache or Nginx servers to password-protect your site with HTTP basic authentication.

### Specifications
- **Specification**: HTTP Semantics

### Browser Compatibility

#### Authorization
| Browser           | Support    |
|-------------------|------------|
| Chrome            | Full       |
| Edge              | Full       |
| Firefox           | Full       |
| Opera             | Full       |
| Safari            | Full       |
| Chrome Android    | Full       |
| Firefox for Android | Full     |
| Opera Android     | Full       |
| Safari on iOS     | Full       |
| Samsung Internet  | Full       |
| WebView Android   | Full       |

#### Basic Authentication
| Browser           | Support    |
|-------------------|------------|
| Chrome            | Full       |
| Edge              | Full       |
| Firefox           | Full       |
| Opera             | Full       |
| Safari            | Full       |
| Chrome Android    | Full       |
| Firefox for Android | Full     |
| Opera Android     | Full       |
| Safari on iOS     | Full       |
| Samsung Internet  | Full       |
| WebView Android   | Full       |

#### Digest Authentication
| Browser           | Support    |
|-------------------|------------|
| Chrome            | Full       |
| Edge              | Full       |
| Firefox           | Full       |
| Opera             | Full       |
| Safari            | ?          |
| Chrome Android    | Full       |
| Firefox for Android | Full     |
| Opera Android     | Full       |
| Safari on iOS     | ?          |
| Samsung Internet  | Full       |
| WebView Android   | Full       |

### Additional Information
- **SHA2-256 Digest Authentication**: Supported by some browsers.
- **SHA2-512 Digest Authentication**: Generally not supported.
- **MD5 Digest Authentication**: Widely supported.
- **NTLM Authentication**: Widely supported.
- **Negotiate (Kerberos) Authentication**: Widely supported.

#### Authorization Header Removed from Cross-Origin Redirects
- Not supported by most browsers.

**Legend**: Full support, No support, Compatibility unknown


### Basic Authentication Example

**Request:**
```HTTP
GET /protected-resource HTTP/1.1
Host: example.com
Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l
```

**Explanation:**
- The `Authorization` header uses the "Basic" authentication scheme.
- `YWxhZGRpbjpvcGVuc2VzYW1l` is the base64 encoded form of `aladdin:opensesame`.

**Response (if successful):**
```HTTP
HTTP/1.1 200 OK
Content-Type: text/html

<!-- The protected content goes here -->
```

**Response (if unauthorized):**
```HTTP
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Example"

<!DOCTYPE html>
<html>
<head><title>401 Unauthorized</title></head>
<body>
<h1>Unauthorized</h1>
<p>You must provide valid credentials to access this resource.</p>
</body>
</html>
```

### Digest Authentication Example

**Request:**
```HTTP
GET /protected-resource HTTP/1.1
Host: example.com
Authorization: Digest username="Mufasa",
    realm="Example",
    uri="/protected-resource",
    algorithm=MD5,
    nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093",
    nc=00000001,
    cnonce="0a4f113b",
    qop=auth,
    response="6629fae49393a05397450978507c4ef1",
    opaque="5ccc069c403ebaf9f0171e9517f40e41"
```

**Explanation:**
- The `Authorization` header uses the "Digest" authentication scheme.
- `username="Mufasa"` is the username.
- `realm="Example"` specifies the protection space.
- `uri="/protected-resource"` is the requested URI.
- `algorithm=MD5` specifies the algorithm for hashing.
- `nonce`, `nc`, `cnonce`, `qop`, `response`, and `opaque` are all part of the digest mechanism to provide security.

**Response (if successful):**
```HTTP
HTTP/1.1 200 OK
Content-Type: text/html

<!-- The protected content goes here -->
```

**Response (if unauthorized):**
```HTTP
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Digest realm="Example",
    qop="auth",
    nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093",
    opaque="5ccc069c403ebaf9f0171e9517f40e41"

<!DOCTYPE html>
<html>
<head><title>401 Unauthorized</title></head>
<body>
<h1>Unauthorized</h1>
<p>You must provide valid credentials to access this resource.</p>
</body>
</html>
```

### Bearer Token Authentication Example

**Request:**
```HTTP
GET /protected-resource HTTP/1.1
Host: example.com
Authorization: Bearer mF_9.B5f-4.1JqM
```

**Explanation:**
- The `Authorization` header uses the "Bearer" authentication scheme.
- `mF_9.B5f-4.1JqM` is the bearer token.

**Response (if successful):**
```HTTP
HTTP/1.1 200 OK
Content-Type: text/html

<!-- The protected content goes here -->
```

**Response (if unauthorized):**
```HTTP
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="Example",
    error="invalid_token",
    error_description="The access token expired"

<!DOCTYPE html>
<html>
<head><title>401 Unauthorized</title></head>
<body>
<h1>Unauthorized</h1>
<p>Your access token is invalid or expired.</p>
</body>
</html>
```

### AWS4-HMAC-SHA256 Example

**Request:**
```HTTP
GET /protected-resource HTTP/1.1
Host: example.com
Authorization: AWS4-HMAC-SHA256 Credential=AKIDEXAMPLE/20230709/us-east-1/service/aws4_request, 
    SignedHeaders=host;x-amz-date, 
    Signature=4f44d0dfecea84faab776dd26442b6ec5e7c9ea5f1e3e3b1f839a0ff739b6f15
```

**Explanation:**
- The `Authorization` header uses the "AWS4-HMAC-SHA256" authentication scheme.
- `Credential` specifies the access key and the date.
- `SignedHeaders` lists the headers that are included in the signature.
- `Signature` is the computed signature.

**Response (if successful):**
```HTTP
HTTP/1.1 200 OK
Content-Type: text/html

<!-- The protected content goes here -->
```

**Response (if unauthorized):**
```HTTP
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "code": "SignatureDoesNotMatch",
  "message": "The request signature we calculated does not match the signature you provided."
}
```

These examples illustrate how different authorization schemes work in HTTP requests and what kind of responses you might receive.
