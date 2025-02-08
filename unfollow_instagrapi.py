from instagrapi import Client
import time
import json
import logging

logging.basicConfig(level=logging.INFO)

def unfollow_non_followers(username, password):
    cl = Client()
    cl.login(username, password)
    user_id = cl.user_id

    # Load cached data if exists
    try:
        with open('instagram_cache.json', 'r') as f:
            cache = json.load(f)
            following = cache.get('following', {})
            followers = cache.get('followers', {})
            logging.info("Loaded data from cache")
    except FileNotFoundError:
        logging.info("Getting following list...")
        following = cl.user_following(user_id, amount=0)
        logging.info("Getting followers list...")
        followers = cl.user_followers(user_id, amount=0)

        # Cache the data
        with open('instagram_cache.json', 'w') as f:
            json.dump({
                'following': {str(k): v for k, v in following.items()},
                'followers': {str(k): v for k, v in followers.items()}
            }, f)

    non_followers = set(following.keys()) - set(followers.keys())
    logging.info(f"Found {len(non_followers)} non-followers")

    for i, user_id in enumerate(non_followers, 1):
        try:
            cl.user_unfollow(user_id)
            logging.info(f"Unfollowed {following[user_id].username} ({i}/{len(non_followers)})")
            time.sleep(2)  # Minimal delay to avoid rate limits
        except Exception as e:
            logging.error(f"Error unfollowing {following[user_id].username}: {e}")
            time.sleep(60)  # Longer delay on error

if __name__ == "__main__":
    username = input("Enter Instagram username: ")
    password = input("Enter Instagram password: ")
    unfollow_non_followers(username, password)
