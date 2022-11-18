import sys
import paramiko
import time
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

log = logging.getLogger("cisco_script_api" + __name__)

def save_text_file(file_name, command, data):
    with open(f"{file_name}_{command}.txt", "w") as file:
        file.write(data)
        print(f"saved {command} to file {file_name}_{command}.txt")

def change_enable_password(host, username, password, secret, new_enanble_password):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(hostname=host, username=username, password=password)
    shell = conn.invoke_shell()
    print("ssh connection")
    time.sleep(1)
    shell.send(f"{secret}\n")
    shell.send("enable\n")
    shell.send("terminal len 0\n")
    time.sleep(1)
    shell.recv(9999).decode("utf-8")
    
    shell.send("sh startup-config\n")
    time.sleep(2)
    show_run = shell.recv(9999).decode("utf-8")
    file_name = host.replace(".", "_")
    save_text_file(file_name, "show_run_before", show_run)
    
    shell.send("conf t\n")
    shell.send("password " + new_enanble_password + "\n")
    shell.send("exit\n")
    shell.send("wr\n")
    time.sleep(2)

    shell.send("sh startup-config\n")
    time.sleep(2)
    show_modem = shell.recv(9999).decode("utf-8")
    save_text_file(file_name, "show_run_after", show_modem)
    conn.close()

def show_home(host, port, username, password):
    command = "ls /home"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()

    return lines

@app.route("/show_home", methods=["POST"])
def show_home_command():
    try:
        data = request.get_json()
        result = show_home(
            host=data["host"],
            port=int(data["port"]),
            username=data["username"],
            password=data["password"]
        )
        print(result)

        response = jsonify({
                    "message": "show home successfully",
                    "host": data["host"],
                    "result": result})
        response.status_code = 200

        return response
    
    except Exception as error:
        log.exception(error)

        response = jsonify({
                "message": "Something error",
                "error": str(error)
            })
        response.status_code = 500

        return response

@app.route("/change_enable_password", methods=["POST"])
def change_enable_password_comand():
    try:
        data = request.get_json()
        
        change_enable_password(host=data["host"],
                 username=data["username"],
                 password=data["password"],
                 secret=data["enable_password"],
                 new_enanble_password=data["new_enable_password"])

        response = jsonify({
                "message": "change enable password successfully",
                "host": data["host"]
            })
        response.status_code = 200

        return response
    
    except Exception as error:
        log.exception(error)

        response = jsonify({
                "message": "Something error",
                "error": str(error)})
        response.status_code = 500

        return response

if __name__ == "__main__":
    print("API strating ...")
    app.run(
        host="0.0.0.0",
        port="8000",
        threaded=True,
        debug=True
    )

