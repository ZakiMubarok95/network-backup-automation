# 🔧 Network Configuration Backup Automation

Automation script for backing up network device configurations (HPE Comware) using Python and SSH.

---

## 📌 Overview

This project is designed to automate the process of backing up configuration files from multiple network devices.  
It ensures reliability, reduces manual work, and improves recovery readiness in case of device failure.

---

## 🚀 Features

- 🔌 Multi-device backup (from list of IP addresses)
- 🌐 Connectivity check using ping before SSH connection
- 🔁 Retry mechanism for failed connections
- 📥 Automated configuration retrieval
- 💾 Structured backup storage (by date & time)
- 📝 Logging system (success / failed devices)
- ⏱️ Random delay to avoid firewall detection

---

## 🛠️ Technologies Used

- Python 3
- Netmiko (SSH automation)
- Standard libraries:
  - os
  - time
  - subprocess
  - datetime
  - getpass

---

## 📂 Project Structure
backupconfig/
│
├── devicess.txt # List of device IPs
├── backup/ # Backup results (auto-created)
├── backup_log_YYYY-MM-DD.txt
└── backup_script.py # Main script


---

## ⚙️ How It Works

1. User inputs username & password securely
2. Script reads device IP list from file
3. Each device is checked via ping
4. SSH connection is established using Netmiko
5. Device configuration is retrieved
6. Backup is saved in RTF format (timestamped)
7. Result is logged (success / failure)

---

## ▶️ Usage

1. Install dependencies:

```bash
pip install netmiko



