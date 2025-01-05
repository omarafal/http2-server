huffman_table = {
    "10100": " ",
    "1111111000": "!",
    "1111111001": "\"",
    "111111111010": "#",
    "1111111111001": "$",
    "10101": "%",
    "11111000": "&",
    "11111111010": "'",
    "1111111010": "(",
    "1111111011": ")",
    "11111001": "*",
    "11111111011": "+",
    "11111010": ",",
    "10110": "-",
    "10111": ".",
    "11000": "/",
    "00000": "0",
    "00001": "1",
    "00010": "2",
    "11001": "3",
    "11010": "4",
    "11011": "5",
    "11100": "6",
    "11101": "7",
    "11110": "8",
    "11111": "9",
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
huffman_table_rev = {
    " ": "010100",
    "!": "1111111000",
    "\"": "1111111001",
    "#": "111111111010",
    "$": "1111111111001",
    "%": "010101",
    "&": "11111000",
    "'": "11111111010",
    "(": "1111111010",
    ")": "1111111011",
    "*": "11111001",
    "+": "11111111011",
    ",": "11111010",
    "-": "010110",
    ".": "010111",
    "/": "011000",
    "0": "00000",
    "1": "00001",
    "2": "00010",
    "3": "011001",
    "4": "011010",
    "5": "011011",
    "6": "011100",
    "7": "011101",
    "8": "011110",
    "9": "011111",
    ":": "1011100",
    ";": "11111011",
    "<": "111111111111100",
    "=": "100000",
    ">": "1111111111011",
    "?": "1111111100",
    "@": "11111111111010",
    "A": "100001",
    "B": "1011101",
    "C": "1011110",
    "D": "1011111",
    "E": "1100000",
    "F": "1100001",
    "G": "1100010",
    "H": "1100011",
    "I": "1100100",
    "J": "1100101",
    "K": "1100110",
    "L": "1100111",
    "M": "1101000",
    "N": "1101001",
    "O": "1101010",
    "P": "1101011",
    "Q": "1101100",
    "R": "1101101",
    "S": "1101110",
    "T": "1101111",
    "U": "1110000",
    "V": "1110001",
    "W": "1110010",
    "X": "11111100",
    "Y": "1110011",
    "Z": "11111101",
    "[": "11111111111011",
    "\\": "111111111111111000",
    "]": "11111111111100",
    "^": "111111111111100",
    "_": "100010",
    "`": "111111111111101",
    "a": "00011",
    "b": "100011",
    "c": "00100",
    "d": "100100",
    "e": "00101",
    "f": "100101",
    "g": "100110",
    "h": "100111",
    "i": "00110",
    "j": "1110100",
    "k": "1110101",
    "l": "101000",
    "m": "101001",
    "n": "101010",
    "o": "00111",
    "p": "101011",
    "q": "1110110",
    "r": "101100",
    "s": "01000",
    "t": "01001",
    "u": "101101",
    "v": "1110111",
    "w": "1111000",
    "x": "1111001",
    "y": "1111010",
    "z": "1111011",
    "{": "111111111111110",
    "|": "111111111100",
    "}": "111111111111101",
    "~": "1111111111101",
}

STATIC_TABLE = {
    0: {},
    1: {"authority": ""},
    2: {"method": "GET"},
    3: {"method": "POST"},
    4: {"path": "/"},
    5: {"path": "/index.html"},
    6: {"path": ""},
    7: {"scheme": "http"},
    8: {"scheme": "https"},
    9: {"status": ""},
    10: {"status": "200"},
    11: {"status": "204"},
    12: {"status": "206"},
    13: {"status": "304"},
    14: {"status": "400"},
    15: {"status": "404"},
    16: {"status": "500"},
    17: {"accept-charset": ""},
    18: {"accept-encoding": "gzip, deflate"},
    19: {"accept-ranges": ""},
    20: {"accept": ""},
    21: {"host": ""},
    22: {"stream-identifier": ""},
    23: {"content-type": "text/html"},
    24: {"content-type": "text/css"},
    25: {"content-type": "text/js"},
    26: {"content-length": ""},
    27: {"date": ""}

}

def encode(request):
    msg = b""
    st = list(STATIC_TABLE.values())

    for key, value in request.items():
        try:    
            indx = st.index({key: value})
        except ValueError:
            indx = st.index({key: ""})

        indx_byte = indx.to_bytes((indx.bit_length() + 7) // 8, 'big')

        header = st[indx]

        if header[key] != "": # Means it exists in static table and can just put number
            msg += indx_byte

        else:
            size = len(str(value)) # Length of the value
            size_byte = size.to_bytes((size.bit_length() + 7) // 8, 'big')

            msg += indx_byte
            msg += size_byte

            # use the static table to encode the values
            for char in str(value):
                val = int(huffman_table_rev[char], 2)

                byte_length = (len(huffman_table_rev[char]) + 7) // 8

                byte_val = val.to_bytes(byte_length, byteorder='big')

                msg += byte_val
    
    return msg

def find_longest_match(encoded_string, huffman_table):
    match = ""
    longest_key = None

    # Iterate through the characters in the encoded string
    for char in encoded_string:
        match += char
        
        if match in huffman_table:
            longest_key = match  # Update the longest key if found

    return longest_key, huffman_table[longest_key] if longest_key else None

def decode(msg):
    decoded = {}

    is_key = True
    length = 0
    val = ""
    
    for byte in msg:
        if is_key:
            header = STATIC_TABLE[int(byte)]

            key = list(header.keys())[0]
            val = list(header.values())[0]

            if val != "":
                decoded[key] = val

            else:
                is_key = False
        
        else:
            if length == 0:
                val = "" # reset val
                length = byte
                continue
            
            bin_byte = bin(byte)[2:].zfill(5)  # Minimum length of 5

            decoded_char = huffman_table[str(bin_byte)]

            val += decoded_char
            length -= 1
            if length == 0:
                # this time it finished
                decoded[key] = val
                is_key = True

    return decoded
