#!/bin/bash

echo "[+] Installing dependencies"

sudo apt update
sudo apt install -y python3-pip python3-venv

echo "[+] Installing Poetry"

curl -sSL https://install.python-poetry.org | python3 -

echo "[+] Installing Poetry Dependencies"
poetry install

echo "[+] Done! Run 'poetry shell' to activate the environment"
