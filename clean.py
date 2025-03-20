import os
import platform
import sys

def remove_persistence():
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SpaceInvaders")
            winreg.CloseKey(key)
            print("Persistence removed from Windows Registry.")
        except Exception as e:
            print(f"Failed to remove persistence on Windows: {e}")
    elif platform.system() == "Linux":
        autostart_file = os.path.expanduser("~/.config/autostart/space_invaders_demo.desktop")
        if os.path.exists(autostart_file):
            os.remove(autostart_file)
            print("Autostart entry removed.")
        else:
            print("No autostart entry found.")
    elif platform.system() == "Darwin":  # macOS
        launch_agent_file = os.path.expanduser("~/Library/LaunchAgents/com.spaceinvaders.demo.plist")
        if os.path.exists(launch_agent_file):
            os.remove(launch_agent_file)
            print("LaunchAgent removed.")
        else:
            print("No LaunchAgent found.")

if __name__ == "__main__":
    print("Cleaning up persistence features...")
    remove_persistence()
    print("Cleanup complete.")
