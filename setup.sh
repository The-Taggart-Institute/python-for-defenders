#!/bin/bash

echo "[+] Installing dependencies"

sudo apt update
sudo apt install -y python3-pip
sudo pip3 install jupyterlab plotly ipywidgets pandas jupyter-dash

