from constants import header_table, huffman_table
import math

def decode_huffman(binary_str):
    # Define the Huffman table as a dictionary {bit_string: character}
    # huffman_table = {
    #     "010100": " ",
    #     "1111111000": "!",
    #     "1111111001": "\"",
    #     "111111111010": "#",
    #     "1111111111001": "$",
    #     "010101": "%",
    #     "11111000": "&",
    #     "11111111010": "'",
    #     "1111111010": "(",
    #     "1111111011": ")",
    #     "11111001": "*",
    #     "11111111011": "+",
    #     "11111010": ",",
    #     "010110": "-",
    #     "010111": ".",
    #     "011000": "/",
    #     "00000": "0",
    #     "00001": "1",
    #     "00010": "2",
    #     "011001": "3",
    #     "011010": "4",
    #     "011011": "5",
    #     "011100": "6",
    #     "011101": "7",
    #     "011110": "8",
    #     "011111": "9",
    #     "1011100": ":",
    #     "11111011": ";",
    #     "111111111111100": "<",
    #     "100000": "=",
    #     "1111111111011": ">",
    #     "1111111100": "?",
    #     "11111111111010": "@",
    #     "100001": "A",
    #     "1011101": "B",
    #     "1011110": "C",
    #     "1011111": "D",
    #     "1100000": "E",
    #     "1100001": "F",
    #     "1100010": "G",
    #     "1100011": "H",
    #     "1100100": "I",
    #     "1100101": "J",
    #     "1100110": "K",
    #     "1100111": "L",
    #     "1101000": "M",
    #     "1101001": "N",
    #     "1101010": "O",
    #     "1101011": "P",
    #     "1101100": "Q",
    #     "1101101": "R",
    #     "1101110": "S",
    #     "1101111": "T",
    #     "1110000": "U",
    #     "1110001": "V",
    #     "1110010": "W",
    #     "11111100": "X",
    #     "1110011": "Y",
    #     "11111101": "Z",
    #     "11111111111011": "[",
    #     "111111111111111000": "\\",
    #     "11111111111100": "]",
    #     "111111111111100": "^",
    #     "100010": "_",
    #     "111111111111101": "`",
    #     "00011": "a",
    #     "100011": "b",
    #     "00100": "c",
    #     "100100": "d",
    #     "00101": "e",
    #     "100101": "f",
    #     "100110": "g",
    #     "100111": "h",
    #     "00110": "i",
    #     "1110100": "j",
    #     "1110101": "k",
    #     "101000": "l",
    #     "101001": "m",
    #     "101010": "n",
    #     "00111": "o",
    #     "101011": "p",
    #     "1110110": "q",
    #     "101100": "r",
    #     "01000": "s",
    #     "01001": "t",
    #     "101101": "u",
    #     "1110111": "v",
    #     "1111000": "w",
    #     "1111001": "x",
    #     "1111010": "y",
    #     "1111011": "z",
    #     "111111111111110": "{",
    #     "111111111100": "|",
    #     "111111111111101": "}",
    #     "1111111111101": "~",
    # }

    # # Convert the input bytes to a binary string
    # binary_str = ''.join(f'{byte:08b}' for byte in encoded_bytes)

    # print(f"BITS: {binary_str}\n-------------------\n")

    # Decode the binary string using the Huffman table
    decoded_str = ""
    temp = ""
    for bit in binary_str:
        temp += bit
        if temp in huffman_table:
            decoded_str += huffman_table[temp]
            # print(F"FOUND CHAR: {decoded_str}")
            temp = ""  # Reset temp for the next character

    return decoded_str

# Example usage
# encoded_response = b"\x00\x01\x1b\x01\x25\x00\x00\x00\x03\x00\x00\x00\x00\x29\x82\x04\x81cA\x8a\xa0\xe4\x1d\x13\x9d\t\xb8\xf3M3\x87z\xbc\xd0\x7ff\xa2\x81\xb0\xda\xe0S\xfa\xe4j\xa4?\x84)\xa7z\x81\x02\xe0\xfbS\x91\xaaq\xaf\xb5<\xb8\xd7\xda\x96w\xb8\x16Y\\\x1f\xda\x98\x8aN\xa7`@\x08\x00\x10\x05L&\xb0\xb2\x9f\xcb\x01e\x95\xc1S\xb0I|\xa5\x89\xd3M\x1fC\xae\xba\x0cA\xa4\xc7\xa9\x8f3\xa6\x9a?\xdf\x9ah\xfa\x1du\xd0b\r&=Ly\xa6\x8f\xbe\xd0\x01w\xfe\xbeX\xf9\xfb\xed\x00\x17{Q\x8b-Kp\xdd\xf4Z\xbe\xfb@\x05\xdbP\x92\x9b\xd9\xab\xfaRB\xcb@\xd2_\xa5#\xb3\xe9OhL\x9f@\x92\xb6\xb9\xac\x1c\x85X\xd5 \xa4\xb6\xc2\xada{ZT%\x1f\x81\x0f@\x8aAH\xb4\xa5I'ZB\xa1?\x86\x90\xe4\xb6\x92\xd4\x9f@\x8aAH\xb4\xa5I'Z\x93\xc8_\x86\xa8}\xcd0\xd2_@\x8aAH\xb4\xa5I'Y\x06I\x7f\x83\xa8\xf5\x17@\x8aAH\xb4\xa5I'Z\xd4\x16\xcf\x82\xff\x03@\x86\xae\xc3\x1e\xc3'\xd7\x85\xb6\x00"

# \x00\x01\x1b\x01%\x00\x00\x00\x03\x00\x00\x00\x00)\x82\x04

# assume that we removed headers
encoded_response = b"\x81cA\x8a\xa0\xe4\x1d\x13\x9d\t\xb8\xf3M3\x87z\xbc\xd0\x7ff\xa2\x81\xb0\xda\xe0S\xfa\xe4j\xa4?\x84)\xa7z\x81\x02\xe0\xfbS\x91\xaaq\xaf\xb5<\xb8\xd7\xda\x96w\xb8\x16Y\\\x1f\xda\x98\x8aN\xa7`@\x08\x00\x10\x05L&\xb0\xb2\x9f\xcb\x01e\x95\xc1S\xb0I|\xa5\x89\xd3M\x1fC\xae\xba\x0cA\xa4\xc7\xa9\x8f3\xa6\x9a?\xdf\x9ah\xfa\x1du\xd0b\r&=Ly\xa6\x8f\xbe\xd0\x01w\xfe\xbeX\xf9\xfb\xed\x00\x17{Q\x8b-Kp\xdd\xf4Z\xbe\xfb@\x05\xdbP\x92\x9b\xd9\xab\xfaRB\xcb@\xd2_\xa5#\xb3\xe9OhL\x9f@\x92\xb6\xb9\xac\x1c\x85X\xd5 \xa4\xb6\xc2\xada{ZT%\x1f\x81\x0f@\x8aAH\xb4\xa5I'ZB\xa1?\x86\x90\xe4\xb6\x92\xd4\x9f@\x8aAH\xb4\xa5I'Z\x93\xc8_\x86\xa8}\xcd0\xd2_@\x8aAH\xb4\xa5I'Y\x06I\x7f\x83\xa8\xf5\x17@\x8aAH\xb4\xa5I'Z\xd4\x16\xcf\x82\xff\x03@\x86\xae\xc3\x1e\xc3'\xd7\x85\xb6\x00}(o@\x82I\x7f\x86M\x835\x05\xb1\x1f\x00\x00\x04\x08\x00\x00\x00\x00\x03\x00\xbe\x00\x00"

binary_str = ':'.join(f'{byte:08b}' for byte in encoded_response)

decoded_msg = {}

sep_bytes = binary_str.split(":")

print(header_table[int(sep_bytes[0][4:], 2)])
to_int = int(sep_bytes[1], 2)
print(math.floor(int(sep_bytes[1], 2)/7))
# byte_value = to_int.to_bytes((to_int.bit_length() + 7) // 8, byteorder='big')
# print(byte_value)

collect = ""
for i in range(0, math.floor(int(sep_bytes[1], 2)/7)-2):
    collect += sep_bytes[i+2]
    print(sep_bytes[i+2])

print(collect)
print(decode_huffman(collect))

# for byte in binary_str.split(":"):
#     print(byte)

# decoded = decode_huffman(encoded_response)

# print(decoded)

