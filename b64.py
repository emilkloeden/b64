"""
b64.py

A completely pointless, pure python, no imports implementation of the
base64 encoding and decoding algorithms.

"""

ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ascii_lowercase = ascii_uppercase.lower()
digits = "0123456789"

BASE64_CHARSET = list(ascii_uppercase) + list(ascii_lowercase) + list(digits)
BASE64_CHARMAP = {i: u for i, u in enumerate(BASE64_CHARSET) }
REVERSE_BASE64_CHARMAP = {v:k for k, v in BASE64_CHARMAP.items()}


def __convert_to_bytes(input_: str or bytes) -> bytes:
    if isinstance(input_, bytes):
        return input_
    return bytes(input_, "utf-8", "strict")

def __convert_to_joined_octets_string(bytes_: bytes) -> str:
    return "".join([f"{b:>08b}" for b in bytes_])


def __convert_to_sextet_strings_and_padding(joined_octets_string: str): #-> tuple(list(str), int):
    sextet_strings = [joined_octets_string[i:i+6] for i in range(0, len(joined_octets_string), 6)]
    if len(sextet_strings):
        padding = (6 - len(sextet_strings[-1])) // 2  # if len is 6, then 0, if 4 then 1, if 2 then 2
    else:
        padding = 0
    return (sextet_strings, padding)

def __convert_to_base64_string(joined_octets_string: str) ->str:
    sextet_strings, padding = __convert_to_sextet_strings_and_padding(joined_octets_string)
    sextet_ints = [int(s, 2) for s in sextet_strings]
        
    return "".join([BASE64_CHARSET[i] for i in sextet_ints]) + padding * "="
    
def decode(base64_input: str) -> bytes:
    "Decode a base64 string to bytes (an arbitrary choice since we don't know if it should be bytes or a string)"
    # Remove trailing '=' characters, probably shouldn't do this and instead check for correctness
    padding_stripped_input = base64_input.rstrip("=")

    # Convert each character to it's integer mapping in the range 0-63
    ints = [REVERSE_BASE64_CHARMAP[c] for c in padding_stripped_input]
    
    # Convert each int into a 6-digit binary string representation...
    # ... and combine all strings into one long string 
    bin_string = "".join([f"{i:>06b}" for i in ints])
    
    # If our string is empty, return an empty byte string
    if not len(bin_string):
        return b""
    
    # Split the long string into a list of 8-digit long binary strings
    octet_strings = [bin_string[b:b+8] for b in range(0, len(bin_string), 8)]
    
    # Convert each octet binary string into an int
    ints = [int(o, 2) for o in octet_strings]

    # ...and then into a char
    chars = [chr(i) for i in ints]
    
    # Strip a trailing null byte - this is not the correct way to do this.
    string = "".join(chars if chars[-1] != '\x00' else chars[:-1])

    # Return our string as a bytes object
    return string.encode("utf-8")


def encode(input_: str or bytes) -> str:
    "Return a Base64 encoded string from string or bytes."
    bytes_ = __convert_to_bytes(input_)
    joined_octets_string = __convert_to_joined_octets_string(bytes_)
    return __convert_to_base64_string(joined_octets_string)