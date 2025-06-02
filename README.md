# TeleFetch — Telegram System Info Bot

A lightweight Telegram bot to fetch and monitor your system information remotely.  
Get CPU, RAM, disk usage, uptime, network info, and even run shell commands — all via Telegram!

---

## ⚠️ Legal Notice

This project is intended for **educational and ethical use only**.  
Do **not** use it on machines you do not own or manage. Unauthorized access is illegal.  
The author is not responsible for any misuse or damage caused by this tool.

---

## ✨ Features

- 🖥️ Get detailed system info (OS, CPU, machine)
- 💾 Disk usage stats
- 🧠 Memory (RAM) usage
- ⏳ System uptime
- 🔥 Top CPU-consuming processes
- 🌐 Network interface info
- 💻 Execute shell commands remotely
- ✅ Access restricted to your Telegram user ID

---

## 🚀 Setup & Installation

### Requirements

- Python 3.7 or higher
- Telegram Bot Token ([get one from @BotFather](https://t.me/BotFather))
- Your Telegram User ID ([find it using @userinfobot](https://t.me/userinfobot))
## 🛠️ Run as a Background Service (Linux)
To run the bot persistently in the background and auto-start on boot, set it up as a `systemd` service.
### 1. Clone the Repository

```bash
git clone https://github.com/DebaA17/Basic_sys_info_gather.git
cd Basic_sys_info_gather
pip3 install -r requirements.txt
