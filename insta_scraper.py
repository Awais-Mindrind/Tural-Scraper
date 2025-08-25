import time
import random
import csv
import re
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from utils import parse_count , format_count
from dotenv import load_dotenv
load_dotenv()

username =  os.getenv("USERNAME")
password = os.getenv("PASSWORD")

HASHTAG = "food"
NUM_PROFILES = 20

def get_driver():
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--window-size=1920,1080")  # Set window size
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # Set implicit wait time
    return driver

def human_sleep(min_s, max_s):
    time.sleep(random.uniform(min_s, max_s))

def get_follower_count(text):
    match = re.search(r"([\d\.]+)([kKmMbB]?)", text)
    if match:
        num, suffix = match.groups()
        multiplier = {'': 1, 'k': 1e3, 'm': 1e6, 'b': 1e9}
        return int(float(num) * multiplier.get(suffix.lower(), 1))
    return 0

def scrape_instagram():
    driver = get_driver()
    username =  os.getenv("USERNAME")
    password = os.getenv("PASSWORD") 
    driver.get("https://www.instagram.com/accounts/login/")
    human_sleep(3, 5)
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    human_sleep(2, 3)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    human_sleep(5, 7)
    cookies = driver.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f, indent=4)
    print("🔑 Cookies saved to cookies.json")

    # 🧠 Manually log in and bypass any 2FA, CAPTCHA, etc.
    input("✅ After you log in manually, press ENTER here to continue...")

    hashtag_url = f"https://www.instagram.com/explore/tags/{HASHTAG}/"
    driver.get(hashtag_url)
    human_sleep(5, 7)

    profile_links = set()

    print("🔍 Scraping post links under hashtag...")

    # Click on posts and collect profile URLs
    post_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')
    for post in post_links[:NUM_PROFILES * 2]:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", post)
            human_sleep(2, 3)
            post.click()
            human_sleep(2, 4)

            # Click username link
            username_elem = driver.find_element(By.CSS_SELECTOR, 'a[href^="/"][role="link"]')
            profile_url = "https://www.instagram.com" + username_elem.get_attribute("href")
            profile_links.add(profile_url)

            close_btn = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_btn.click()
            human_sleep(1, 2)

            if len(profile_links) >= NUM_PROFILES:
                break

        except Exception as e:
            print("⚠️ Error scraping post/profile:", e)
            continue

    print(f"✅ Found {len(profile_links)} profile links")

    profiles = []

    for url in list(profile_links)[:NUM_PROFILES]:
        print(f"🔍 Scraping profile: {url}")
        driver.get(url)
        human_sleep(4, 6)

        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Username from URL
            username = url.strip("/").split("/")[-1]

            # Bio
            bio_tag = soup.find("div", {"class": "_aa_c"})
            bio = bio_tag.text.strip() if bio_tag else ""

            # Email if present in bio
            email = ""
            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", bio)
            if email_match:
                email = email_match.group(0)

            # Follower count
            follower_text = soup.find_all("span", {"class": "_ac2a"})
            followers = "N/A"
            if follower_text:
                followers = get_follower_count(follower_text[0].text)

            profiles.append({
                "username": username,
                "profile_link": url,
                "bio": bio,
                "email": email,
                "followers": parse_count(followers)
            })

        except Exception as e:
            print("⚠️ Failed to scrape profile info:", e)
            continue

    # Save results
    with open(f"{HASHTAG}_instagram_influencers.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "profile_link", "bio", "email", "followers"])
        writer.writeheader()
        for row in profiles:
            writer.writerow(row)

    print("✅ Done! Saved to CSV.")
    driver.quit()

if __name__ == "__main__":
    scrape_instagram()
