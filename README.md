# GPUMode Fedora

System tray application for manual GPU mode switching on Fedora laptops with AMD integrated and NVIDIA discrete graphics.

---

## What It Does

- **Manual GPU Mode Switching**: Switch between Integrated and Hybrid modes via system tray
- **Power Change Notifications**: Optional informational notifications when AC power changes, suggesting manual GPU switching
- **Automatic Power Profiles**: Automatically switches TuneD power profiles (desktop/laptop-battery-powersave) based on AC/battery status
- **NVIDIA Mode Detection**: Detects when BIOS is set to NVIDIA-only mode and provides guidance

---

## Prerequisites

- AMD integrated GPU + NVIDIA discrete GPU
- NVIDIA proprietary drivers installed
- Fedora Linux (42+)
- [envycontrol installed](https://github.com/bayasdev/envycontrol)
- TuneD installed and enabled
- GNOME Shell Extension Manager
- AppIndicator and KStatusNotifierItem/Legacy Tray Icons extension

---

## Installation

### Step 1: Install System Tray Support

For the tray icon to appear in GNOME, you need the AppIndicator extension:

1. Install Extension Manager:
    - Software Center
    - Search gnome extension manager
    - Install it.

2. Open Extension Manager from your applications
    - Search for "AppIndicator and KStatusNotifierItem Support"
    - Install and enable the extension
    - Log out and log back in

### Step 2: Install GPUMode

1. Download latest .rpm [from releases](https://github.com/FrameworkComputer/GPUMode-Fedora/releases)
2. Install: sudo dnf install gpumode_*.rpm
3. Reboot

The tray icon will auto-start on login.

---

## Usage

### Switching GPU Modes

1. Click GPUMode tray icon
2. Select mode (Integrated/Hybrid)
3. Wait 1-3 minutes for Fedora to process GPU configuration changes
4. Reboot for changes to take effect, **wait for the notification before rebooting**

Note: Manual GPU switching on Fedora takes 1-3 minutes due to how Fedora processes GPU configuration changes. The app will show a "switching" icon during this time.

Note: If the system is in NVIDIA mode (set via BIOS), the app will detect this and disable switching. To regain switching functionality, reboot and set BIOS to Hybrid mode (F2 during boot).

### Power Change Notifications

Toggle "Power Change Notifications" in the tray menu to enable/disable informational notifications when AC power changes. These notifications suggest manual GPU mode switching but do not perform automatic switching.

### Checking Current Mode

Click tray icon to see current mode, or run:

    glxinfo | grep "OpenGL renderer"

or
    
    nvidia-smi

---

## Graphics Modes

### Hybrid Mode (Recommended)
- Both GPUs active
- AMD handles desktop/light tasks
- NVIDIA handles games/heavy applications
- Moderate battery impact
- Power consumption: ~14.4W at idle (3 min idle, laptop-battery-powersave profile, D0 power state)
- Switchable via this app

### Integrated Mode (AMD-only)
- NVIDIA completely off
- Best battery life
- Cannot run GPU-intensive applications
- Power consumption: ~6.7W at idle (3 min idle, laptop-battery-powersave profile)
- Switchable via this app

### NVIDIA Mode (Discrete-only)
- NVIDIA handles everything
- AMD disabled
- Maximum performance
- High battery drain
- Must be set in BIOS (F2) - not switchable in app

---

## Framework Laptop 16 AI 300 Series

GPU modes can be set in BIOS (F2 during boot):
- Hybrid mode (recommended): Enables app switching between Hybrid and Integrated
- NVIDIA mode: App will detect this and block switching until BIOS is set back to Hybrid
- Integrated mode: Can be set via BIOS or via this app

For best experience, set BIOS to Hybrid and use this app for switching.

---

## Troubleshooting

### Tray icon not visible
Install the AppIndicator and KStatusNotifierItem Support extension:
1. Install Extension Manager: sudo dnf install gnome-shell-extension-manager
2. Open Extension Manager
3. Search for and install "AppIndicator and KStatusNotifierItem Support"
4. Enable the extension
5. Log out and log back in

### envycontrol not found
Install envycontrol from https://github.com/bayasdev/envycontrol

### Mode didn't change after reboot
- Check BIOS graphics settings (may override in-OS)
- Verify with: nvidia-smi or glxinfo

### App shows "NVIDIA Mode Active" and blocks switching
Your BIOS is set to NVIDIA-only mode. To regain switching functionality:
1. Reboot and press F2 to enter BIOS
2. Navigate to graphics settings
3. Set mode to Hybrid
4. Save and exit
5. App will detect Hybrid mode and enable switching

### GPU switch takes a long time
This is normal on Fedora. Manual GPU switching takes 1-3 minutes due to how Fedora processes GPU configuration changes. Wait for the success notification before rebooting.

---

## How GPU Mode Detection Works

The app uses glxinfo to detect the active GPU:
- NVIDIA-only detected: App shows NVIDIA mode is active and blocks switching (BIOS setting required)
- AMD-only detected: Checks envycontrol to confirm Integrated mode
- Both GPUs detected: Confirms Hybrid mode

This ensures accurate mode detection regardless of whether the mode was set via BIOS or the app.

---

## Automatic Power Profile Management

The power-profile-manager service runs automatically and switches between:
- desktop TuneD profile when on AC power
- laptop-battery-powersave TuneD profile when on battery

This happens independently of GPU mode switching and works with TuneD.

---

## Uninstallation

    sudo dnf remove gpumode

---

## Reporting Bugs

Include:
- Fedora version (42+)
- GPU models
- Driver versions (nvidia-smi output)
- BIOS graphics setting (Framework Laptop 16 users)
- Steps to reproduce
- Log file: ~/.local/share/gpumode/gpumode.log

---

## License

GPL-3.0
