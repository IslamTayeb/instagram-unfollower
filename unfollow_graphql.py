from instagram_private_api import Client, ClientCompatPatch
import time
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            f'instagram_unfollow_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        ),
        logging.StreamHandler(),
    ],
)


def unfollow_non_followers(username, password):
    logging.info("Initializing Instagram API client...")
    api = Client(username, password)
    user_id = api.authenticated_user_id
    logging.info(f"Logged in successfully as {username} (ID: {user_id})")

    following = []
    followers = []
    rank_token = Client.generate_uuid()

    # Get following
    logging.info("Fetching following list...")
    results = api.user_following(user_id, rank_token=rank_token)
    following.extend(results.get("users", []))
    logging.info(f"Initial batch: {len(following)} following")

    next_max_id = results.get("next_max_id")
    while next_max_id:
        logging.info(f"Fetching next batch of following (max_id: {next_max_id})")
        results = api.user_following(user_id, rank_token=rank_token, max_id=next_max_id)
        batch = results.get("users", [])
        following.extend(batch)
        logging.info(f"Added {len(batch)} users. Total following: {len(following)}")
        next_max_id = results.get("next_max_id")
        time.sleep(1)

    # Get followers
    logging.info("\nFetching followers list...")
    results = api.user_followers(user_id, rank_token=rank_token)
    followers.extend(results.get("users", []))
    logging.info(f"Initial batch: {len(followers)} followers")

    next_max_id = results.get("next_max_id")
    while next_max_id:
        logging.info(f"Fetching next batch of followers (max_id: {next_max_id})")
        results = api.user_followers(user_id, rank_token=rank_token, max_id=next_max_id)
        batch = results.get("users", [])
        followers.extend(batch)
        logging.info(f"Added {len(batch)} users. Total followers: {len(followers)}")
        next_max_id = results.get("next_max_id")
        time.sleep(1)

    # Find non-followers
    following_dict = {user["pk"]: user["username"] for user in following}
    follower_dict = {user["pk"]: user["username"] for user in followers}

    non_follower_ids = set(following_dict.keys()) - set(follower_dict.keys())
    logging.info(f"\nAnalysis Complete:")
    logging.info(f"Total following: {len(following_dict)}")
    logging.info(f"Total followers: {len(follower_dict)}")
    logging.info(f"Found {len(non_follower_ids)} non-followers")

    # Save data to file
    data = {
        "timestamp": datetime.now().isoformat(),
        "non_followers": [
            {"id": user_id, "username": following_dict[user_id]}
            for user_id in non_follower_ids
        ],
    }
    with open("non_followers.json", "w") as f:
        json.dump(data, f, indent=2)
    logging.info("Saved non-followers list to non_followers.json")

    # Unfollow
    logging.info("\nStarting unfollow process...")
    for i, user_id in enumerate(non_follower_ids, 1):
        username = following_dict[user_id]
        try:
            logging.info(f"Unfollowing {username} ({i}/{len(non_follower_ids)})")
            api.friendships_destroy(user_id)
            logging.info(f"Successfully unfollowed {username}")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to unfollow {username}: {str(e)}")
            logging.info("Waiting 60 seconds before continuing...")
            time.sleep(60)

    logging.info("\nProcess complete!")


if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    unfollow_non_followers(username, password)
