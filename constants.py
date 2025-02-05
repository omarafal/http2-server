STATUS = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    226: "IM Used",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a Teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required"
}

FORBIDDEN = ["/for.html"]
UNAUTHORIZED = ["/unauthorized.html"]
REDIRECTS = {
    "/old-page": ("/new-page.html", True),  # 301 Moved Permanently
    "/temp-page": ("/temporary-page.html", False),  # 302 Found
}
NO_CONTENT_PATHS = ["/ping", "/delete-item"]

header_table = [
    "",
    ":authority",
    ":method: GET",
    ":method: POST",
    ":path: /",
    ":path: index.html",
    ":scheme: http",
    ":scheme: https"
]

huffman_table = {
        "010100": " ",
        "1111111000": "!",
        "1111111001": "\"",
        "111111111010": "#",
        "1111111111001": "$",
        "010101": "%",
        "11111000": "&",
        "11111111010": "'",
        "1111111010": "(",
        "1111111011": ")",
        "11111001": "*",
        "11111111011": "+",
        "11111010": ",",
        "010110": "-",
        "010111": ".",
        "011000": "/",
        "00000": "0",
        "00001": "1",
        "00010": "2",
        "011001": "3",
        "011010": "4",
        "011011": "5",
        "011100": "6",
        "011101": "7",
        "011110": "8",
        "011111": "9",
        "1011100": ":",
        "11111011": ";",
        "111111111111100": "<",
        "100000": "=",
        "1111111111011": ">",
        "1111111100": "?",
        "11111111111010": "@",
        "100001": "A",
        "1011101": "B",
        "1011110": "C",
        "1011111": "D",
        "1100000": "E",
        "1100001": "F",
        "1100010": "G",
        "1100011": "H",
        "1100100": "I",
        "1100101": "J",
        "1100110": "K",
        "1100111": "L",
        "1101000": "M",
        "1101001": "N",
        "1101010": "O",
        "1101011": "P",
        "1101100": "Q",
        "1101101": "R",
        "1101110": "S",
        "1101111": "T",
        "1110000": "U",
        "1110001": "V",
        "1110010": "W",
        "11111100": "X",
        "1110011": "Y",
        "11111101": "Z",
        "11111111111011": "[",
        "111111111111111000": "\\",
        "11111111111100": "]",
        "111111111111100": "^",
        "100010": "_",
        "111111111111101": "`",
        "00011": "a",
        "100011": "b",
        "00100": "c",
        "100100": "d",
        "00101": "e",
        "100101": "f",
        "100110": "g",
        "100111": "h",
        "00110": "i",
        "1110100": "j",
        "1110101": "k",
        "101000": "l",
        "101001": "m",
        "101010": "n",
        "00111": "o",
        "101011": "p",
        "1110110": "q",
        "101100": "r",
        "01000": "s",
        "01001": "t",
        "101101": "u",
        "1110111": "v",
        "1111000": "w",
        "1111001": "x",
        "1111010": "y",
        "1111011": "z",
        "111111111111110": "{",
        "111111111100": "|",
        "111111111111101": "}",
        "1111111111101": "~",
    }