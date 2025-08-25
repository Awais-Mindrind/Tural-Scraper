import os
from pyairtable import Api
from dotenv import load_dotenv
load_dotenv()

# Airtable config
AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
BASE_ID = "appdKQ8h63VIsBEAj"  # Replace with your base ID
TABLE_NAME = "tiktok"

api = Api(AIRTABLE_PAT)
table = api.table(BASE_ID, TABLE_NAME)
print("Connected to Airtable Table:", table.name)


def save_profile_to_airtable(profile_data: dict):
    """
    Save a scraped profile to Airtable.
    
    profile_data: {
        "Name": str,
        "Username": str,
        "Followers": int,
        "Profile URL": str,
        ...
    }
    """
    try:
        record = table.create(profile_data)
        print(f"✅ Saved to Airtable: {profile_data['Username']}")
        return record
    except Exception as e:
        print(f"❌ Error saving to Airtable: {e}")
        return None
    
def get_existing_usernames():
    """
    Fetch all usernames from the Airtable table.
    Returns a Python list of usernames.
    """
    # Fetch all records
    records = table.all()    
    # Extract Username field values
    usernames = []
    for record in records:
        username = record["fields"].get("Username")
        if username:  # avoid None values
            usernames.append(username)   
    return usernames

if __name__ == "__main__":
    from schemas import Profile
    # Example profile data
    profile = Profile(
    Username="John Doe",
    Bio="@johndoe",
    Followers=48700,
    Likes=9818,
    Profile_URL="https://www.tiktok.com/@johndoe",
    Image_URL="https://example.com/image.jpg",
    Hashtag=", ".join(["travel", "funnyvideos"]),   # Multiple hashtags
    Blacklist=False,
    Source="Tiktok",
    Country="USA"
)
    save_profile_to_airtable(profile.dict())
