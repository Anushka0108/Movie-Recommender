import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
headers = {"User-Agent": "Mozilla/5.0"}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

data = []

movies = soup.find_all("li", class_="ipc-metadata-list-summary-item")

for movie in movies[:10]: 
    try:
        title = movie.find("h3").get_text(strip=True)
    except:
        title = "N/A"

    try:
        metadata = movie.find_all("span", class_="cli-title-metadata-item")
        year = metadata[0].get_text(strip=True) if len(metadata) > 0 else "N/A"
        duration = metadata[1].get_text(strip=True) if len(metadata) > 1 else "N/A"
        rating = metadata[2].get_text(strip=True) if len(metadata) > 2 else "N/A"
    except:
        year, duration, rating = "N/A", "N/A", "N/A"

    try:
        link = "https://www.imdb.com" + movie.find("a")["href"].split("?")[0]
    except:
        link = "N/A"

    if link != "N/A":
        movie_page = requests.get(link, headers=headers)
        movie_soup = BeautifulSoup(movie_page.text, "html.parser")
        try:
            genre = ", ".join([g.get_text(strip=True) 
                               for g in movie_soup.find_all("span", class_="ipc-chip__text")])
        except:
            genre = "N/A"
        time.sleep(1) 
    else:
        genre = "N/A"

    data.append({
        "Title": title,
        "Year": year,
        "Duration": duration,
        "Rating": rating,
        "Genre": genre,
        "Link": link
    })

df = pd.DataFrame(data)
df.to_excel("imdb_movies.xlsx", index=False)

print("Data saved to imdb_movies.xlsx")
