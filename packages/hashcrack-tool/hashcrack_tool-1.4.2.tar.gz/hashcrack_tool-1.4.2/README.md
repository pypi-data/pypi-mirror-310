<p align="center">
  <img src="https://github.com/user-attachments/assets/283f9b80-bd00-4303-a35b-ed1823d6ea4d"/>
</p>

A Python-based wrapper for [Hashcat](https://hashcat.net/hashcat/), offering a simplified interface for password cracking tasks. hashCrack enables you to use different attack methods—wordlists, rules, brute-force, and hybrid attacks—through a guided menu interface. ![GitHub License](https://img.shields.io/github/license/ente0v1/hashCrack)

> [!CAUTION]
> This tool is provided "as-is," without any express or implied warranties. The author assumes no responsibility for any damages, losses, or consequences arising from the use of this tool. It is specifically designed for penetration testing purposes, and should only be used in legal and authorized environments, such as with explicit permission from the system owner. Unauthorized use or misuse of this tool, in violation of applicable laws, is strictly prohibited. Users are strongly advised to comply with all relevant local, national, and international laws and obtain proper authorization before performing any security assessments.

---

## Features
- Multiple attack modes: wordlists, rules, brute-force, and hybrid attacks.
- An interactive menu for selecting and configuring cracking options.
- Session restoration support for interrupted sessions.
- Designed for compatibility across Linux and Windows environments.

## Installation & Setup

### Requirements

#### Linux:
- **OS**: Any Linux distribution
- **Programs**:
  - **Hashcat**: Install from [hashcat.net](https://hashcat.net/hashcat/)
  - **Optional**: For WPA2 cracking, additional tools like [aircrack-ng](https://www.aircrack-ng.org/), [hcxtools](https://github.com/zkryss/hcxtools), and [hcxdumptool](https://github.com/fg8/hcxdumptool) are recommended.
  
**Distribution-specific Commands**:
- **Debian/Ubuntu**:
  ```bash
  sudo apt update && sudo apt install hashcat python3 python3-pip
  ```
- **Fedora**:
  ```bash
  sudo dnf install hashcat python3 python3-pip
  ```
- **Arch Linux/Manjaro**:
  ```bash
  sudo pacman -S hashcat python python-pip
  ```

#### Windows:
- **OS**: Windows 10 or later
- **Programs**:
  - **Hashcat**: Download the Windows version from [hashcat.net](https://hashcat.net/hashcat/)
  - **Python**: Install from [python.org](https://www.python.org/downloads/)
  - **Optional**: For a Linux-like environment, set up [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)

> [!TIP]
> Recommended wordlists, rules, and masks can be found in repositories like [SecLists](https://github.com/danielmiessler/SecLists) and [wpa2-wordlists](https://github.com/kennyn510/wpa2-wordlists.git). It’s advised to keep these resources in `hashCrack` under `wordlists`, `rules`, and `masks` folders for better compatibility.
   
### Installation via pip
1. **Install hashCrack with pip**:
   You can install `hashCrack` directly from the Python Package Index (PyPI) using the following command:
   ```bash
   pip install hashcrack-tool
   ```
2. **Running hashCrack**:
   After installation, you can run `hashCrack` by specifying the hash file you want to crack:
   ```bash
   hashcrack hash
   ```

   
<p align="center">
  <video src="https://github.com/user-attachments/assets/7c09f4c1-007d-464b-a241-753d6e6cb25c" />
</p>
    
>[!TIP]
> **(Optional) Download default wordlists and rules**:
   ```bash
   git clone https://github.com/ente0v1/hashcat-defaults
   git lfs install
   git pull
   cd ..
   cp -rf hashcat-defaults/* .
   sudo rm -r hashcat-defaults
   ```
> [!IMPORTANT]
> The cracking results will be stored in `~/.hashCrack/logs`, specifically in `status.txt`.

> [!WARNING]
> Before starting a new cracking session (denoted as session "x"), ensure that the status file in the .hashCrack/logs/x folder does not exist or is empty. This is important to prevent conflicts if you run a second session of cracking using the same session name. For example, if a plaintext password "a" is generated in the first session, and a second session with the same name is started, the final output might contain passwords from both sessions, which can cause confusion. 
## Latest Releases
For the latest release versions of hashCrack, visit the [hashCrack Releases](https://github.com/ente0v1/hashCrack/releases) page.

## Attack Modes
hashCrack supports the following attack modes:
| # | Mode                 | Description                                                                                   |
|---|-----------------------|-----------------------------------------------------------------------------------------------|
| 0 | Straight             | Uses a wordlist directly to attempt cracks                                                    |
| 1 | Combination          | Combines two dictionaries to produce candidate passwords                                      |
| 3 | Brute-force          | Attempts every possible password combination based on a specified character set               |
| 6 | Hybrid Wordlist + Mask | Uses a wordlist combined with a mask to generate variations                                 |
| 7 | Hybrid Mask + Wordlist | Uses a mask combined with a wordlist for generating password candidates                     |
| 9 | Association          | For specific hash types where known data is combined with brute-force attempts                |

## Menu Options
The main menu provides easy access to various cracking methods:

| Option     | Description                | Script                          |
|------------|----------------------------|---------------------------------|
| 1 (Mode 0) | Crack with Wordlist        | Executes wordlist-based cracking |
| 2 (Mode 9) | Crack with Rules           | Executes rule-based cracking |
| 3 (Mode 3) | Crack with Brute-Force     | Executes brute-force cracking |
| 4 (Mode 6) | Crack with Combinator      | Executes hybrid wordlist + mask cracking |
| 0          | Clear Hashcat Potfile      | Deletes the potfile to clear previous hash results |
| X          | Switch Current OS Menu     | Updates the menu and script settings based on the current OS |
| Q          | Quit                       | Exits the program |

### Example Commands
```bash
hashcat -a 0 -m 400 example400.hash example.dict              # Wordlist
hashcat -a 0 -m 0 example0.hash example.dict -r best64.rule   # Wordlist + Rules
hashcat -a 3 -m 0 example0.hash ?a?a?a?a?a?a                  # Brute-Force
hashcat -a 1 -m 0 example0.hash example.dict example.dict     # Combination
hashcat -a 9 -m 500 example500.hash 1word.dict -r best64.rule # Association
```
---
## Troubleshooting Hashcat Issues

If you encounter errors when running Hashcat, you can follow these steps to troubleshoot:

1. **Test Hashcat Functionality**:
   First, run a benchmark test to ensure that Hashcat is working properly:
   ```bash
   hashcat -b
   ```
   This command will perform a benchmark on your system to check Hashcat's overall functionality. If this command works without issues, Hashcat is likely properly installed.

2. **Check Available Devices**:
   To verify that Hashcat can detect your devices (such as GPUs) for cracking, use the following command:
   ```bash
   hashcat -I
   ```
   This command will list the available devices. Ensure that the correct devices are listed for use in cracking.

3. **Check for Errors in Hashcat**:
   If the cracking process fails or Hashcat doesn't seem to recognize your devices, running the above tests should help identify potential problems with your system configuration, such as missing or incompatible drivers.

4. **Permissions**:
   If you encounter permission issues (especially on Linux), consider running Hashcat with elevated privileges or configuring your user group correctly for GPU access. You can run Hashcat with `sudo` if necessary:
   ```bash
   sudo hashcat -b
   ```

---

## Script Walkthrough

The main hashCrack script consists of:
1. **Initialization**: Loads default parameters and reusable functions.
2. **User Prompts**: Gathers inputs from the user such as wordlist location, session names, and attack type.
3. **Command Construction**: Constructs the Hashcat command based on user inputs and specified attack mode.
4. **Execution**: Runs the cracking session with or without status timers.
5. **Logging**: Saves session settings and logs the results for future reference.

---

## Help
For more resources, consider the following repositories:
- [hashcat-defaults](https://github.com/ente0v1/hashcat-defaults)
- [wpa2-wordlists](https://github.com/kennyn510/wpa2-wordlists.git)
- [paroleitaliane](https://github.com/napolux/paroleitaliane)
- [SecLists](https://github.com/danielmiessler/SecLists)
- [hashcat-rules](https://github.com/Unic0rn28/hashcat-rules)

To capture WPA2 hashes, follow [this guide on the 4-way handshake](https://notes.networklessons.com/security-wpa-4-way-handshake) and see this [video](https://www.youtube.com/watch?v=WfYxrLaqlN8) to see how the attack actually works.
For more details on Hashcat’s attack modes and usage, consult the [Hashcat Wiki](https://hashcat.net/wiki/), [Radiotap Introduction](https://www.radiotap.org/), or [Aircrack-ng Guide](https://wiki.aircrack-ng.org/doku.php?id=airodump-ng).
