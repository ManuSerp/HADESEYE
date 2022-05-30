import socket
import struct
import sys
from trilat import model

print("configuring udp multicast receiver...")
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("done\nconfiguring trilateration model...")
m = model(["0", "1", "2"])
print("calibrating...")
m.calibrate(0, [0, 0])
m.calibrate(1, [0, 233])
m.calibrate(2, [198, 150])
print("done\nwaiting for data...")
l_data = [None for i in range(len(m.antenna))]


# Receive/respond loop
while True:
    # print(sys.stderr, '\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    # print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    # print(sys.stderr, data)
    data = data.decode('utf-8')
    data = data.split('#')
    l_data[int(data[1])] = float(data[0])
    if None not in l_data:
        print(l_data)

        print("TRILAT:")
        print(m.det_pos(l_data))

    # print(sys.stderr, 'sending acknowledgement to', address)
    sock.sendto(bytes('ack', 'utf-8'), address)
