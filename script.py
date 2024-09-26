import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Suppress TensorFlow logging (if applicable)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

# Function to scroll the webpage for a given duration with slower speed
def scroll_page(browser, duration):
    start_time = time.time()
    last_height = browser.execute_script("return document.body.scrollHeight")  # Get initial scroll height

    while time.time() - start_time < duration:
        # Scroll down by a smaller amount (e.g., 100 pixels)
        browser.execute_script("window.scrollBy(0, 100);")
        time.sleep(2)  # Increased delay between scrolls

        # Check new scroll height after scrolling
        new_height = browser.execute_script("return document.body.scrollHeight")

        # If the new height is the same as the last height, we've reached the bottom
        if new_height == last_height:
            # Scroll to the bottom of the page to load more content
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for a moment to load more content
            new_height = browser.execute_script("return document.body.scrollHeight")  # Update the height

            # If still the same, restart scrolling from the top
            if new_height == last_height:
                browser.execute_script("window.scrollTo(0, 0);")  # Scroll back to the top
                time.sleep(2)  # Wait before scrolling down again
                last_height = browser.execute_script("return document.body.scrollHeight")  # Update height after resetting

        last_height = new_height  # Update the last height for the next check

def main(search_queries, iterations):
    # Create a Chrome browser instance with options
    options = Options()
    options.add_argument("--start-maximized")  # Start Chrome in maximized mode

    # Create a browser instance
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for i in range(iterations):
        for query in search_queries:
            print(f"Iteration {i + 1}: Searching for '{query}'...")

            # Load the Google homepage
            browser.get('https://www.google.com')

            # Search for the given query
            search_box = browser.find_element(By.NAME, 'q')
            search_box.send_keys(query + Keys.RETURN)

            # Wait for search results to load
            time.sleep(3)

            # Initialize a variable to track if the target URL was found
            target_found = False

            while not target_found:
                # Attempt to find the link that contains "hireremotestars.com"
                try:
                    first_result = browser.find_element(By.XPATH, "//a[contains(@href, 'hireremotestars.com/hire-remote-software-developers')]")
                    print("Found the target link, clicking...")
                    first_result.click()
                    target_found = True  # Set to true once the target is found
                except Exception as e:
                    print("Target link not found on this page. Checking next page...")
                    try:
                        # Check for the "Next" button to navigate to the next search results page
                        next_button = browser.find_element(By.XPATH, "//a[@id='pnnext']")
                        next_button.click()
                        time.sleep(3)  # Wait for the new page to load
                    except Exception as e:
                        print("No more pages available or an error occurred.")
                        break  # Exit the loop if there are no more pages

            # Wait for the website to load if the target was found
            if target_found:
                time.sleep(5)

                # Scroll the website for 1 minute with slower speed
                scroll_page(browser, 60)

                # Visit other website pages by clicking buttons/links
                links = browser.find_elements(By.TAG_NAME, 'a')  # Find all links on the page
                for link in links:
                    try:
                        link.click()  # Click the link
                        time.sleep(3)  # Wait for the new page to load

                        # Scroll the new page for 1 minute with slower speed
                        scroll_page(browser, 60)

                        # Go back to the previous page after interacting with the new page
                        browser.back()
                        time.sleep(3)
                    except Exception as e:
                        print(f"Error clicking link: {e}")
                        continue

        # Open a new tab for the next iteration
        if i < iterations - 1 or query != search_queries[-1]:  # Avoid opening a new tab after the last iteration
            browser.execute_script("window.open('');")  # Open a new tab
            browser.switch_to.window(browser.window_handles[-1])  # Switch to the new tab

    # Close the browser after all tasks are completed
    browser.quit()

if __name__ == "__main__":
    # Get parameters from command line arguments
    queries = "hire remote software developers at hire remote stars"  # Default search queries
    iterations = 50  # Default number of iterations

    if len(sys.argv) > 1:
        queries = sys.argv[1]  # Take the first argument as the search queries
    if len(sys.argv) > 2:
        iterations = int(sys.argv[2])  # Take the second argument as the number of iterations

    # Split the queries into a list
    search_queries = [query.strip() for query in queries.split(',')]
    main(search_queries, iterations)
