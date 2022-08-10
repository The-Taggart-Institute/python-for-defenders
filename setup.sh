#!/bin/bash

echo "[+] Installing dependencies"

sudo apt update
sudo apt install -y python3-pip python3-venv
sudo pip3 install jupyterlab plotly ipywidgets pandas jupyter-dash

echo "[+] Installing Poetry"

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
