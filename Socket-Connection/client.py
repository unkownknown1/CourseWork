"""Connect to the matching localhost server and exchange text messages."""

import socket


HOST = "127.0.0.1"
PORT = 50007
MAX_MESSAGE_BYTES = 4096


def main() -> None:
    try:
        # A timeout prevents the connection attempt from waiting indefinitely.
        with socket.create_connection((HOST, PORT), timeout=5) as connection:
            print(f"Connected to server at {HOST}:{PORT}")
            with connection.makefile("r", encoding="utf-8", newline="\n") as incoming:
                while True:
                    try:
                        message = input("Enter a message (or 'quit' to disconnect): ")
                    except (EOFError, KeyboardInterrupt):
                        message = "quit"
                        print("\nDisconnecting...")

                    # Keep the newline-delimited protocol to one line per message.
                    if "\n" in message or "\r" in message:
                        print("Please enter a single-line message.")
                        continue
                    if len(message.encode("utf-8")) > MAX_MESSAGE_BYTES:
                        print("Message is too long; use at most 4096 UTF-8 bytes.")
                        continue
                    connection.sendall((message + "\n").encode("utf-8"))
                    response = incoming.readline()
                    if not response:
                        print("Server disconnected without a response.")
                        break
                    print(response.rstrip("\n"))
                    if message == "quit":
                        print("Disconnected cleanly.")
                        break
    except ConnectionRefusedError:
        print("Connection failed: server is not running. Start server.py first.")
    except (socket.timeout, OSError, UnicodeError) as error:
        print(f"Connection error: {error}")


if __name__ == "__main__":
    main()
