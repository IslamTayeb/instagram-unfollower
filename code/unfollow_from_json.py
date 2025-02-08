from instagrapi import Client
import json
import time
import random
import logging
from datetime import datetime
import os

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = f"logs/unfollow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


def unfollow_from_json(username, password, json_file="non_followers.json"):
    logging.info("=== Starting Instagram Unfollow Process ===")

    cl = Client()
    logging.info("Logging in...")
    cl.login(username, password)
    logging.info("Login successful!")

    with open(json_file) as f:
        data = json.load(f)
        users = data["non_followers"]
    logging.info(f"Loaded {len(users)} users to unfollow")

    successful = 0
    failed = 0
    consecutive_fails = 0
    skipped = 0

    for i, user in enumerate(users, 1):
        user_id = user["id"]
        username = user["username"]

        logging.info(f"\n[{i}/{len(users)}] Processing @{username}")

        try:
            result = cl.user_unfollow(user_id)

            if result:
                successful += 1
                consecutive_fails = 0
                logging.info(f"✓ Successfully unfollowed @{username}")
                delay = random.uniform(0, 1)
                logging.info(f"Waiting {delay:.1f}s...")
                time.sleep(delay)
            else:
                raise Exception("Unfollow request failed")

        except Exception as e:
            failed += 1
            consecutive_fails += 1
            logging.error(f"✗ Failed to unfollow @{username}: {str(e)}")

            if consecutive_fails >= 3:
                delay = 300
                logging.warning(f"Taking a {delay}s break...")
                time.sleep(delay)
                consecutive_fails = 0
            else:
                delay = 3
                logging.info(f"Waiting {delay}s...")
                time.sleep(delay)

        logging.info(f"Progress: {(i/len(users))*100:.1f}%")
        logging.info(f"Success: {successful} | Failed: {failed} | Skipped: {skipped}")

    logging.info("\n=== Final Summary ===")
    logging.info(f"Total processed: {len(users)}")
    logging.info(f"Successful unfollows: {successful}")
    logging.info(f"Failed unfollows: {failed}")
    logging.info(f"Skipped users: {skipped}")
    logging.info(f"Success rate: {(successful/(len(users)-skipped))*100:.1f}%")


if __name__ == "__main__":
    username = input("Instagram username: ")
    password = input("Instagram password: ")
    unfollow_from_json(username, password)
