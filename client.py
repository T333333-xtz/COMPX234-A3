#client.py
import socket
import sys


def send_request(client_socket, request):
    size = len(request)
    formatted_request = f"{size:03d}{request}"
    client_socket.send(formatted_request.encode())
    response = client_socket.recv(1024).decode()
    return response


def run_client(hostname, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))
    try:
       with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                command = parts[0].upper()
                key = parts[1]
                value = parts[2] if len(parts) > 2 else None

                if len(key + (f" {value}" if value else "")) > 970:
                    print(f"Error: The combined size of key and value exceeds 970 characters. Ignoring: {line}")
                    continue

              parts = line.split()
                command = parts[0].upper()
                key = parts[1]
                value = parts[2] if len(parts) > 2 else None
          if len(key + (f" {value}" if value else "")) > 970:
                    print(f"Error: The combined size of key and value exceeds 970 characters. Ignoring: {line}")
                    continue

      if command == 'PUT':
                    request = f"P{key} {value}"
                elif command == 'READ':
                    request = f"R{key}"
                elif command == 'GET':
                    request = f"G{key}"
                else:
                    print(f"Error: Invalid command in file: {command}")
                    continue

   response = send_request(client_socket, request)
                print(f"{line}: {response[3:]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <file_path>")
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    run_client(hostname, port, file_path)
    
