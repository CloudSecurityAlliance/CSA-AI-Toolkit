#!/bin/bash

#
# Make sure we're in a venv first
#
echo "make sure you're in a venv first"
echo "To create the venv:"
echo "python3 -m venv .venv-CSA-AI-Toolkit"
echo "echo \".venv-CSA-AI-Toolkit\" >> .gitignore"
echo ""
echo "Then you need to run"
echo "source .venv-CSA-AI-Toolkit/bin/activate"
echo ""
sleep 1
echo 5
sleep 1
echo 4
sleep 1
echo 3
sleep 1
echo 2
sleep 1
echo 1
sleep 1

# Pip install all the things

pip3 install anthropic
pip3 install google-generativeai
pip3 install openai
