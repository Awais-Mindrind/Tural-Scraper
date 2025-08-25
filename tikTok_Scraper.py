import time, random, re
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from schemas import Profile
from utils import parse_count 
from airtable import save_profile_to_airtable, get_existing_usernames

# CONFIGURATION
BASE_HASHTAG = "games"
NUM_PROFILES = 500
SCROLL_PAUSE = (2, 4)


def get_driver():
    # 🔹 Add Proxy Here
    proxy = "c7a43522e2000b561ab6__cr.us:b16012b413a3bddf@gw.dataimpulse.com:823"
    
    driver = Driver(browser="chrome", proxy=proxy, uc=True, headless=True, no_sandbox=True, window_size="1920,1080", disable_gpu=True)
    driver.implicitly_wait(10)
    return driver

def human_sleep(min_s, max_s):
    time.sleep(random.uniform(min_s, max_s))

def extract_username_from_url(url):
    match = re.search(r"tiktok\.com/@([\w\.\-]+)", url)
    return match.group(1) if match else None

def generate_country_hashtags(base_hashtag):
    countries = [
        "usa", "uk", "canada", "australia", "germany", "france", "italy",
        "spain", "japan", "china", "india", "brazil", "mexico", "russia",
        "southkorea", "uae", "saudiarabia", "turkey", "indonesia", "singapore"
    ]
    hashtag_variations = []
    for country in countries:
        hashtag_variations.append((f"{base_hashtag}{country}", country))
        hashtag_variations.append((f"{base_hashtag}_{country}", country))
        hashtag_variations.append((f"{base_hashtag}-in-{country}", country))
        hashtag_variations.append((f"{base_hashtag}-{country}", country))
    return hashtag_variations

def get_unique_profiles_via_videos(driver, hashtag, num_profiles, profile_urls, country):
    hashtag_url = f"https://www.tiktok.com/tag/{hashtag}"
    driver.get(hashtag_url)
    human_sleep(5, 7)

    video_elements = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(profile_urls) < num_profiles:
        video_cards = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')
        print(f"Found {len(video_cards)} video cards for #{hashtag}")

        for video in video_cards:
            try:
                if video in video_elements:
                    continue
                video_elements.add(video)
                video_link = video.get_attribute("href")
                if not video_link:
                    continue
                profile_url = video_link.split("/video/")[0]
                if profile_url in [p["profile_link"] for p in profile_urls]:
                    continue
                profile_urls.append({"profile_link": profile_url, "country": country})
                print(f"Collected profile: {profile_url} ({len(profile_urls)}/{num_profiles})")
                if len(profile_urls) >= num_profiles:
                    return
            except Exception:
                continue

        driver.execute_script("window.scrollBy(0, 800);")
        human_sleep(*SCROLL_PAUSE)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more scrolling possible.")
            break
        last_height = new_height

def scrape_tiktok_profiles(base_hashtag=BASE_HASHTAG, num_profiles=NUM_PROFILES):
    driver = get_driver()
    all_profiles = []
    existing_usernames = set(get_existing_usernames())

    try:
        hashtag_country_pairs = generate_country_hashtags(base_hashtag)

        # Phase 1: Collect all profile URLs first
        print("\n📥 Collecting profile URLs...")
        for hashtag, country in hashtag_country_pairs:
            if len(all_profiles) >= num_profiles:
                break
            get_unique_profiles_via_videos(driver, hashtag, num_profiles, all_profiles, country)

        print(f"\n✅ Finished collecting {len(all_profiles)} profiles.\n")

        # Phase 2: Scrape profiles
        scraped_profiles = []
        for profile in all_profiles:
            url = profile["profile_link"]
            country = profile["country"]
            print(f"Scraping profile: {url} (Country: {country})")
            driver.get(url)
            human_sleep(3, 5)

            try:
                username = extract_username_from_url(url)
                bio, followers = "", ""
                if username in existing_usernames:
                    print(f"Skipping {profile['Username']} - already in Airtable")
                    continue
                print(f"Collected profile: {username} ({len(scraped_profiles)+1}/{len(existing_usernames)})")

                try:
                    bio_elem = driver.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-bio"]')
                    bio = bio_elem.text.strip()
                except NoSuchElementException:
                    pass

                try:
                    stats = driver.find_elements(By.CSS_SELECTOR, 'strong[data-e2e="followers-count"]')
                    if stats:
                        followers = stats[0].text.strip()
                        print("Followers: ",followers)
                except:
                    pass
                try:
                    likes_elem = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="likes-count"]')
                    likes = likes_elem.text.strip()
                except NoSuchElementException:
                    pass

                try:
                    img_elem = driver.find_element(By.CSS_SELECTOR, 'div[data-e2e="user-avatar"]').find_element(By.TAG_NAME,"img")
                    image_url = img_elem.get_attribute("src")
                except NoSuchElementException:
                    pass
                profile_data = {
                    "Username": username,
                    "Bio": bio,
                    "Followers": parse_count(followers),
                    "Likes": parse_count(likes),
                    "Profile_URL": url,
                    "Image_URL": image_url,
                    "Country": country.upper(),
                    "Hashtag": base_hashtag.lower()
                }
                profile_data = Profile(
                    Username= username,
                    Bio=bio,
                    Followers= parse_count(followers),
                    Likes= parse_count(likes),
                    Profile_URL= url,
                    Image_URL= image_url,
                    Country= country.upper(),
                    Hashtag= base_hashtag.lower()
                )
                save_profile_to_airtable(profile_data.dict())
                scraped_profiles.append(profile_data.dict())


            except Exception as e:
                print(f"Error scraping {url}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    except KeyboardInterrupt:
        print("Keyboard Interupted")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_tiktok_profiles()
