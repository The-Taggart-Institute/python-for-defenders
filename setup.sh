#!/bin/bash

echo "[+] Installing dependencies"

sudo apt update
sudo apt install -y python3-pip python3-venv pipx

echo "[+] Installing Poetry"

pipx install poetry
pipx ensurepath

echo "[+] Installing Poetry Dependencies"
~/.local/bin/poetry install

echo "[+] Done! Run 'poetry env activate' and the command provided afterward to activate the environment. Deactivate with 'deactivate.'"
