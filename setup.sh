#!/bin/bash

echo "[+] Installing dependencies"

sudo apt update
sudo apt install -y python3-pip python3-venv

echo "[+] Installing Poetry"

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

echo "[+] Installing Poetry Dependencies"
poetry install

echo "[+] Done! Run 'poetry shell' to activate the environment"
