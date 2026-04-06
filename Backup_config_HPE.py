from netmiko import ConnectHandler
import os
import time
import subprocess
import random
import getpass
from datetime import datetime

# =============================
# LOGIN
# =============================

username = input("Username : ")
password = getpass.getpass("Password : ")

# =============================
# PATH
# =============================

devices_file = r"C:\Users\zaki\Documents\PYTHON\backupconfigHPE\devicess.txt"
base_backup_folder = r"C:\Users\zaki\Documents\PYTHON\backupconfigHPE\backup"

today = datetime.now().strftime("%Y-%m-%d")
time_now = datetime.now().strftime("%H-%M")

backup_folder = os.path.join(base_backup_folder, today)
os.makedirs(backup_folder, exist_ok=True)

log_file = os.path.join(base_backup_folder, f"backup_log_{today}.txt")

# =============================
# FUNCTION
# =============================

def write_log(message):
    with open(log_file, "a") as log:
        log.write(message + "\n")

def ping_device(ip):
    result = subprocess.run(
        ["ping", "-n", "2", ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return "TTL=" in result.stdout

# =============================
# LOAD DEVICE
# =============================

with open(devices_file) as f:
    devices = [x.strip() for x in f if x.strip()]

total_devices = len(devices)

success = 0
failed = 0

start_time = time.time()

print("====================================")
print(f"Total device : {total_devices}")
print("Starting backup process...")
print("====================================")

# =============================
# LOOP DEVICE
# =============================

for index, ip in enumerate(devices, start=1):

    print(f"[{index}/{total_devices}] Checking {ip}")

    if not ping_device(ip):
        message = f"{ip} FAILED -> Device unreachable"
        print(message)
        write_log(message)
        failed += 1
        continue

    device = {
        "device_type": "hp_comware",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 30,
    }

    retry = 3
    connected = False

    for attempt in range(retry):

        try:

            print(f"Connecting {ip} (attempt {attempt+1})")

            connection = ConnectHandler(**device)
            connected = True
            break

        except Exception as e:
            time.sleep(5)

    if not connected:
        message = f"{ip} FAILED -> SSH connection failed"
        print(message)
        write_log(message)
        failed += 1
        continue

    try:

        connection.send_command_timing("screen-length disable")
        time.sleep(1)

        hostname = connection.find_prompt().replace("<", "").replace(">", "").strip()

        if hostname == "":
            hostname = ip

        # =============================
        # GET CONFIG
        # =============================

        config = connection.send_command_timing("display current-configuration")

        while True:
            more = connection.read_channel()
            if not more:
                break
            config += more
            time.sleep(0.5)

        config = config.strip()

        if len(config) < 1000:
            raise Exception("Config terlalu kecil / tidak terbaca")

        filename = os.path.join(
            backup_folder,
            f"{hostname}_{time_now}.rtf"
        )

        rtf_content = r"{\rtf1\ansi\deff0 " + config.replace("\n", r"\par ") + "}"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(rtf_content)

        connection.disconnect()

        message = f"{ip} SUCCESS -> {hostname}"
        print(message)
        write_log(message)

        success += 1

    except Exception as e:

        message = f"{ip} FAILED -> {e}"
        print(message)
        write_log(message)

        failed += 1

    # random delay supaya tidak dianggap scanning firewall
    time.sleep(random.uniform(1.5, 3.5))


# =============================
# SUMMARY
# =============================

end_time = time.time()

duration = round((end_time - start_time) / 60, 2)

print("\n====================================")
print("Backup selesai.")
print(f"Total device : {total_devices}")
print(f"Success      : {success}")
print(f"Failed       : {failed}")
print(f"Waktu proses : {duration} menit")
print("------------------------------------")
print("Hasil backup tersimpan di folder :")
print(backup_folder)
print("====================================")