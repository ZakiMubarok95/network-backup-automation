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
