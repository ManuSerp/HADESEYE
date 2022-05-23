import socket
import struct
import sys


def send_data(data):
    multicast_group = ('224.3.29.71', 10000)


# Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
    sock.settimeout(0.2)

    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    message = data
    try:

        # Send data to the multicast group
        print(sys.stderr, 'sending "%s"' % message)
        sent = sock.sendto(bytes(message, 'utf-8'), multicast_group)

    # Look for responses from all recipients
        while True:
            print(sys.stderr, 'waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print(sys.stderr, 'timed out, no more responses')
                break
            else:
                print(sys.stderr, 'received "%s" from %s' % (data, server))

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()


if __name__ == '__main__':
    send_data("Hello World")
