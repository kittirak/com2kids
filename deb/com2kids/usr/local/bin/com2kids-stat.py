# Get stat from host send to com2kids.in.th
# must edit server IP or domain

import platform
import datetime
import sys
import requests

# ฟังก์ชันสำหรับส่งข้อมูลไปยังเซิร์ฟเวอร์
def send_log(event_type):
    data = {
        "machine_name": platform.node(),  # ชื่อเครื่อง
	"school_id": 123456789,          # รหัสโรงเรียนตาม OBEC
        "event_type": event_type,        # startup หรือ shutdown
        "timestamp": datetime.datetime.now().isoformat()  # เวลาปัจจุบัน
    }
    try:
        # URL เซิร์ฟเวอร์ (แก้ไขตามของคุณ)
        response = requests.post("http://10.0.2.251:5000/api/logs", json=data)
        print(f"Log sent: {data}, Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending log: {e}")

# ฟังก์ชันบันทึก Log ลงไฟล์ในเครื่อง
def write_local_log(event_type):
    log_file = "/var/log/machine_usage.log"
    log_message = f"{datetime.datetime.now().isoformat()} - {event_type}\n"
    with open(log_file, "a") as f:
        f.write(log_message)

# ฟังก์ชันหลัก
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py [--startup | --shutdown]")
        sys.exit(1)

    # รับพารามิเตอร์จาก systemd
    event = sys.argv[1].lower()
    if event == "--startup":
        event_type = "Startup"
    elif event == "--shutdown":
        event_type = "Shutdown"
    else:
        print("Invalid argument. Use --startup or --shutdown")
        sys.exit(1)

    # บันทึกข้อมูล
    send_log(event_type)
    write_local_log(event_type)
