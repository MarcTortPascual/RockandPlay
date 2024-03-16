encode_ascii_dict = {
    "@" : "%40" ,
    "á" : "%c3%a1",
    "é" : "%c3%a9",
    "í" : "%c3%ad",
    "ó" : "%c3%b3",
    "ú" : "%c3%ba%0d%0a",
    " " : "+"
}

def encode_ascii(string: str) -> str:
    for char in encode_ascii_dict:
        string = string.replace(char, encode_ascii_dict[char])
    return string
ascii_dict = {
    "%40": "@",
    "%c3%a1": "á",
    "%c3%a9": "é",
    "%c3%ad": "í",
    "%c3%b3": "ó",
    "%c3%ba%0d%0a": "ú",
    "+": " "
}

def convert_ascii(string: str) -> str:
    for char in ascii_dict:
        string = string.replace(char, ascii_dict[char])
    return string