<div align="center">

# 🛰️ AegisHost Nexus

### Dynamic Live Host Auditor for Windows

*Stateful recon engine + custom live report builder — scan only what you choose, then export a dark-themed HTML security dashboard.*

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=flat)
![Interface](https://img.shields.io/badge/Interface-CLI-00d4ff?style=flat)

</div>

---

## 📖 About

**AegisHost Nexus** is a command-line host security auditor that inspects the machine it runs on. It checks endpoint protection, firewall profiles, active network sockets, and virtualization artifacts, keeps the results in memory, and compiles **only the scans you actually ran** into a polished HTML report.

It detects whether it is running with Administrator rights and tells you plainly which checks will be limited without them, so results are never silently misleading.

> ⚠️ **Scope:** AegisHost Nexus is a read-only auditing tool intended for machines you own or are authorized to assess. It only reads system state — it does not modify settings or send data anywhere.

---

## ✨ Features

| Category | Details |
|---|---|
| 🛡️ **Endpoint Protection Check** | Reads Microsoft Defender status (service, real-time protection, antivirus) via PowerShell |
| 🔥 **Firewall Audit** | Shows state of all firewall profiles (Domain / Private / Public) via `netsh` |
| 🌐 **Network Recon** | Lists listening and established sockets with owning PIDs via `netstat` |
| 🧪 **VM / Sandbox Detection** | Flags virtualization drivers (VirtualBox, VMware) — requires Administrator |
| 🔑 **Privilege Awareness** | Detects admin vs. normal user and warns before restricted scans |
| 🧾 **Dynamic HTML Report** | Report contains only the scans you ran; includes machine, user, and privilege context |
| 🤖 **Full Automated Assessment** | One option runs every scan and generates the report |
| ⌨️ **Terminal UX** | Typewriter effect, loading animations, clean menu-driven flow |

---

## 🖼️ Preview

```
======================================================================
           AEGISHOST NEXUS - DYNAMIC LIVE AUDITOR v2.5
     [ Stateful Recon Engine | Custom Live Report Builder ]
======================================================================
[+] Target Machine Connected: DESKTOP-XXXX
[+] Privilege Level        : ADMINISTRATOR (Full Access)

[?] SELECT AUDIT PROFILE MODE:
    [1] Quick System Hardening Check (Defender & Firewall)
    [2] Deep Network Recon (Open Ports)
    [3] Advanced Evading Audit (VM / Sandbox Detection)
    [4] GENERATE CUSTOM LIVE REPORT
    [5] FULL AUTOMATED ASSESSMENT (All Scans + Report)
    [6] Exit Auditor

AegisNexus>
```

---

## 🧰 Requirements

- **OS:** Windows 10 / 11 (uses PowerShell, `netsh`, `netstat`, `sc`)
- **Python:** 3.8+
- **Packages:** none — standard library only
- **Recommended:** run from an elevated terminal (*Run as administrator*) for complete results

---

## 🚀 Installation & Usage

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/AegisHost_Nexus

# 2. Run it (preferably in an Administrator terminal)
python aegis.py
```

### Quick Start
1. Pick **[1]**, **[2]**, or **[3]** to run individual scans
2. Pick **[4]** to generate a report from the scans you've run so far
3. Or pick **[5]** to run everything and generate the report in one go
4. Open the generated `security_report.html` in any browser

---

## 📁 Project Structure

```
AegisHost_Nexus/
├── aegis.py        # Full application (scanners + report generator + CLI)
├── LICENSE
├── .gitignore
└── README.md
```

---

## 🏗️ Architecture

| Function | Responsibility |
|---|---|
| `check_admin_privileges()` | Detects whether the session has Administrator rights |
| `get_defender_status()` | Queries Defender state with `Get-MpComputerStatus` |
| `get_firewall_status()` | Reads firewall profile states with `netsh advfirewall` |
| `get_network_ports()` | Collects listening/established connections from `netstat -ano` |
| `get_sandbox_vm_status()` | Looks for known virtualization drivers (admin only) |
| `generate_custom_report()` | Builds the HTML dashboard from whichever scans were run |

---

## 🗺️ Roadmap

- [ ] Resolve PIDs to process names in the network table
- [ ] Add Windows Update / patch-level check
- [ ] JSON export alongside HTML
- [ ] Linux support for the network and firewall modules

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

Built for the cybersecurity community 🔐

</div>
