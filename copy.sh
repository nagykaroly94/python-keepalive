#!/bin/bash

sudo cp mysql.py /usr/local/lib/keep-alive/mysql.py
sudo cp keep-alive.service /etc/systemd/system/keep-alive.service

sudo systemctl daemon-reload

sudo systemctl enable keep-alive.service && sudo systemctl start keep-alive.service