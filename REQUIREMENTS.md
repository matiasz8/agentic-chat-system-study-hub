# Requirements Setup Guide

This project requires **Node.js** and **Python 3** to run.

## ❌ Issue: "npm: No such file or directory"

This error means Node.js is not installed or not in your PATH.

## ✅ Solution: Install Node.js

### Option 1: Using NVM (Recommended for Linux/Mac)

```bash
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart your terminal or run:
source ~/.bashrc

# Install latest Node.js (includes npm)
nvm install node

# Verify installation
node --version
npm --version
```

### Option 2: Direct Download (All Platforms)

Visit [nodejs.org](https://nodejs.org/) and download:
- **LTS (Long Term Support)** - Recommended for stability
- Choose your operating system (Linux, Mac, Windows)

After installation, verify:
```bash
node --version
npm --version
```

### Option 3: Using Package Manager

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nodejs npm
```

**Mac (Homebrew):**
```bash
brew install node
```

**Windows (Chocolatey):**
```bash
choco install nodejs
```

## 🐍 Python Requirements

Python 3.9+ is also required. Check:
```bash
python3 --version
```

If not installed, visit [python.org](https://www.python.org/)

## ✅ Verify Everything is Ready

Once installed, run:
```bash
make check-requirements
```

This will confirm both Node.js and Python are available.

## 🚀 Now You Can Use Make

After installation, try:
```bash
make help          # Show all available commands
make install       # Install dependencies
make run           # Start development server
```

## 🆘 Troubleshooting

### If `make check-requirements` still fails:

**Mac/Linux:** Check your PATH:
```bash
echo $PATH
```

**Windows:** Make sure Node.js is in your system PATH. Restart your terminal after installation.

### If npm still not found after installation:

Try restart your terminal/shell, or:
```bash
# Mac/Linux
source ~/.bashrc
source ~/.zshrc

# Then check again
npm --version
```

---

**Need help?** Run `make help` or see the Makefile for all available commands.
