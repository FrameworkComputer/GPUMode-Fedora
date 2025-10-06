#!/usr/bin/env python3
import subprocess
import logging
import sys
from pathlib import Path

LOG_DIR = Path("/var/log/power-profile-manager")
LOG_FILE = LOG_DIR / "power-profile-manager.log"

class PowerProfileManager:
    def __init__(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Power Profile Manager started (TuneD)")
        
        if not self.check_tuned():
            logging.error("TuneD not found or not running")
            sys.exit(1)
        
        logging.info("Using TuneD for power profile management")
    
    def check_tuned(self):
        """Check if TuneD is active"""
        try:
            result = subprocess.run(['systemctl', 'is-active', 'tuned'],
                                  capture_output=True, text=True, timeout=2)
            return result.returncode == 0 and result.stdout.strip() == "active"
        except:
            return False
    
    def is_on_ac_power(self):
        """Check if system is on AC power"""
        try:
            power_supply_path = Path("/sys/class/power_supply")
            for adapter in power_supply_path.glob("AC*"):
                online_file = adapter / "online"
                if online_file.exists():
                    return online_file.read_text().strip() == "1"
            
            for adapter in power_supply_path.glob("A*"):
                if adapter.name.startswith("AC") or adapter.name.startswith("ADP"):
                    online_file = adapter / "online"
                    if online_file.exists():
                        return online_file.read_text().strip() == "1"
            
            return False
        except Exception as e:
            logging.error(f"Error checking AC power status: {e}")
            return False
    
    def set_tuned_profile(self, profile):
        """Set TuneD profile"""
        try:
            result = subprocess.run(['tuned-adm', 'profile', profile],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logging.info(f"Set TuneD profile to {profile}")
                return True
            else:
                logging.error(f"Failed to set TuneD profile: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Error setting TuneD profile: {e}")
            return False
    
    def set_profile_for_current_state(self):
        """Set appropriate TuneD profile based on current AC status"""
        on_ac = self.is_on_ac_power()
        power_state = "AC" if on_ac else "Battery"
        logging.info(f"Current power state: {power_state}")
        
        profile = "throughput-performance" if on_ac else "powersave"
        return self.set_tuned_profile(profile)

if __name__ == "__main__":
    manager = PowerProfileManager()
    manager.set_profile_for_current_state()
