# Instagram Non-Mutual Unfollower

This project provides a set of tools to automatically identify and unfollow users on Instagram who don't follow you back.  It uses two methods: one leveraging the `instagrapi` library for efficient unfollowing and another utilizing Selenium for a more browser-based approach.

<div align="center">
<img src="https://github.com/IslamTayeb/instagram-unfollower/blob/main/public/image-1739056283083.png?raw=true" alt="image-1739056283083.png" />
</div>

## Features

* **Identify Non-Followers:**  The `make_json.py` script identifies users you follow but who don't follow you back. The results are saved to a JSON file (`non_followers.json`).
* **Automated Unfollowing:** The `unfollow_from_json.py` script reads the JSON file generated by `make_json.py` and unfollows the listed users using the `instagrapi` library.  It includes error handling and retry mechanisms.
* **Alternative Methods of Unfollowing:** The `unfollow_selenium.py` script provides an alternative unfollowing method using Selenium to interact directly with the Instagram website. This method is more robust against changes in Instagram's interface but can be slower.

## Usage

This project consists of 3 Python scripts:

1. Move to the "code/" directory for the following commands to work.

    ```bash
    cd code
    ```

2. **`make_json.py`:** This script creates a JSON file containing a list of users you follow who don't follow you back.

    ```bash
    python make_json.py
    ```

    You will be prompted for your Instagram username and password.

3. **`unfollow_from_json.py`:** This script unfollows the users listed in `non_followers.json` using the `instagrapi` library.

    ```bash
    python unfollow_from_json.py
    ```

    You will be prompted for your Instagram username and password.

4. *(OPTIONAL)* **`unfollow_selenium.py`:** This script unfollows users you are following using Selenium. Best used if rate-limited.

    ```bash
    python unfollow_selenium.py
    ```

    You will be prompted for your Instagram username and password.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/IslamTayeb/instagram-unfollower.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    You will need a Chrome webdriver installed and configured in your system's PATH for `unfollow_selenium.py` to work.  Download the appropriate webdriver from the official ChromeDriver site for your system.

## Technologies Used

* **instagrapi:** A Python library for interacting with the Instagram API.  Used for efficient and reliable unfollowing in `unfollow_from_json.py`.
* **Selenium:** A Python library for automating web browsers. Used in `unfollow_selenium.py` to interact directly with the Instagram website.  Provides robustness against interface changes.

## Configuration

No specific configuration files are used.  Your Instagram username and password are requested directly from the command line during script execution.  The `unfollow_from_json.py` script uses `non_followers.json` as the default input file;  `unfollow_selenium.py` logs to `instagram_unfollow.log`.  Your password is not stored anywhere, neither locally nor remotely. The [instagrapi](https://github.com/subzeroid/instagrapi) library, used in this tool, is also employed by the official Instagram API and is considered safe. You can check its usage details on the official instagrapi page for further assurance.  This tool prioritizes security, and your data remains protected throughout the unfollowing process.

## Dependencies

The project dependencies are listed in `requirements.txt`.  Install them using `pip install -r requirements.txt`.

## Story

Made this since I noticed a few new irls didn't know I had an instagram account since my current Instagram account gives them a warning about potentially following a bot whenever they tried following me. To fix this, and the fact that I had way more "following" (2100~) than "followers" (1000~), I created this script to automatically unfollow all non-mutual accounts lmao

*README.md was made with [Etchr](https://etchr.dev)*
