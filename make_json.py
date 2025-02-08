from instagrapi import Client
import json
from datetime import datetime
import getpass
import logging
import sys
import time


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("instagram_audit.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def get_non_followers():
    logger = setup_logging()
    max_retries = 3
    retry_delay = 300  # 5 minutes

    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")

    for attempt in range(max_retries):
        try:
            cl = Client()
            cl.login(username, password)

            user_id = cl.user_id
            logger.info(f"Logged in successfully as {username}")

            logger.info("Fetching followers...")
            followers = cl.user_followers(user_id)

            logger.info("Fetching following...")
            following = cl.user_following(user_id)

            non_followers = []
            for user_id, user_info in following.items():
                if user_id not in followers:
                    non_followers.append(
                        {"id": user_id, "username": user_info.username}
                    )
                    logger.debug(f"Found non-follower: {user_info.username}")

            output = {
                "timestamp": datetime.now().isoformat(),
                "non_followers": non_followers,
            }

            with open("non_followers.json", "w") as f:
                json.dump(output, f, indent=2)

            logger.info(
                f"Saved {len(non_followers)} non-followers to non_followers.json"
            )
            break

        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Exiting.")
                raise


if __name__ == "__main__":
    get_non_followers()
