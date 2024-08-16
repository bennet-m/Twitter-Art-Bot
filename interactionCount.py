from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://twitter.com/login")

# Need to do this because X wants to make my life difficult and it's different every time
class_name = input("Enter the class name for interaction elements (e.g., retweets, likes, views): ")

total_views = 0
unique_posts = set()
last_height = driver.execute_script("return document.body.scrollHeight")

# Function to count interactions in the current view and avoid double-counting
def count_interactions():
    global total_views
    
    tweets = driver.find_elements(By.TAG_NAME, "article")
    print(f"Found {len(tweets)} tweets in the current view")
    for tweet in tweets:
        try:
            # Get uid for the tweet
            tweet_url_elements = tweet.find_elements(By.TAG_NAME, "a")
            if tweet_url_elements:
                tweet_href = tweet_url_elements[-2].get_attribute("href")
            else:
                continue

            # Ensure the post hasn't been counted yet
            if tweet_href not in unique_posts:
                unique_posts.add(tweet_href)
                print("Processing tweet:", tweet_href)
                
                # Interaction tabs are the elements that display the number of views, likes, etc.
                interaction_tabs = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'.//div[contains(@class, "{class_name}")]')
                    )
                )
                
                if len(interaction_tabs) >= 1:
                    try:
                        # The view count is the fourth interaction tab
                        view_count = interaction_tabs[3].text.replace(",", "").strip()
                        print(f"Raw view count: {view_count}")
                        if view_count.isdigit():
                            total_views += int(view_count)
                            print(f"View count for this tweet: {view_count}, Total views: {total_views}")
                            print("Unique posts:", len(unique_posts))
                    except (ValueError, IndexError) as e:
                        print(f"Skipping due to error: {e}")
                        continue
                else: 
                    print("Skipping due to missing interaction tabs {}".format(len(interaction_tabs)))
                    print(interaction_tabs)

        except Exception as e:
            print(f"Error processing tweet: {e}")
            continue

# Scroll and count in batches with slower scrolling
while True:
    # Count interactions in the current view
    count_interactions()
    
    # Scroll down to load more posts. 
    # Since twitter loads posts dynamically, this can be a bit inaccurate. Can try smaller scroll and more sleep time if needed.
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.2);")
    time.sleep(5)
    
    # Check if we have reached the bottom of the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # Need to double check we're at the bottom because sometimes Twitter just stops displaying posts even if there are more
        if input("Press 'q' to quit or any other key to continue: ") == "q":
            break
    
    last_height = new_height

print(f"Total Views: {total_views}")
print(f"Number of Posts: {len(unique_posts)}")

driver.quit()
