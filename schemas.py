from typing import Optional, List
from pydantic import BaseModel, Field


# MODELS
# ------------------------------
class ProfileFilters(BaseModel):
    hashtag: Optional[str] = None
    country: Optional[str] = None
    min_followers: Optional[int] = None
    min_likes: Optional[int] = None
    limit: Optional[int] 

class Profile(BaseModel):
    Username: str
    Bio: Optional[str] = None
    Followers: Optional[int] = 0
    Likes: Optional[int] = 0
    Profile_URL: Optional[str] = None
    Image_URL: Optional[str] = None
    Hashtag: str 
    Blacklist: bool = False
    Source: str = "Tiktok"
    Country: Optional[str] = None

class AIQueryRequest(BaseModel):
    query: str

class ScrapeRequest(BaseModel):
    hashtag: str
    num_profiles: Optional[int] = 1000
