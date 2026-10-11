#!/usr/bin/env bash

# ANSI Color Codes for Professional Terminal Output
RESET="\033[0m"
BOLD="\033[1m"
RED="\033[91m"
GREEN="\033[92m"
LIGHT_GOLD="\033[33m"
CYAN="\033[96m"

echo -e "${LIGHT_GOLD}${BOLD}"
echo "=================================================="
echo "   INSTALLING CREDENTIAL FOUND & REMOVE TOOL"
echo "            [ Developer : Raj Alok ]"
echo "=================================================="
echo -e "${RESET}"

# Step 1: Check for Python3
echo -e "${LIGHT_GOLD}[*] Checking Python3 installation...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 is not installed! Installing Python3...${RESET}"
    if command -v pkg &> /dev/null; then
        pkg update -y && pkg install python3 -y
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install python3 -y
    else
        echo -e "${RED}[!] Please install Python3 manually to proceed.${RESET}"
        exit 1
    fi
else
    echo -e "${GREEN}[✔] Python3 is already installed.${RESET}"
fi

# Step 2: Make main.py executable
echo -e "${LIGHT_GOLD}[*] Setting up execution permissions for main.py...${RESET}"
if [ -f "main.py" ]; then
    chmod +x main.py
    echo -e "${GREEN}[✔] Permission granted successfully.${RESET}"
else
    echo -e "${RED}[!] Error: main.py not found in the current directory!${RESET}"
    exit 1
fi

# Step 3: Check and request storage permissions (Specifically for Termux)
if [ -d "/data/data/com.termux" ]; then
    echo -e "${LIGHT_GOLD}[*] Detected Termux environment. Setting up storage access...${RESET}"
    if ! [ -d "/storage/emulated/0/Download" ]; then
        echo -e "${CYAN}[i] Requesting storage permission (termux-setup-storage)...${RESET}"
        termux-setup-storage
    else
        echo -e "${GREEN}[✔] Internal storage access verified.${RESET}"
    fi
fi

echo -e "\n${GREEN}${BOLD}=================================================="
echo "          INSTALLATION COMPLETED SUCCESSFULLY!"
echo "=================================================="
echo -e "${RESET}"
echo -e "${LIGHT_GOLD}To run the tool, simply type:${RESET}"
echo -e "${CYAN}python main.py${RESET}\n"
