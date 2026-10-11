import os
import sys
import ctypes
import subprocess
import time
from datetime import datetime

# Global variables
scanned_defender = None
scanned_firewall = None
scanned_ports = None
scanned_sandbox = None

def type_effect(text, delay=0.003):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(duration=1.2, message="Processing Auditing Subsystems..."):
    bars = ["/", "-", "\\", "|"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{' ' * 80}")
        sys.stdout.write(f"\r[*] {message} {bars[i % len(bars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{' ' * 80}")
    sys.stdout.write("\r[+] Query Complete!\n")
    sys.stdout.flush()

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
    ======================================================================
               AEGISHOST NEXUS - DYNAMIC LIVE AUDITOR v2.5           
         [ Stateful Recon Engine | Custom Live Report Builder ]       
    ======================================================================
    """
    type_effect(banner, 0.001)

def check_admin_privileges():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def warn_admin_soft(feature_name):
    print("\n" + "-" * 70)
    type_effect(f"[*] Note: '{feature_name}' can work without admin, but full details are better with Administrator rights.")
    print("-" * 70 + "\n")

def warn_admin_required(feature_name):
    print("\n" + "!" * 70)
    type_effect(f"[!] WARNING: '{feature_name}' requires Administrator privileges for accurate results.")
    type_effect("[!] Current session is running as NORMAL USER.")
    type_effect("[!] This scan will be restricted.")
    type_effect("[!] Recommended: Right-click the script → Run as administrator")
    print("!" * 70 + "\n")
    time.sleep(1.1)

# --- SUB-SYSTEM FUNCTIONS ---
def get_defender_status():
    try:
        cmd = "powershell -Command \"Get-MpComputerStatus | Select-Object -Property AMServiceEnabled, RealTimeProtectionEnabled, AntivirusEnabled\""
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return "Restricted / Incomplete (Administrator rights recommended)"
    except Exception as e:
        return f"Error: {str(e)}"

def get_firewall_status():
    try:
        cmd = "netsh advfirewall show allprofiles state"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            status_lines = [line.strip() for line in result.stdout.split("\n") if "State" in line or "Profile" in line]
            return "\n".join(status_lines) if status_lines else "Unable to retrieve firewall status"
        return "Restricted / Incomplete (Administrator rights recommended)"
    except Exception as e:
        return f"Error: {str(e)}"

def get_sandbox_vm_status():
    # ===== OPTION B: Strong privilege check =====
    if not check_admin_privileges():
        return "Restricted: VM / Sandbox Detection requires Administrator privileges."

    vm_indicators = ["vboxguest", "vmtoolsd", "vmmouse", "vboxservice"]
    detected_list = []
    try:
        cmd = "sc query type= driver"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        
        if result.returncode != 0:
            return "Restricted: Unable to query drivers."
            
        for indicator in vm_indicators:
            if indicator in result.stdout.lower():
                detected_list.append(indicator)
                
        if detected_list:
            return f"ALERT: Virtualization Drivers Found -> {', '.join(detected_list)} (Target is likely a VM/Sandbox)"
        return "Secure: Physical Hardware detected (No VM sandboxes found)."
    except:
        return "Unable to verify Virtualization drivers."

def get_network_ports():
    ports_data = []
    try:
        cmd = "netstat -ano"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "LISTENING" in line or "ESTABLISHED" in line:
                    ports_data.append(line.strip())
        return ports_data
    except:
        return []

# --- DYNAMIC REPORT GENERATOR ---
def generate_custom_report(privs, machine, user):
    global scanned_defender, scanned_firewall, scanned_ports, scanned_sandbox
    
    type_effect("\n[*] Building Custom Report from your Active Scans...")
    loading_animation(0.8, "Compiling layout...")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AegisNexus Custom Audit Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 40px; }}
            h1 {{ color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; }}
            .card {{ background-color: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }}
            .status-good {{ color: #4ade80; font-weight: bold; }}
            .status-alert {{ color: #f87171; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; background-color: #111827; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; font-family: monospace; }}
            th {{ background-color: #1e293b; color: #38bdf8; }}
            .banner {{ font-family: monospace; color: #38bdf8; white-space: pre; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="banner">
======================================================================
               AEGISHOST NEXUS - CUSTOM SECURITY REPORT             
======================================================================</div>
        <h1>Host Security Assessment Dashboard</h1>
        
        <div class="card">
            <h2> Target Environment & Context</h2>
            <p><strong>Privilege Level:</strong> <span class="status-good">{privs}</span></p>
            <p><strong>Machine Name:</strong> {machine}</p>
            <p><strong>Audited User:</strong> {user}</p>
        </div>
    """
    
    has_data = False

    if scanned_sandbox is not None:
        has_data = True
        html_content += f"""
        <div class="card">
            <h2> Anti-Analysis & Sandbox Audit</h2>
            <p class="{"status-alert" if "ALERT" in scanned_sandbox or "Restricted" in scanned_sandbox else "status-good"}">{scanned_sandbox}</p>
        </div>
        """
        
    if scanned_defender is not None:
        has_data = True
        html_content += f"""
        <div class="card">
            <h2> Endpoint Protection Status (Defender)</h2>
            <pre style="color: #4ade80; font-size: 14px; font-family: monospace;">{scanned_defender}</pre>
        </div>
        """
        
    if scanned_firewall is not None:
        has_data = True
        html_content += f"""
        <div class="card">
            <h2> Network Firewall Profiles</h2>
            <pre style="color: #38bdf8; font-size: 14px; font-family: monospace;">{scanned_firewall}</pre>
        </div>
        """
        
    if scanned_ports is not None:
        has_data = True
        ports_html = "".join([f"<tr><td>{p}</td></tr>" for p in scanned_ports[:25]]) or "<tr><td>No active ports found.</td></tr>"
        html_content += f"""
        <div class="card">
            <h2> Active Network Footprint (Open Ports)</h2>
            <table>
                <tr><th>Netstat Output (Listening & Established Connections)</th></tr>
                {ports_html}
            </table>
        </div>
        """
        
    if not has_data:
        html_content += """
        <div class="card" style="border: 1px dashed #f87171;">
            <h2 style="color: #f87171;">[!] No Scans Performed Yet</h2>
            <p>Please run at least one security check from the CLI menu before generating the report.</p>
        </div>
        """
        
    html_content += "</body></html>"
    
    # Improved file handling
    filename = "security_report.html"
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.html"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("\n" + "="*70)
    type_effect(f"[+] SUCCESS: Custom Live HTML report generated -> '{os.path.abspath(filename)}'")
    print("="*70)

# --- MAIN CONTROLLER ---
if __name__ == "__main__":
    print_banner()
    
    is_admin = check_admin_privileges()
    priv_string = "RUNNING AS ADMINISTRATOR (Full Integrity)" if is_admin else "NORMAL USER (Limited Privileges)"
    machine_name = os.environ.get('COMPUTERNAME', 'Unknown')
    user_name = os.environ.get('USERNAME', 'Unknown')
    
    type_effect(f"[+] Target Machine Connected: {machine_name}")
    type_effect(f"[+] Active Identity Context : {user_name}")
    
    if is_admin:
        type_effect("[+] Privilege Level        : ADMINISTRATOR (Full Access)")
    else:
        type_effect("[!] Privilege Level        : NORMAL USER (Limited Access)")
        type_effect("[!] Advanced scans (especially VM Detection) will be restricted.")
    
    print("=" * 70)
    
    while True:
        print("\n[?] SELECT AUDIT PROFILE MODE:")
        print("    [1] Quick System Hardening Check (Defender & Firewall)")
        print("    [2] Deep Network Recon (Open Ports)")
        print("    [3] Advanced Evading Audit (VM / Sandbox Detection)")
        print("    [4] GENERATE CUSTOM LIVE REPORT (Only based on your scans)")
        print("    [5] FULL AUTOMATED ASSESSMENT (All Scans + Report)")
        print("    [6] Exit Auditor")
        
        choice = input("\nAegisNexus> ").strip()
        
        if choice == "1":
            if not is_admin:
                warn_admin_soft("Defender & Firewall Check")
            type_effect("\n[*] Auditing Endpoint Security Guards...")
            loading_animation(0.6, "Querying Subsystems...")
            scanned_defender = get_defender_status()
            scanned_firewall = get_firewall_status()
            print(f"\n{scanned_defender}")
            print(f"\n{scanned_firewall}")
            print("-" * 70)

        elif choice == "2":
            type_effect("\n[*] Auditing Active Network Perimeter...")
            loading_animation(0.8, "Scanning Network Sockets...")
            scanned_ports = get_network_ports()
            print("    Proto  Local Address          Foreign Address        State          PID")
            for p in scanned_ports[:15]:
                print(f"    {p}")
            print("-" * 70)

        elif choice == "3":
            if not is_admin:
                warn_admin_required("VM / Sandbox Detection")
            type_effect("\n[*] Analyzing Virtualization Vector...")
            loading_animation(0.6, "Checking Hardware Artifacts...")
            scanned_sandbox = get_sandbox_vm_status()
            print(f"\n    {scanned_sandbox}")
            print("-" * 70)

        elif choice == "4":
            generate_custom_report(priv_string, machine_name, user_name)

        elif choice == "5":
            if not is_admin:
                warn_admin_soft("Full Assessment")
                print("[*] Note: VM Detection will be restricted without admin rights.\n")
            print_banner()
            type_effect("\n[!] Running Full Enterprise System Audit...")
            scanned_defender = get_defender_status()
            scanned_firewall = get_firewall_status()
            scanned_sandbox = get_sandbox_vm_status()
            scanned_ports = get_network_ports()
            print(f"\n[+] Defender Status:\n{scanned_defender}")
            print(f"\n[+] Firewall Profiles:\n{scanned_firewall}")
            print(f"\n[+] Anti-Analysis:\n{scanned_sandbox}")
            print("\n[+] Open Sockets:")
            for p in scanned_ports[:10]:
                print(f"    {p}")
            generate_custom_report(priv_string, machine_name, user_name)

        elif choice == "6" or choice.lower() == "exit":
            type_effect("[*] Terminating AegisNexus Session. Goodbye Agent.")
            break

        else:
            type_effect("[!] Invalid option. Please select 1-6.")
            print("-" * 70)