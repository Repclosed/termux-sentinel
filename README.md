# 🛡️ Termux-Sentinel

A fast, lightweight terminal resource HUD and system monitor designed for Android devices running Termux micro-servers.

![Termux](https://img.shields.io/badge/Platform-Termux%2FAndroid-black?logo=android)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## Features
- **Zero-lag TUI**: Powered by the Python `rich` rendering engine.
- **Android & PRoot Friendly**: Reads directly from `/proc/` and gracefully handles sandboxed `/sys/class/power_supply` permissions.
- **Battery Tracking**: Compatible with native sysfs and Termux-API hooks.

## Installation & Usage

```bash
git clone [https://github.com/repclosed/termux-sentinel.git](https://github.com/repclosed/termux-sentinel.git)
cd termux-sentinel
pip install -r requirements.txt
python3 sentinel.py

