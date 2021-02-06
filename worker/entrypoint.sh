#! /bin/sh
sleep 30 # wait for kafka broker to start
exec flask run --host=0.0.0.0