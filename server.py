import subprocess
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse 
from pydantic import BaseModel
import os
import socket

app = FastAPI()

# Path สำหรับ Public Key
PUBLIC_KEY_PATH = "/etc/veyon/keys/public/com2kids/key"
VEYON_DEB_FILE_PATH = "/home/com2kids/Downloads/veyon_4.8.3.0-ubuntu.focal_amd64.deb"


# 0. download veyon
@app.get("/download/veyon")
def download_veyon():
    # Check if the file exists
    if not os.path.exists(VEYON_DEB_FILE_PATH):
        return {"error": "File not found"}

    # Serve the file for download
    headers = {
        "Content-Disposition": "attachment; filename=veyon_4.8.3.0-ubuntu.focal_amd64.deb"
    }
    return FileResponse(
        VEYON_DEB_FILE_PATH,
        media_type="application/vnd.debian.binary-package",
        headers=headers
        #filename=os.path.basename(VEYON_DEB_FILE_PATH)
    )

# 1. Endpoint: ดาวน์โหลด Public Key
@app.get("/keys/public")
def get_public_key():
    if not os.path.exists(PUBLIC_KEY_PATH):
        raise HTTPException(status_code=404, detail="Public key not found")
    
    with open(PUBLIC_KEY_PATH, "r") as key_file:
        return {"public_key": key_file.read()}

# enpoint 
def get_latest_computer_number():
    try:
        # Run the veyon-cli command to get the list of computers
        result = subprocess.run(['veyon-cli', 'networkobjects', 'list'], capture_output=True, text=True, check=True)
        print(result)
        # Parse the output using regex to find all the student names
        student_names = re.findall(r'Computer "student(\d+)"', result.stdout)
        
        # Convert the found student names to integers
        student_numbers = [int(name) for name in student_names]
        
        # If there are no students, return 1 as the next number
        if not student_numbers:
            return 1

        # Return the highest number + 1 for the next student
        return max(student_numbers) + 1

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute veyon-cli command: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Pydantic model for client configuration
class ClientConfig(BaseModel):
    ip: str

# 2. Endpoint: รับข้อมูลจาก Client
@app.post("/client/config")
def submit_client_config(config: ClientConfig):

    # Get the latest computer number and increment by 1
    next_computer_number = get_latest_computer_number()

    # Create the new hostname (e.g., student1 -> student2 -> student3 -> ...)
    new_hostname = f"student{next_computer_number}"

    # Here you can use `new_hostname` and `config.ip` to configure the client or do any other action needed

    try:
        # 2.1 เพิ่ม IP ให้ veyon master
        # sudo veyon-cli networkobjects add computer student3 10.0.2.253 "" "Computer Room"
        command = [
            "sudo", "veyon-cli", "networkobjects", "add", "computer", new_hostname, config.ip, "", "Computer Room"
        ]
        # Run the command
        result = subprocess.run(
            command,
            text=True,  # Ensure string-based I/O instead of bytes
            capture_output=True  # Capture stdout and stderr
        )

        # Check the result
        if result.returncode == 0:
            print(f"Successfully added {new_hostname} with IP {config.ip} to Veyon:")
            print(result.stdout)
        else:
            print(f"Error adding {new_hostname}:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute command: {e}")

    # Example: Print the new hostname (or handle further logic)
    fqdn=socket.gethostname()
    domain=fqdn[fqdn.find("."):len(fqdn)]
    return {"new_hostname": new_hostname+domain}

@app.on_event("startup")
def startup_event():
    print(f"Waiting for client connect")

