# Tweet Queue Manager

Tweet Queue Manager is a system that allows you to queue tweets in Apple Notes and automatically sync them to AWS DynamoDB for scheduled posting. This project is designed to work in conjunction with the [tweet-pipeline](https://github.com/esoteric-git/tweet-pipeline) repository, which handles the actual posting of tweets.

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Deployment](#deployment)
8. [Related Projects](#related-projects)

## System Overview

The Tweet Queue Manager follows this workflow:

1. You write tweets in an Apple Note named "Tweet_Queue".
2. At 1 AM daily, a cron job triggers an Automator app that runs a macOS Shortcut.
3. The macOS Shortcut contains an AppleScript that moves tweets from the Apple Note to a `tweets.txt` file.
4. At 6 AM daily, another cron job runs `sync_tweets.sh`.
5. `sync_tweets.sh` executes `sync_tweets.py`, which uploads the staged tweets from `tweets.txt` to a DynamoDB table in AWS.

## Prerequisites

- macOS with Apple Notes
- Python 3.6+
- AWS account with DynamoDB access
- Automator and Shortcuts apps (built-in macOS applications)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/esoteric-git/tweet-queue-manager.git
   cd tweet-queue-manager
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root with the following content:
   ```
   AWS_REGION=your_aws_region
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   TABLE_NAME=your_dynamodb_table_name
   TWEETS_FILE_PATH=/path/to/tweets.txt
   TWITTER_ACCOUNT=your_twitter_account_name
   ```

2. Update the paths in the AppleScript and cron jobs to match your system setup.

3. Create the "Tweet_Queue" note in Apple Notes.

4. Set up the Automator app and macOS Shortcut:
   - Create a new Automator application named `run_tweet_script.app`.
   - Add a "Run Shortcut" action and select the "Process Tweet_Queue" shortcut.
   - Save the Automator application.

5. Create the "Process Tweet_Queue" shortcut in the Shortcuts app:
   - Create a new shortcut and add the provided AppleScript.
   - Adjust file paths as necessary.

6. Set up cron jobs:
   - Open Terminal and run `crontab -e`.
   - Add the following lines (adjust paths as needed):
     ```
     0 1 * * * open /path/to/project/run_tweet_script.app
     0 6 * * * /path/to/project/venv/bin/python /path/to/project/sync_tweets.sh
     ```

## Usage

1. Write your tweets in the "Tweet_Queue" Apple Note, separating each tweet with a soccer ball emoji (⚽️).

2. The system will automatically process your tweets daily:
   - At 1 AM, tweets will be moved from the Apple Note to `tweets.txt`.
   - At 6 AM, tweets will be uploaded to the DynamoDB table.

3. Use the [tweet-pipeline](https://github.com/esoteric-git/tweet-pipeline) project to schedule and post the tweets from DynamoDB to Twitter.

## Project Structure

tweet-queue-manager/
│
├── run_tweet_script.app
├── sync_tweets.py
├── sync_tweets.sh
├── tweets.txt
├── tweet-queue.log
├── .env
├── requirements.txt
└── venv/

- `run_tweet_script.app`: Automator application to trigger the macOS Shortcut.
- `sync_tweets.py`: Python script to upload tweets to DynamoDB.
- `sync_tweets.sh`: Shell script to run the Python script with the virtual environment.
- `tweets.txt`: Temporary storage for tweets between Apple Notes and DynamoDB.
- `tweet-queue.log`: Log file for tracking script executions.
- `.env`: The configuration file containing environment variables.
- `requirements.txt`: A file listing the Python dependencies for the project.
- `venv/`: The directory containing the Python virtual environment.

## Deployment

This project is designed to run locally on a macOS system. Ensure that your Mac is powered on and connected to the internet at the scheduled cron job times for the system to function properly.

## Related Projects

- [tweet-pipeline](https://github.com/esoteric-git/tweet-pipeline): A serverless CI/CD pipeline using AWS Lambda and Step Functions to schedule and post tweets to Twitter in a human-like cadence.

