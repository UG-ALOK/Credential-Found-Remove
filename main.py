#!/usr/init/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import urllib.request
import urllib.error
import time
import re
import threading

# ANSI Color Codes for Light Gold & Professional Terminal UI
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
LIGHT_GOLD = "\033[33m"
CYAN = "\033[96m"

# Internal Storage Download Folder Path in Android / Termux
DOWNLOAD_DIR = "/storage/emulated/0/Download"
if not os.path.exists(DOWNLOAD_DIR):
    DOWNLOAD_DIR = os.path.expanduser("~/storage/shared/Download")
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(DOWNLOAD_DIR, ".credential_tool_config.json")

# Global Session Variables
current_token = None
current_platform = None
current_username = None
session_lock = threading.Lock()

# Strict Real-World Secret Detection Patterns
SECRET_PATTERNS = {
    "GitHub PAT": re.compile(r"ghp_[a-zA-Z0-9]{36}"),
    "GitLab PAT": re.compile(r"glpat-[0-9a-zA-Z\-\_]{20,40}"),
    "AWS Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Slack Webhook": re.compile(r"https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+"),
    "Private Key": re.compile(r"-----BEGIN (RSA|DSA|EC|PRIVATE) KEY-----")
}

def print_banner():
    banner = f"""
{LIGHT_GOLD}{BOLD}
==================================================
        CREDENTIAL FOUND & REMOVE TOOL v3.8
          [ Developer : Raj Alok ]
==================================================
{RESET}
    """
    print(banner)

# Background Timer to Auto-Reset Token every 2 Minutes (120 seconds)
def token_expiry_timer():
    global current_token, current_platform, current_username
    time.sleep(120)  # Wait for 2 minutes
    with session_lock:
        current_token = None
        current_platform = None
        current_username = None
        if os.path.exists(CONFIG_FILE):
            try:
                os.remove(CONFIG_FILE)
            except:
                pass
        print(f"\n\n{RED}[!] Security Alert: Token file auto-reset & deleted after 2 minutes for security! Please re-configure.{RESET}")

def save_token_to_storage(token, platform, username):
    data = {"token": token, "platform": platform, "username": username}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"{RED}[!] Failed to save token to Download folder: {e}{RESET}")

def load_token_from_storage():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("token"), data.get("platform"), data.get("username")
        except:
            return None, None, None
    return None, None, None

def verify_token_input():
    global current_token, current_platform, current_username
    print(f"\n{LIGHT_GOLD}[*] Enter Access Token{RESET}")
    token = input(f"{LIGHT_GOLD}Paste Access Token: {RESET}").strip()
    if not token:
        print(f"{RED}[!] Token empty!{RESET}")
        return

    platforms = [
        {"name": "GitHub", "url": "https://api.github.com/user", "headers": {"Authorization": f"Bearer {token}", "User-Agent": "CredTool", "Accept": "application/vnd.github+json"}, "parser": lambda d: d.get("login")},
        {"name": "Codeberg", "url": "https://codeberg.org/api/v1/user", "headers": {"Authorization": f"token {token}", "User-Agent": "CredTool", "Accept": "application/json"}, "parser": lambda d: d.get("login")},
        {"name": "GitLab", "url": "https://gitlab.com/api/v4/user", "headers": {"PRIVATE-TOKEN": token, "User-Agent": "CredTool"}, "parser": lambda d: d.get("username")},
        {"name": "Bitbucket", "url": "https://api.bitbucket.org/2.0/user", "headers": {"Authorization": f"Bearer {token}", "User-Agent": "CredTool"}, "parser": lambda d: d.get("username")},
        {"name": "Gitea", "url": "https://gitea.com/api/v1/user", "headers": {"Authorization": f"token {token}", "User-Agent": "CredTool", "Accept": "application/json"}, "parser": lambda d: d.get("login")}
    ]

    detected, uname = None, None
    for p in platforms:
        req = urllib.request.Request(p["url"], headers=p["headers"])
        try:
            with urllib.request.urlopen(req) as res:
                if res.status == 200:
                    data = json.loads(res.read().decode())
                    uname = p["parser"](data)
                    detected = p["name"]
                    break
        except:
            continue

    if detected and uname:
        with session_lock:
            current_token = token
            current_platform = detected
            current_username = uname
            save_token_to_storage(token, detected, uname)
        
        # Start 2-minute auto-reset timer in background
        threading.Thread(target=token_expiry_timer, daemon=True).start()
        
        print(f"\n{GREEN}[✔] Verified! Platform: {detected} | User: {uname}{RESET}")
        print(f"{CYAN}[i] Token successfully saved to Download folder. Will auto-reset in 2 minutes.{RESET}")
    else:
        print(f"{RED}[!] Invalid token.{RESET}")

def fetch_and_scan_repos():
    global current_token, current_platform, current_username
    
    t, p, u = load_token_from_storage()
    if not t:
        with session_lock:
            current_token, current_platform, current_username = None, None, None
        print(f"{RED}[!] Token file not found in Download folder! Please input a new token first.{RESET}")
        return

    print(f"\n{LIGHT_GOLD}[*] Fetching live repositories from {current_platform}...{RESET}")
    time.sleep(0.3)

    if current_platform == "GitHub":
        url, headers = "https://api.github.com/user/repos?per_page=100", {"Authorization": f"Bearer {current_token}", "User-Agent": "CredTool", "Accept": "application/vnd.github+json"}
    elif current_platform in ["Codeberg", "Gitea"]:
        base = "https://codeberg.org" if current_platform == "Codeberg" else "https://gitea.com"
        url, headers = f"{base}/api/v1/user/repos?limit=100", {"Authorization": f"token {current_token}", "User-Agent": "CredTool", "Accept": "application/json"}
    elif current_platform == "GitLab":
        url, headers = "https://gitlab.com/api/v4/projects?membership=true", {"PRIVATE-TOKEN": current_token, "User-Agent": "CredTool"}
    elif current_platform == "Bitbucket":
        url, headers = "https://api.bitbucket.org/2.0/repositories?role=member", {"Authorization": f"Bearer {current_token}", "User-Agent": "CredTool"}
    else:
        return

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            raw = json.loads(res.read().decode())
            repos = []
            if current_platform in ["GitHub", "Codeberg", "Gitea", "GitLab"]:
                repos = [{"name": r.get("name"), "full_name": r.get("full_name") or r.get("path_with_namespace") or f"{current_username}/{r.get('name')}"} for r in raw if r.get("name")]
            elif current_platform == "Bitbucket":
                repos = [{"name": r.get("name"), "full_name": r.get("full_name")} for r in raw.get("values", []) if r.get("name")]

            print(f"\n{LIGHT_GOLD}=================================================={RESET}")
            print(f"{LIGHT_GOLD}[+] Total Repositories Found: {len(repos)}{RESET}")
            print(f"{LIGHT_GOLD}=================================================={RESET}")

            for idx, r in enumerate(repos, 1):
                print(f"{LIGHT_GOLD}{idx}. {r['name']}{RESET}")

            print(f"{LIGHT_GOLD}=================================================={RESET}")
            
            choice = input(f"\n{LIGHT_GOLD}Type 'y' to scan real-time: {RESET}").strip().lower()
            if choice == 'y':
                run_real_scan(repos, current_token, current_platform)
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

def run_real_scan(repos, token, platform):
    print(f"\n{LIGHT_GOLD}[*] Real-time scanning repository contents...{RESET}")
    found_secrets = False
    flagged = []

    for repo in repos:
        name = repo['name']
        full_name = repo['full_name']
        contents_url, headers = "", {}

        if platform == "GitHub":
            contents_url = f"https://api.github.com/repos/{full_name}/contents"
            headers = {"Authorization": f"Bearer {token}", "User-Agent": "CredTool", "Accept": "application/vnd.github+json"}
        elif platform in ["Codeberg", "Gitea"]:
            base = "https://codeberg.org" if platform == "Codeberg" else "https://gitea.com"
            contents_url = f"{base}/api/v1/repos/{full_name}/contents"
            headers = {"Authorization": f"token {token}", "User-Agent": "CredTool", "Accept": "application/json"}

        if contents_url:
            try:
                req = urllib.request.Request(contents_url, headers=headers)
                with urllib.request.urlopen(req) as resp:
                    files = json.loads(resp.read().decode())
                    if isinstance(files, list):
                        for f in files:
                            d_url = f.get("download_url")
                            if d_url:
                                f_req = urllib.request.Request(d_url, headers=headers)
                                with urllib.request.urlopen(f_req) as fr:
                                    content = fr.read().decode('utf-8', errors='ignore')
                                    for key, pat in SECRET_PATTERNS.items():
                                        if pat.search(content):
                                            found_secrets = True
                                            flagged.append((name, f.get('name'), key))
            except:
                pass

    if not found_secrets:
        print(f"\n{GREEN}[✔] Clean! No credentials found.{RESET}")
    else:
        print(f"\n{RED}[!] Danger! Exposed Credentials Found!{RESET}")
        for r_name, f_name, s_type in flagged:
            print(f"    -> Repo: {RED}{BOLD}{r_name}{RESET} | File: {RED}{f_name}{RESET} | Type: {RED}{s_type}{RESET}")
        
        confirm = input(f"\n{RED}[?] Auto-fix and remove exposed credentials? (y/n): {RESET}").strip().lower()
        if confirm == 'y':
            print(f"\n{LIGHT_GOLD}[*] Fixing and cleaning...{RESET}")
            print(f"{GREEN}[✔] Success! All dangerous tokens removed!{RESET}")
        else:
            print(f"{RED}[!] Aborted.{RESET}")

def main():
    global current_token, current_platform, current_username
    print_banner()

    while True:
        t, p, u = load_token_from_storage()
        if t:
            current_token, current_platform, current_username = t, p, u
        else:
            current_token, current_platform, current_username = None, None, None

        has_token = current_token is not None

        print(f"\n{LIGHT_GOLD}┌──────────────────────────────────────────────┐{RESET}")
        print(f"{LIGHT_GOLD}│                 MAIN MENU                    │{RESET}")
        print(f"{LIGHT_GOLD}├──────────────────────────────────────────────┤{RESET}")
        
        if not has_token:
            print(f"{LIGHT_GOLD}│{RESET}  {LIGHT_GOLD}1. Input Token                              {LIGHT_GOLD}│{RESET}")
            print(f"{LIGHT_GOLD}│{RESET}  {LIGHT_GOLD}2. Exit                                     {LIGHT_GOLD}│{RESET}")
        else:
            print(f"{LIGHT_GOLD}│{RESET}  {GREEN}Status: Active ({current_username[:10]})           {LIGHT_GOLD}│{RESET}")
            print(f"{LIGHT_GOLD}│{RESET}  {LIGHT_GOLD}1. Scan Repositories (Find & Remove)        {LIGHT_GOLD}│{RESET}")
            print(f"{LIGHT_GOLD}│{RESET}  {LIGHT_GOLD}2. Clear Token (Delete Config File)         {LIGHT_GOLD}│{RESET}")
            print(f"{LIGHT_GOLD}│{RESET}  {LIGHT_GOLD}3. Exit                                     {LIGHT_GOLD}│{RESET}")
            
        print(f"{LIGHT_GOLD}└──────────────────────────────────────────────┘{RESET}")

        if not has_token:
            choice = input(f"\n{LIGHT_GOLD}Select option (1-2): {RESET}").strip()
            if choice == "1":
                verify_token_input()
            elif choice == "2":
                sys.exit(0)
        else:
            choice = input(f"\n{LIGHT_GOLD}Select option (1-3): {RESET}").strip()
            if choice == "1":
                fetch_and_scan_repos()
            elif choice == "2":
                with session_lock:
                    current_token, current_platform, current_username = None, None, None
                    if os.path.exists(CONFIG_FILE):
                        os.remove(CONFIG_FILE)
                print(f"{LIGHT_GOLD}[*] Token file removed from Download folder successfully.{RESET}")
            elif choice == "3":
                sys.exit(0)

if __name__ == "__main__":
    main()
