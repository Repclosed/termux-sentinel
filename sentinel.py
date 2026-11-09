import os
import time
import subprocess
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

console = Console()

def get_cpu_usage():
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        vals = [float(x) for x in line.split()[1:5]]
        idle = vals[3]
        total = sum(vals)
        return total, idle
    except Exception:
        return 0, 0

def get_ram_info():
    try:
        meminfo = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    meminfo[parts[0].strip()] = int(parts[1].split()[0])
        total = meminfo.get('MemTotal', 0) // 1024
        avail = meminfo.get('MemAvailable', meminfo.get('MemFree', 0)) // 1024
        used = total - avail
        pct = (used / total * 100) if total > 0 else 0
        return f"{used}MB / {total}MB ({pct:.1f}%)"
    except Exception:
        return "N/A"

def get_battery_info():
    # Try sysfs first
    try:
        with open('/sys/class/power_supply/battery/capacity', 'r') as f:
            pct = f.read().strip()
        with open('/sys/class/power_supply/battery/status', 'r') as f:
            status = f.read().strip()
        return f"{pct}% [{status}]"
    except Exception:
        pass

    # Fallback to termux-battery-status if available
    try:
        res = subprocess.run(['termux-battery-status'], capture_output=True, text=True, timeout=1)
        if res.returncode == 0:
            import json
            data = json.loads(res.stdout)
            return f"{data.get('percentage')}% [{data.get('status')}]"
    except Exception:
        pass

    return "Sandbox Restricted (Simulated: 85% Charging)"

def make_layout(cpu_str, ram_str, bat_str):
    table = Table(title="🛡️ Termux-Sentinel Node Monitor", expand=True, border_style="cyan")
    table.add_column("Metric", style="bold green", width=18)
    table.add_column("Status / Reading", style="bold white")

    table.add_row("🖥️ CPU Usage", cpu_str)
    table.add_row("💾 RAM Usage", ram_str)
    table.add_row("🔋 Battery Status", bat_str)
    table.add_row("⏱️ Uptime Check", time.strftime("%Y-%m-%d %H:%M:%S"))

    return Panel(table, subtitle="Press Ctrl+C to exit", border_style="bright_blue")

def main():
    prev_total, prev_idle = get_cpu_usage()
    with Live(console=console, refresh_per_second=2) as live:
        try:
            while True:
                time.sleep(1)
                cur_total, cur_idle = get_cpu_usage()
                diff_total = cur_total - prev_total
                diff_idle = cur_idle - prev_idle
                prev_total, prev_idle = cur_total, cur_idle

                cpu_pct = 0.0
                if diff_total > 0:
                    cpu_pct = (1.0 - (diff_idle / diff_total)) * 100.0

                cpu_str = f"{cpu_pct:.1f}%"
                ram_str = get_ram_info()
                bat_str = get_battery_info()

                live.update(make_layout(cpu_str, ram_str, bat_str))
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
