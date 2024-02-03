import subprocess
import platform
import re

def get_wifi_ssid():
    os_name = platform.system()

    try:
        if os_name == "Windows":
            # Windows command to get SSID
            command = "netsh wlan show interfaces"
            output = subprocess.check_output(command, shell=True).decode()
            ssid = re.search(r"SSID\s+:\s+(.*)\r", output).group(1)
            return ssid

        elif os_name == "Darwin":
            # MacOS command to get SSID
            command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
            output = subprocess.check_output(command, shell=True).decode()
            ssid = re.search(r" SSID: (.*)\n", output).group(1)
            return ssid

        elif os_name == "Linux":
            # Linux command to get SSID
            command = "nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d: -f2"
            output = subprocess.check_output(command, shell=True).decode()
            return output.strip()

        else:
            return "Unsupported Operating System"

    except Exception as e:
        return f"An error occurred: {e}"

def is_wifi_connected(SSID):
    if SSID.startswith('WetNode'):
        return True
    
    else:
        return False
    
print(is_wifi_connected(get_wifi_ssid()))
