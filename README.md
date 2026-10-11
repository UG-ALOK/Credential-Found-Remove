# 🛡️ Credential Found & Remove Tool

**Credential Found & Remove Tool** is a lightweight, high-security utility designed specifically for terminal environments (such as Termux and Linux). It allows developers to securely manage their remote repositories, scan for accidentally exposed API keys, personal access tokens (PATs), and sensitive credentials, and safely remediate them to prevent security breaches.

---

## 🌐 Supported Platforms
The tool seamlessly integrates and works with the following major version control platforms:
* **GitHub** (`github.com`)
* **Codeberg** (`codeberg.org`)
* **GitLab** (`gitlab.com`)
* **Bitbucket** (`bitbucket.org`)
* **Gitea** (`gitea.com` or self-hosted instances)

---

## 🚀 Key Features
* **Global Terminal Command:** Install once and run directly from anywhere using a simple custom command without typing `python`.
* **Advanced Security & Auto-Reset:** Stores encrypted tokens safely in your device's internal **Download** folder and automatically wipes/resets session configurations every **2 minutes** to prevent leaks.
* **Real-Time Content Scanning:** Deep-scans repository buffers to detect hardcoded secrets, private keys, and PATs.
* **Smart UI & Color Coding:** Clean, interactive terminal menus optimized for mobile screens (Termux) and Linux shells.
* **Interactive Auto-Fix:** Prompts user confirmation before automatically cleaning or removing vulnerabilities.

---

## ⚠️ Important Note on Permissions & Security
Modern code hosting platforms enforce strict security policies. Therefore, **administrator permissions and a valid Personal Access Token (PAT)** with repository write scopes are strictly required to modify or clean remote files.

---

## 📦 Installation (Termux / Linux)

To download, set up the global command, and configure storage permissions, run the following commands:

```bash
git clone https://github.com/UG-ALOK/Credential-Found-Remove.git
```
```bash
cd Credential-Found-Remove
```
```bash
chmod +x install.sh
```
```bash
bash install.sh
```
# 💡 Usage
​Once the installation is complete, you no longer need to type
RUN
```bash
python main.py
```
---

## 🛠️ Quick Start Guide

* **Input Token:** Select **Option 1** from the main menu to input and verify your Personal Access Token. The token will be safely stored in your internal `Download` folder.
* **Scan & Remediate:** Choose repository scanning options to inspect live projects. If any exposed credentials are found, confirm with `y` to clean them.
* **Auto-Reset Security:** For enhanced safety, the token session automatically expires and deletes itself every **2 minutes**. You can also manually clear the token using **Option 2** in the active menu.

---

## 🔑 How to Generate a Personal Access Token (PAT)

### 1. GitHub
* Navigate to **Settings** > **Developer settings** > **Personal access tokens**.
* Generate a new token and grant `contents` (**Read and write**) and `metadata` permissions.

### 2. GitLab
* Navigate to **Preferences** > **Access Tokens**.
* Create a token with `api` or `write_repository` scopes enabled.

### 3. Codeberg / Gitea
* Navigate to **Settings** > **Applications** > **Manage Access Tokens**.
* Generate a new token with appropriate repository write scopes.

---

## 👨‍💻 Developer
* **Developer:** Raj-u

---

## 📄 License & Disclaimer
This tool is designed strictly for **defensive self-auditing** and managing your own repositories. Please read the `DISCLAIMER.md` file carefully before use.
