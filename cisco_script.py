import paramiko
import time

def save_text_file(file_name, command, data):
    with open(f"{file_name}_{command}.txt", "w") as file:
        file.write(data)
        print(f"saved {command} to file {file_name}_{command}.txt")

def call_ssh(host, username, password, secret):
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
    
    shell.send("show run\n")
    time.sleep(2)
    show_run = shell.recv(9999).decode("utf-8")
    file_name = host.replace(".", "_")
    save_text_file(file_name, "show_run", show_run)
    
    shell.send("show modem\n")
    time.sleep(2)
    show_modem = shell.recv(9999).decode("utf-8")
    save_text_file(file_name, "show_modem", show_modem)
    conn.close()

print(f"Connecting to Host {sys.argv[1]}...")
cisco = {
    "device_type": "cisco_ios",
    "host": sys.argv[1],
    "username": sys.argv[2],
    "password": sys.argv[3],
    "enable_password": sys.argv[4]
}

call_ssh(host=cisco["host"],
         username=cisco["username"],
         password=cisco["password"],
         secret=cisco["enable_password"])
