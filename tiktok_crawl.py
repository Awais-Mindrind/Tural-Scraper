import asyncio, random, re, os, math
from typing import List, Dict, Tuple, Set

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai import ProxyConfig, RoundRobinProxyStrategy, CacheMode
# your existing helpers
from schemas import Profile
from utils import parse_count
from airtable import save_profile_to_airtable, get_existing_usernames

# --------------------------
# CONFIGURATION (tweakable)
# --------------------------
BASE_HASHTAG = "Sports"
NUM_PROFILES = 500
SCROLL_PAUSE = (2.0, 4.0)
HEADLESS = False

# Optional proxy (HTTP or SOCKS). Set via env or inline here.
PROXY_SERVER = os.getenv("PROXY_SERVER")  # e.g. "http://username:password@host:port"
PROXY_USERNAME = os.getenv("PROXY_USERNAME")  # optional when embedded in PROXY_SERVER
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")  # optional when embedded in PROXY_SERVER
PROXY_PORT = os.getenv("PROXY_PORT","823")  # optional, if needed separately

# For identity-based crawling (keep cookies/login). Leave None to disable.
USER_DATA_DIR = os.getenv("C4AI_USER_DATA_DIR")  # e.g. "/path/to/chrome-profile-dir"

# --------------------------
# Utilities
# --------------------------
def human_delay(a: float, b: float) -> float:
    return random.uniform(a, b)

def extract_username_from_url(url: str) -> str:
    m = re.search(r"tiktok\.com/@([\w\.\-]+)", url)
    return m.group(1) if m else None

def generate_country_hashtags(base_hashtag: str) -> List[Tuple[str, str]]:
    countries = [
        "usa", "uk", "canada", "australia", "germany", "france", "italy",
        "spain", "japan", "china", "india", "brazil", "mexico", "russia",
        "southkorea", "uae", "saudiarabia", "turkey", "indonesia", "singapore"
    ]
    out = []
    for c in countries:
        out.append((f"{base_hashtag}{c}", c))
        out.append((f"{base_hashtag}_{c}", c))
        out.append((f"{base_hashtag}-in-{c}", c))
        out.append((f"{base_hashtag}-{c}", c))
    return out

def base_profile_from_video_link(href: str) -> str:
    # "https://www.tiktok.com/@user/video/123..." -> "https://www.tiktok.com/@user"
    if "/video/" in href:
        return href.split("/video/")[0]
    return href

def pick_unique_profile(profile_url: str, seen: Set[str]) -> bool:
    if not profile_url:
        return False
    if not re.search(r"tiktok\.com/@", profile_url):
        return False
    if profile_url in seen:
        return False
    seen.add(profile_url)
    return True

def extract_bio(html: str) -> str:
    # Matches <h2 data-e2e="user-bio"> ... </h2>
    m = re.search(r'<h2[^>]*data-e2e="user-bio"[^>]*>(.*?)</h2>', html, flags=re.S|re.I)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""

def extract_followers(html: str) -> str:
    # Matches <strong data-e2e="followers-count">1.2M</strong>
    m = re.search(r'<strong[^>]*data-e2e="followers-count"[^>]*>(.*?)</strong>', html, flags=re.S|re.I)
    return m.group(1).strip() if m else ""

def extract_likes(html: str) -> str:
    # Matches <strong data-e2e="likes-count">34.5M</strong>
    m = re.search(r'<strong[^>]*data-e2e="likes-count"[^>]*>(.*?)</strong>', html, flags=re.S|re.I)
    return m.group(1).strip() if m else ""

def extract_avatar(html: str) -> str:
    # Matches <div data-e2e="user-avatar"><img src="..." ...></div>
    m = re.search(r'data-e2e="user-avatar"[^>]*>.*?<img[^>]*src="([^"]+)"', html, flags=re.S|re.I)
    return m.group(1) if m else ""

# --------------------------
# Crawl4AI configs
# --------------------------
def make_browser_config() -> BrowserConfig:
    if PROXY_SERVER:
        return BrowserConfig(
            headless=HEADLESS,
            # stealth=True,          # enable if needed
            # undetected=True,       # enable if needed
            # proxy=PROXY_SERVER
            # user_data_dir=USER_DATA_DIR or None,
            # user_agent="...",      # set a stable UA if desired
            # viewport={"width": 1366, "height": 768},
        )

def make_hashtag_run_config() -> CrawlerRunConfig:
    proxies = ProxyConfig.from_env()
    if not proxies:
        print("No proxies found in environment. Set PROXIES env variable!")
        return
    proxy_strategy = RoundRobinProxyStrategy(proxies)
    # Scroll & gently click "more" buttons; wait for video anchors to appear.
    return CrawlerRunConfig(
        js_code="""
            async () => {
              const delay = (ms) => new Promise(r => setTimeout(r, ms));
              // Try a few "load more" clicks if present
              const tryClickers = () => {
                const btns = [...document.querySelectorAll('button, a')];
                for (const b of btns) {
                  const t = (b.textContent||'').toLowerCase();
                  if (/more|load|show more/.test(t)) b.click();
                }
              };
              for (let i=0;i<6;i++){
                window.scrollBy(0, 1200);
                tryClickers();
                await delay(800 + Math.random()*400);
              }
            }
        """,
        wait_for="css:a[href*='/video/']",
        # timeout_sec=45,
        remove_overlay_elements=True,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2, 
            include_external=False
        ),
        verbose=True,
        cache_mode=CacheMode.BYPASS,
        proxy_rotation_strategy=proxy_strategy
    )

def make_profile_run_config() -> CrawlerRunConfig:
    proxies = ProxyConfig.from_env()
    if not proxies:
        print("No proxies found in environment. Set PROXIES env variable!")
        return
    proxy_strategy = RoundRobinProxyStrategy(proxies)
    return CrawlerRunConfig(
        # js_code="""
        #     async () => {
        #       const delay = (ms) => new Promise(r => setTimeout(r, ms));
        #       // Nudge the viewport to ensure dynamic sections render
        #       for (let i=0;i<3;i++){
        #         window.scrollBy(0, 800);
        #         await delay(400 + Math.random()*300);
        #       }
        #     }
        # """,
        wait_for="css:h2[data-e2e='user-bio'], css:strong[data-e2e='followers-count']",
        # timeout_sec=45,
        remove_overlay_elements=True,
        verbose=True,
        cache_mode=CacheMode.BYPASS,
        proxy_rotation_strategy=proxy_strategy
    )

# --------------------------
# Phase 1: collect profile URLs
# --------------------------
async def collect_profiles(crawler: AsyncWebCrawler, hashtag: str, target: int, country: str, seen: Set[str]) -> List[Dict]:
    url = f"https://www.tiktok.com/tag/{hashtag}"
    run_cfg = make_hashtag_run_config()
    print(f"[Collect] Hashtag: #{hashtag} -> {url}")

    res = await crawler.arun(url=url, config=run_cfg)
    if not res or (res.error is not None):
        print(f"[Collect] Error for #{hashtag}: {res.error if res else 'Unknown error'}")
        return []

    # res.links is typically a list of objects with href attributes
    links = res.links or []
    new_profiles = []
    for L in links:
        href = getattr(L, "href", None) or (isinstance(L, dict) and L.get("href"))
        if not href:
            continue
        if "/video/" in href:
            prof = base_profile_from_video_link(href)
            if pick_unique_profile(prof, seen):
                new_profiles.append({"profile_link": prof, "country": country})
                print(f"[Collect] + {prof} ({len(seen)}/{target})")
                if len(seen) >= target:
                    break
    await asyncio.sleep(human_delay(*SCROLL_PAUSE))
    return new_profiles

# --------------------------
# Phase 2: visit profiles & extract fields
# --------------------------
async def scrape_profiles(crawler: AsyncWebCrawler, profiles: List[Dict], base_hashtag: str, existing_usernames: Set[str]) -> List[Dict]:
    run_cfg = make_profile_run_config()
    out_rows = []

    # Batch in chunks for nicer pacing
    CHUNK = 10
    for i in range(0, len(profiles), CHUNK):
        batch = profiles[i:i+CHUNK]
        urls = [p["profile_link"] for p in batch]
        results = await crawler.arun_many(urls=urls, config=run_cfg)

        for res, row in zip(results, batch):
            url = row["profile_link"]
            country = row["country"]
            if not res or res.error:
                print(f"[Profile] Error: {url} -> {res.error if res else 'Unknown error'}")
                continue

            html = res.html or res.markdown or ""
            username = extract_username_from_url(url)
            if not username:
                continue
            if username in existing_usernames:
                print(f"[Skip] {username} already in Airtable")
                continue

            try:
                bio = extract_bio(html)
                followers_raw = extract_followers(html)
                likes_raw = extract_likes(html)
                image_url = extract_avatar(html)

                profile_obj = Profile(
                    Username=username,
                    Bio=bio,
                    Followers=parse_count(followers_raw or ""),
                    Likes=parse_count(likes_raw or ""),
                    Profile_URL=url,
                    Image_URL=image_url or "",
                    Country=country.upper(),
                    Hashtag=base_hashtag.lower(),
                )
                save_profile_to_airtable(profile_obj.dict())
                out_rows.append(profile_obj.dict())
                print(f"[Saved] @{username} — followers={profile_obj.Followers}, likes={profile_obj.Likes}")

            except Exception as e:
                print(f"[Profile] Extraction error for {url}: {e}")

        # Human-like delay between batches
        await asyncio.sleep(human_delay(*SCROLL_PAUSE))

    return out_rows

# --------------------------
# Orchestrator
# --------------------------
async def scrape_tiktok_profiles(base_hashtag: str = BASE_HASHTAG, num_profiles: int = NUM_PROFILES):
    browser_cfg = make_browser_config()
    existing_usernames = set(get_existing_usernames())
    all_profiles: List[Dict] = []
    seen_urls: Set[str] = set()
    hashtag_country_pairs = generate_country_hashtags(base_hashtag)
    print("\n📥 Collecting profile URLs...")
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        for hashtag, country in hashtag_country_pairs:
            if len(seen_urls) >= num_profiles:
                break
            try:
                newly_found = await collect_profiles(
                    crawler=crawler,
                    hashtag=hashtag,
                    target=num_profiles,
                    country=country,
                    seen=seen_urls
                )
                all_profiles.extend(newly_found)
            except Exception as e:
                print(f"[Collect] Error #{hashtag}: {e}")
            await asyncio.sleep(human_delay(*SCROLL_PAUSE))

        print(f"\n✅ Finished collecting {len(all_profiles)} unique profiles.\n")

        print("🔎 Scraping profile pages...")
        scraped = await scrape_profiles(
            crawler=crawler,
            profiles=all_profiles,
            base_hashtag=base_hashtag,
            existing_usernames=existing_usernames
        )
        print(f"\n🎉 Done. Scraped {len(scraped)} profiles (after dedupe).")

# --------------------------
# Entrypoint
# --------------------------
if __name__ == "__main__":
    try:
        asyncio.run(scrape_tiktok_profiles())
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
