import platform
import socket
import subprocess
import psutil
from datetime import datetime
import telebot

BOT_TOKEN = "YOUR_BOT_TOKEN"
AUTHORIZED_USER_ID = 123456789  # your Telegram user ID

bot = telebot.TeleBot(BOT_TOKEN)

def is_authorized(message):
    return message.chat.id == AUTHORIZED_USER_ID

def get_system_info():
    uname = platform.uname()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return (
        f"📋 System Info:\n"
        f"System   : {uname.system}\n"
        f"Node     : {uname.node}\n"
        f"Release  : {uname.release}\n"
        f"Version  : {uname.version}\n"
        f"Machine  : {uname.machine}\n"
        f"Processor: {uname.processor}\n"
        f"IP       : {ip}\n"
        f"Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

def get_disk_usage():
    usage = psutil.disk_usage('/')
    return (
        f"💾 Disk Usage:\n"
        f"Total: {usage.total // (2**30)} GB\n"
        f"Used : {usage.used // (2**30)} GB\n"
        f"Free : {usage.free // (2**30)} GB\n"
        f"Percent Used: {usage.percent}%"
    )

def get_memory_usage():
    mem = psutil.virtual_memory()
    return (
        f"🧠 Memory Usage:\n"
        f"Total: {mem.total // (2**20)} MB\n"
        f"Available: {mem.available // (2**20)} MB\n"
        f"Used: {mem.used // (2**20)} MB\n"
        f"Percent Used: {mem.percent}%"
    )

def get_uptime():
    boot = datetime.fromtimestamp(psutil.boot_time())
    return f"⏳ Uptime since: {boot.strftime('%Y-%m-%d %H:%M:%S')}"

def get_top_processes():
    procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
    lines = ["🔥 Top CPU Processes:"]
    for p in procs:
        lines.append(f"{p.info['pid']:>5} | {p.info['cpu_percent']:5.1f}% | {p.info['name']}")
    return "\n".join(lines)

def get_network_info():
    addrs = psutil.net_if_addrs()
    lines = ["🌐 Network Interfaces:"]
    for iface, addrs_list in addrs.items():
        lines.append(f"- {iface}:")
        for addr in addrs_list:
            if addr.family == socket.AF_INET:
                lines.append(f"    IPv4: {addr.address}")
            elif addr.family == socket.AF_PACKET:
                lines.append(f"    MAC: {addr.address}")
    return "\n".join(lines)

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    if not is_authorized(message): return
    bot.reply_to(message, """
✅ Commands:
/sysinfo   - System info
/disk      - Disk usage
/memory    - RAM usage
/uptime    - System uptime
/processes - Top CPU processes
/netinfo   - Network info
/exec <cmd> - Run shell command
/help      - This help message
""")

@bot.message_handler(commands=['sysinfo'])
def sysinfo(message):
    if not is_authorized(message): return
    bot.reply_to(message, get_system_info())

@bot.message_handler(commands=['disk'])
def disk(message):
    if not is_authorized(message): return
    bot.reply_to(message, get_disk_usage())

@bot.message_handler(commands=['memory'])
def memory(message):
    if not is_authorized(message): return
    bot.reply_to(message, get_memory_usage())

@bot.message_handler(commands=['uptime'])
def uptime(message):
    if not is_authorized(message): return
    bot.reply_to(message, get_uptime())

@bot.message_handler(commands=['processes'])
def processes(message):
    if not is_authorized(message): return
    bot.reply_to(message, get_top_processes())

@bot.message_handler(commands=['netinfo'])
def netinfo(message):
    if not is_authorized(message): return
    bot.reply_to(message, get_network_info())

@bot.message_handler(commands=['exec'])
def exec_command(message):
    if not is_authorized(message): return
    cmd = message.text[len("/exec "):].strip()
    if not cmd:
        bot.reply_to(message, "⚠️ Usage: /exec <shell_command>")
        return
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=15, universal_newlines=True)
        bot.reply_to(message, f"🖥️ Output:\n{output[:4000]}")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Command error:\n{e.output}")
    except Exception as e:
        bot.reply_to(message, f"Execution failed: {e}")

@bot.message_handler(func=lambda m: True)
def unknown(message):
    if is_authorized(message):
        bot.reply_to(message, "❓ Unknown command. Use /help.")

if __name__ == "__main__":
    print("🤖 Bot running...")
    bot.polling()
