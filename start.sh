#!/bin/bash
gunicorn -w 10 -b 0.0.0.0:24572 srv:app -D
