from hpack import Decoder
import pyshark
import sslkeylog




pyshark.LiveCapture

decoder = Decoder()

# data = b"\x00\x01\x1b\x01\x25\x00\x00\x00\x03\x00\x00\x00\x00\x29\x82\x04\x81cA\x8a\xa0\xe4\x1d\x13\x9d\t\xb8\xf3M3\x87z\xbc\xd0\x7ff\xa2\x81\xb0\xda\xe0S\xfa\xe4j\xa4?\x84)\xa7z\x81\x02\xe0\xfbS\x91\xaaq\xaf\xb5<\xb8\xd7\xda\x96w\xb8\x16Y\\\x1f\xda\x98\x8aN\xa7`@\x08\x00\x10\x05L&\xb0\xb2\x9f\xcb\x01e\x95\xc1S\xb0I|\xa5\x89\xd3M\x1fC\xae\xba\x0cA\xa4\xc7\xa9\x8f3\xa6\x9a?\xdf\x9ah\xfa\x1du\xd0b\r&=Ly\xa6\x8f\xbe\xd0\x01w\xfe\xbeX\xf9\xfb\xed\x00\x17{Q\x8b-Kp\xdd\xf4Z\xbe\xfb@\x05\xdbP\x92\x9b\xd9\xab\xfaRB\xcb@\xd2_\xa5#\xb3\xe9OhL\x9f@\x92\xb6\xb9\xac\x1c\x85X\xd5 \xa4\xb6\xc2\xada{ZT%\x1f\x81\x0f@\x8aAH\xb4\xa5I'ZB\xa1?\x86\x90\xe4\xb6\x92\xd4\x9f@\x8aAH\xb4\xa5I'Z\x93\xc8_\x86\xa8}\xcd0\xd2_@\x8aAH\xb4\xa5I'Y\x06I\x7f\x83\xa8\xf5\x17@\x8aAH\xb4\xa5I'Z\xd4\x16\xcf\x82\xff\x03@\x86\xae\xc3\x1e\xc3'\xd7\x85\xb6\x00}(o@\x82I\x7f\x86M\x835\x05\xb1\x1f\x00\x00\x04\x08\x00\x00\x00\x00\x03\x00\xbe\x00\x00"

data = b"00011b012500000003000000002982048163418aa0e41d139d09b8f34d33877abcd07f66a281b0dae053fae46aa43f8429a77a8102e0fb5391aa71afb53cb8d7da9677b816595c1fda988a4ea76040080010054c26b0b29fcb016595c153b0497ca589d34d1f43aeba0c41a4c7a98f33a69a3fdf9a68fa1d75d0620d263d4c79a68fbed00177febe58f9fbed00177b518b2d4b70ddf45abefb4005db50929bd9abfa5242cb40d25fa523b3e94f684c9f4092b6b9ac1c8558d520a4b6c2ad617b5a54251f810f408a4148b4a549275a42a13f8690e4b692d49f408a4148b4a549275a93c85f86a87dcd30d25f408a4148b4a549275906497f83a8f517408a4148b4a549275ad416cf82ff034086aec31ec327d785b6007d286f4082497f864d833505b11f00000408000000000300be0000"

# Frame header length
frame_header_length = 9

# Priority length (5 bytes because PRIORITY flag is set)
priority_length = 5

# Start of HPACK block
hpack_start_index = frame_header_length + priority_length

print(decoder.decode(data))

