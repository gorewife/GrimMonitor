#!/bin/bash
# Quick push script for GrimMonitor

git add .
git commit -m "${1:-Quick update}" 
git push
