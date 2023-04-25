import socket
from Library.Spout import Spout
import cv2

##########osc###########
from pythonosc import osc_server
from pythonosc import dispatcher
##########osc###########


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('localhost', 7000))

from interpolate import *

img1, z1 = generate_image_random(7) #50 for smoky
img2, z2 = generate_image_random(23) #7 for smoky

# img = generate_interpolation(z1, z2, alpha = 0.5)

spout = Spout(silent = False)
spout.createSender('output')


##########osc###########
dispatcher = dispatcher.Dispatcher()

# This maps a messageID to a function.
# That is when a message with a given ID is received, the given function is run:
dispatcher.map("/alpha", gen_frame)

server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)

print("Serving on {}".format(server.server_address))
server.serve_forever()

def gen_frame(addr, alpha):
    print(alpha)
    img = generate_interpolation(z1, z2, alpha = alpha)
    cv2.imshow("frame", img)
    if cv2.waitKey(1) and ord('q') == 0xFF:
        cv2.destroyAllWindows()
##########osc###########


while True:
    data, addr = udp_socket.recvfrom(1024)
    alpha = float(data.decode())
    print(alpha)
    img = generate_interpolation(z1, z2, alpha = alpha)
    cv2.imshow("frame", img)
    if cv2.waitKey(1) and ord('q') == 0xFF:
        cv2.destroyAllWindows()
        break
    
    # spout.check()
    # spout.send(img)