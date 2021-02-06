#! /bin/sh
sleep 30 # wait for kafka broker to start
exec python parser/parser.py
