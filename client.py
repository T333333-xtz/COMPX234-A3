#client.py
import socket
import sys


def send_request(client_socket, request):
    size = len(request)
    formatted_request = f"{size:03d}{request}"
    client_socket.send(formatted_request.encode())
    response = client_socket.recv(1024).decode()
    return response
