# Cyber Defense Suite - Option A (Minimal FIM)

This repository contains a minimal, GitHub-ready File Integrity Monitor (FIM) daemon implemented in Python.
It uses `watchdog` for filesystem events and `hashlib` for SHA384 hashing. The project is intended as a
starting point for a production-ready FIM.

## Features 
- Watchdog-based file event monitoring (create/modify/delete)
- SHA384 hashing for baseline and checks
- Baseline creation and storage (JSON)
- Simple logging to file and console
- systemd unit file provided (service/fim_daemon.service)

## Quickstart
1. Create a Python virtualenv and install requirements:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a baseline for directories you want to monitor:
   ```bash
   python -m fim_daemon.main --baseline /etc,/var/www
   ```

3. Start the daemon (for testing):
   ```bash
   python -m fim_daemon.main
   ```

4. To run as a service (Linux systemd):
   ```bash
   sudo cp service/fim_daemon.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable fim_daemon
   sudo systemctl start fim_daemon
   ```

## Notes
- This is a minimal implementation for lab and demonstration purposes.
- For production use: secure baseline storage (off-host), hardened logging, and proper permissions are recommended.
