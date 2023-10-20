import socket
import time

server_ip = "0.0.0.0"
server_port = 6000

tick = 10 / 1000  # tick rate for server response
loopDelay = 0.1  # prevent big CPU usage

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((server_ip, server_port))
sock.setblocking(False)

print(f"UDP server is listening on {server_ip}:{server_port}")

next_tick_time = time.time() + tick
while True:
    try:
        data, client_address = sock.recvfrom(1024)
        print(f"Received data from {client_address}: {data.decode()}")
        sock.sendto(b"received", client_address)
    except socket.error as e:
        if e.errno in [10035, 11]:
            pass
        else:
            raise

    current_time = time.time()
    if current_time >= next_tick_time:
        # print("tick pass")

        next_tick_time = current_time + tick

    time.sleep(loopDelay)
