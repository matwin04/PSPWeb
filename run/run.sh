#!/bin/bash

# Run app.py in the background
python3 app.py &

# Run scanner.py in the foreground
python3 scanner.py
