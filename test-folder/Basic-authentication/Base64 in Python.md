The `base64` module in Python provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data. The module supports several encodings specified in RFC 3548, including Base16, Base32, and Base64, as well as de-facto standard encodings like Ascii85 and Base85. Here is a detailed explanation of each function along with examples and their outputs.

### Modern Interface

#### Base64 Encoding and Decoding

1. **`base64.b64encode(s, altchars=None)`**
   - Encodes the bytes-like object `s` using Base64 and returns the encoded bytes.
   - `altchars` allows specifying an alternative alphabet for the `+` and `/` characters, useful for generating URL or filesystem safe Base64 strings.

```python
import base64

# Encoding
data = b'data to be encoded'
encoded = base64.b64encode(data)
print(encoded)  # Output: b'ZGF0YSB0byBiZSBlbmNvZGVk'

# Decoding
decoded = base64.b64decode(encoded)
print(decoded)  # Output: b'data to be encoded'
```

2. **`base64.b64decode(s, altchars=None, validate=False)`**
   - Decodes the Base64 encoded bytes-like object or ASCII string `s` and returns the decoded bytes.
   - `altchars` specifies an alternative alphabet.
   - If `validate` is `True`, non-alphabet characters in the input result in a `binascii.Error`.

```python
# Decoding with validation
try:
    decoded_with_validation = base64.b64decode(encoded, validate=True)
    print(decoded_with_validation)  # Output: b'data to be encoded'
except binascii.Error as e:
    print(f"Error: {e}")
```

3. **`base64.standard_b64encode(s)` and `base64.standard_b64decode(s)`**
   - Similar to `b64encode` and `b64decode`, but using the standard Base64 alphabet.

```python
# Standard Base64 Encoding
standard_encoded = base64.standard_b64encode(data)
print(standard_encoded)  # Output: b'ZGF0YSB0byBiZSBlbmNvZGVk'

# Standard Base64 Decoding
standard_decoded = base64.standard_b64decode(standard_encoded)
print(standard_decoded)  # Output: b'data to be encoded'
```

4. **`base64.urlsafe_b64encode(s)` and `base64.urlsafe_b64decode(s)`**
   - Encodes and decodes using a URL- and filesystem-safe alphabet, substituting `-` for `+` and `_` for `/`.

```python
# URL-safe Base64 Encoding
urlsafe_encoded = base64.urlsafe_b64encode(data)
print(urlsafe_encoded)  # Output: b'ZGF0YSB0byBiZSBlbmNvZGVk'

# URL-safe Base64 Decoding
urlsafe_decoded = base64.urlsafe_b64decode(urlsafe_encoded)
print(urlsafe_decoded)  # Output: b'data to be encoded'
```

#### Base32 Encoding and Decoding

1. **`base64.b32encode(s)`**
   - Encodes the bytes-like object `s` using Base32 and returns the encoded bytes.

```python
# Base32 Encoding
encoded_base32 = base64.b32encode(data)
print(encoded_base32)  # Output: b'ORUGS4ZANFZSAYJAORSXI2LOM4======'

# Base32 Decoding
decoded_base32 = base64.b32decode(encoded_base32)
print(decoded_base32)  # Output: b'data to be encoded'
```

2. **`base64.b32decode(s, casefold=False, map01=None)`**
   - Decodes the Base32 encoded bytes-like object or ASCII string `s` and returns the decoded bytes.
   - `casefold` allows a lowercase alphabet.
   - `map01` specifies optional mapping of the digit `1` to `I` or `L`.

```python
# Base32 Decoding with casefold and map01
decoded_base32_casefold = base64.b32decode(encoded_base32, casefold=True, map01='L')
print(decoded_base32_casefold)  # Output: b'data to be encoded'
```

#### Base16 Encoding and Decoding

1. **`base64.b16encode(s)`**
   - Encodes the bytes-like object `s` using Base16 and returns the encoded bytes.

```python
# Base16 Encoding
encoded_base16 = base64.b16encode(data)
print(encoded_base16)  # Output: b'6461746120746F20626520656E636F646564'

# Base16 Decoding
decoded_base16 = base64.b16decode(encoded_base16)
print(decoded_base16)  # Output: b'data to be encoded'
```

2. **`base64.b16decode(s, casefold=False)`**
   - Decodes the Base16 encoded bytes-like object or ASCII string `s` and returns the decoded bytes.
   - `casefold` allows a lowercase alphabet.

```python
# Base16 Decoding with casefold
decoded_base16_casefold = base64.b16decode(encoded_base16, casefold=True)
print(decoded_base16_casefold)  # Output: b'data to be encoded'
```

#### Ascii85 and Base85 Encoding and Decoding

1. **`base64.a85encode(b, *, foldspaces=False, wrapcol=0, pad=False, adobe=False)`**
   - Encodes the bytes-like object `b` using Ascii85 and returns the encoded bytes.
   - `foldspaces` uses a special short sequence `y` for 4 consecutive spaces.
   - `wrapcol` adds newline characters.
   - `pad` pads the input to a multiple of 4 bytes before encoding.
   - `adobe` frames the encoded byte sequence with `<~` and `~>`.

```python
# Ascii85 Encoding
encoded_a85 = base64.a85encode(data)
print(encoded_a85)  # Output: b'@<)A;ElR*D<PE7~j'

# Ascii85 Decoding
decoded_a85 = base64.a85decode(encoded_a85)
print(decoded_a85)  # Output: b'data to be encoded'
```

2. **`base64.a85decode(b, *, foldspaces=False, adobe=False, ignorechars=b' \t\n\r\v')`**
   - Decodes the Ascii85 encoded bytes-like object or ASCII string `b` and returns the decoded bytes.
   - `foldspaces` accepts the `y` short sequence.
   - `adobe` indicates Adobe Ascii85 format.
   - `ignorechars` specifies characters to ignore.

```python
# Ascii85 Decoding with adobe and foldspaces
decoded_a85_adobe = base64.a85decode(encoded_a85, adobe=True, foldspaces=True)
print(decoded_a85_adobe)  # Output: b'data to be encoded'
```

3. **`base64.b85encode(b, pad=False)`**
   - Encodes the bytes-like object `b` using Base85 and returns the encoded bytes.
   - `pad` pads the input to a multiple of 4 bytes before encoding.

```python
# Base85 Encoding
encoded_b85 = base64.b85encode(data)
print(encoded_b85)  # Output: b'FCfN8~#P/CKI'

# Base85 Decoding
decoded_b85 = base64.b85decode(encoded_b85)
print(decoded_b85)  # Output: b'data to be encoded'
```

#### Legacy Interface

1. **`base64.decode(input, output)`**
   - Decodes the contents of the binary input file and writes the resulting binary data to the output file.

2. **`base64.decodebytes(s)`**
   - Decodes the bytes-like object `s`, which must contain one or more lines of base64 encoded data, and returns the decoded bytes.

```python
# Legacy Base64 Decoding
encoded_legacy = b'ZGF0YSB0byBiZSBlbmNvZGVk'
decoded_legacy = base64.decodebytes(encoded_legacy)
print(decoded_legacy)  # Output: b'data to be encoded'
```

3. **`base64.encode(input, output)`**
   - Encodes the contents of the binary input file and writes the resulting base64 encoded data to the output file.

4. **`base64.encodebytes(s)`**
   - Encodes the bytes-like object `s`, which can contain arbitrary binary data, and returns bytes containing the base64-encoded data.

```python
# Legacy Base64 Encoding
encoded_legacy = base64.encodebytes(data)
print(encoded_legacy)  # Output: b'ZGF0YSB0byBiZSBlbmNvZGVk\n'
```

### Summary
The `base64` module in Python provides several functions for encoding and decoding data using different base encodings, such as Base16, Base32, Base64, Ascii85, and Base85. These encodings are useful for safely transmitting binary data over mediums that only support text, such as emails and URLs. The module offers a modern interface with various functions tailored to different use cases, and a legacy interface for backward compatibility.
