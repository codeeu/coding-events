#!/bin/bash

# Spawn a screen with two tabs
screen -AdmS 'main' "supervisord -c /opt/supervisor.conf -n"
screen -S 'main' -X screen bash -l
screen -r 'main'
