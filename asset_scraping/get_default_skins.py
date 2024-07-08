import requests
from bs4 import BeautifulSoup
import os
import shutil


# List of brawler names to search for
brawler_names = [
    "Berry",
    "Meg",
    "Frank",
    "Draco",
    "Sandy",
    "Buster",
    "Chester",
    "Lily",
    "Jacky",
    "Jessie",
    "Gale",
    "Surge",
    "Bibi",
    "Mico",
    "Crow",
    "Melodie",
    "Fang",
    "Doug",
    "Nita",
    "Chuck",
    "Leon",
    "Eve",
    "Cordelius",
    "Larry & Lawrie",
    "Colette",
    "Buzz",
    "Edgar",
    "Angelo",
    "R-T",
    "Bo",
    "Rico",
    "Kit",
    "Emz",
    "Belle",
    "Mandy",
    "Amber",
    "Tick",
    "Lou",
    "Spike",
    "Dynamike",
    "Piper",
    "Pearl",
    "Charlie",
    "Tara",
    "Gray",
    "Mortis",
    "Byron",
    "Mr. P",
    "Colt",
    "Max",
    "Maisie",
    "Brock",
    "Otis",
    "Griff",
    "Gene",
    "El Primo",
    "Squeak",
    "Nani",
    "Poco",
    "Grom",
    "Shelly",
    "Janet",
    "Sprout",
    "Ruffs",
    "8-Bit",
    "Bea",
    "Sam",
    "Stu",
    "Darryl",
    "Willow",
    "Bonnie",
    "Lola",
    "Carl",
    "Penny",
    "Ash",
    "Bull",
    "Gus",
    "Barley",
    "Rosa",
    "Hank",
    "Pam",
]

# Starting URL
base_url = "https://brawlstars.fandom.com"


# Function to get the soup object from a URL
def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


# Get the main page with the list of brawlers
main_page_url = base_url + "/wiki/Category:Brawlers"
soup = get_soup(main_page_url)

# Find all links to brawler pages
brawler_links = []
for brawler in brawler_names:
    brawler_tag = soup.find("a", title=brawler)
    if brawler_tag:
        brawler_links.append(base_url + brawler_tag["href"])


# Extract image links from each brawler page
image_links = []
for link in brawler_links:
    brawler_soup = get_soup(link)
    if brawler_soup:
        print(link)
        figures = brawler_soup.find_all("figure", class_="pi-item pi-image")
        for tag in figures:
            a_tag = tag.find("a")
            if a_tag and "href" in a_tag.attrs:
                image_links.append(a_tag["href"])

if not os.path.exists("default_skins"):
    os.makedirs("default_skins")

cleaned_image_urls = [img_url.split("/revision")[0] for img_url in image_links]
for img_url in cleaned_image_urls:
    img_name = img_url.split("/")[-1]
    file_path = os.path.join("default_skins", img_name)
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        print(f"Saved {img_name}")
    else:
        print(f"Failed to retrieve image from {img_url}")
