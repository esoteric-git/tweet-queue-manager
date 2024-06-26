import os
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from .env
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
TABLE_NAME = os.getenv('TABLE_NAME')
TWEETS_FILE_PATH = os.getenv('TWEETS_FILE_PATH')
TWITTER_ACCOUNT = os.getenv('TWITTER_ACCOUNT')

# Initialize the DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
table = dynamodb.Table(TABLE_NAME)

def get_tweets_from_file(file_path):
    with open(file_path, 'r') as file:
        tweets = file.read().split('⚽️')  # Split tweets by the soccer ball emoji delimiter
    return [tweet.strip() for tweet in tweets if tweet.strip()]

def upload_tweets_to_dynamodb(tweets):
    for tweet in tweets:
        tweet_id = str(datetime.now().timestamp())
        table.put_item(
            Item={
                'id': tweet_id,
                'tweet': tweet,
                'posted': False,
                'twitter_account': TWITTER_ACCOUNT
            }
        )
    print(f"{len(tweets)} tweets uploaded to DynamoDB table {TABLE_NAME} for account {TWITTER_ACCOUNT}.")


def main():
    tweets = get_tweets_from_file(TWEETS_FILE_PATH)
    if tweets:
        upload_tweets_to_dynamodb(tweets)
    else:
        print("No tweets to upload.")

if __name__ == "__main__":
    main()
