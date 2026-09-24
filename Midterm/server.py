"""A small, single-client TCP echo server for a localhost demonstration."""

import socket


HOST = "127.0.0.1"
PORT = 50007
MAX_MESSAGE_BYTES = 4096


def main() -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            # Allow a quick restart after the previous demonstration ends.
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            print(f"Server listening on {HOST}:{PORT}", flush=True)

            # A context manager closes the connection even if an error occurs.
            with server.accept()[0] as connection:
                print("Client connected.", flush=True)
                with connection.makefile("r", encoding="utf-8", newline="\n") as incoming:
                    for line in incoming:
                        message = line.rstrip("\n")
                        if message == "quit":
                            connection.sendall(b"Goodbye!\n")
                            print("Client requested disconnection.", flush=True)
                            break
                        print(f"Client: {message}", flush=True)
                        # Each newline marks the end of one response.
                        reply = f"Server received: {message}\n".encode("utf-8")
                        connection.sendall(reply)
                    else:
                        print("Client disconnected.", flush=True)
    except (OSError, UnicodeError) as error:
        print(f"Server error: {error}", flush=True)
    finally:
        print("Server shut down.", flush=True)


if __name__ == "__main__":
    main()
