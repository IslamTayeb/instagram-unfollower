from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("instagram_unfollow.log"), logging.StreamHandler()],
)


def unfollow_non_followers(username, password):
    logging.info("Starting unfollow process")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        logging.info("Logging in...")
        driver.get("https://www.instagram.com/")
        time.sleep(4)

        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.submit()

        # Handle "Save Info" popup if it appears
        time.sleep(5)
        try:
            not_now = driver.find_element(By.XPATH, "//button[text()='Not Now']")
            not_now.click()
            logging.info("Handled 'Save Info' popup")
        except:
            logging.info("No 'Save Info' popup found")

        time.sleep(3)

        logging.info("Navigating to profile...")
        profile_xpath = f"//a[@href='/{username}/']"
        profile_link = wait.until(
            EC.presence_of_element_located((By.XPATH, profile_xpath))
        )
        profile_link.click()
        time.sleep(3)

        following_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/following')]/span")
            )
        )
        following_count = int(following_element.text)
        logging.info(f"Following count: {following_count}")

        following_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]"))
        )
        following_link.click()
        time.sleep(3)

        unfollowed = 0
        processed = 0

        while processed < following_count:
            try:
                buttons = wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//button[contains(@class, '_acan') and contains(text(), 'Following')]",
                        )
                    )
                )

                for button in buttons:
                    try:
                        username_element = button.find_element(
                            By.XPATH, "./ancestor::div[contains(@class, '_ab8w')]//span"
                        )
                        current_username = username_element.text
                        logging.info(f"Processing user: {current_username}")

                        button.click()
                        time.sleep(1)

                        unfollow_confirm = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[text()='Unfollow']")
                            )
                        )
                        unfollow_confirm.click()

                        unfollowed += 1
                        processed += 1
                        logging.info(
                            f"Unfollowed {current_username}. Total unfollowed: {unfollowed}"
                        )
                        time.sleep(2)

                    except Exception as e:
                        logging.error(f"Error processing user: {str(e)}")
                        processed += 1
                        continue

                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight",
                    driver.find_element(By.XPATH, "//div[@class='_aano']"),
                )
                time.sleep(2)

            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                break

        logging.info(f"Process completed. Unfollowed {unfollowed} users")

    except Exception as e:
        logging.error(f"Major error occurred: {str(e)}")

    finally:
        driver.quit()
        logging.info("Browser closed")


if __name__ == "__main__":
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    unfollow_non_followers(username, password)
