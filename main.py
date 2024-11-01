from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Initialize vote count dictionary
votes = {}

# Set up Chrome WebDriver with context manager to ensure cleanup
with webdriver.Chrome() as driver:
    driver.get("https://web.whatsapp.com")

    # Wait until the chat list is fully loaded
    wait = WebDriverWait(driver, 30)
    try:
        chat_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Chat list"]')))
    except TimeoutException:
        print("Timeout: Chat list not found.")
        driver.quit()

    # Extract all chat elements
    chat_elements = chat_list.find_elements(By.XPATH, './*')

    for index, chat in enumerate(chat_elements):
        chat.click()  # Open each chat
        time.sleep(0.5)  # Brief pause to ensure chat loads

        # Try to locate the poll message
        try:
            poll_element = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "Poll from you")]'))
            )
            # Process the poll options
            aria_label_value = poll_element.get_attribute("aria-label")
            options = aria_label_value.split(":", 2)[-1].split(",")

            # Parse options and update the vote count
            for option in options:
                try:
                    key = option.split(":")[0].strip()
                    value = int(option.split(":")[1].replace(".", "").strip())
                    votes[key] = votes.get(key, 0) + value
                except ValueError:
                    print(f"Could not parse vote count for option '{option}'")
        except TimeoutException:
            print(f"Child {index + 1}: No poll element found.")
        except NoSuchElementException:
            print(f"Child {index + 1}: Error accessing poll element.")

    # Final vote count
    print("Final Vote Counts:", votes)
