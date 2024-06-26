#!/bin/bash

# Load environment variables from the .env file
export $(grep -v '^#' .env | xargs)

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python sync_tweets.py

# Check if the Python script ran successfully and log it
if [ $? -eq 0 ]; then
  echo "$(date): sync_tweets.py ran successfully" >> ./tweet-queue.log
else
  echo "$(date): sync_tweets.py encountered an error" >> ./tweet-queue.log
fi