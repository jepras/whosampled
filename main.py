import cloudscraper
from bs4 import BeautifulSoup

def main():
    url = "https://www.whosampled.com/Naughty-by-Nature/Hip-Hop-Hooray/"
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())

    # Find the section header for "Contains samples of"
    header = soup.find("h3", string=lambda s: s and "Contains samples of" in s)
    if header:
        print(header.text.strip())
        # The table is in the next table after this header
        table = header.find_next("table")
        if table:
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) >= 5:
                    song = cells[1].find("a", class_="trackName")
                    artist = cells[2].find("a")
                    year = cells[3].get_text(strip=True)
                    genre = cells[4].find("span", class_="tdata__badge")
                    print("Song:", song.get_text(strip=True) if song else "N/A")
                    print("Artist:", artist.get_text(strip=True) if artist else "N/A")
                    print("Year:", year)
                    print("Genre/Type:", genre.get_text(strip=True) if genre else "N/A")
                    print("-" * 20)
        else:
            print("No table found after the header.")
    else:
        print("No 'Contains samples of' section found.")

if __name__ == "__main__":
    main() 