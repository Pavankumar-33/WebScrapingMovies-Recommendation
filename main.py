import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

url = r'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'

# Set a User-Agent header to mimic a legitimate browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Introduce a delay between requests
delay = 2  # Set the delay in seconds

# Make the request using a Session object
with requests.Session() as session:
    response = session.get(url, headers=headers)
    time.sleep(delay)  # Introduce a delay before parsing the content to mimic human-like behavior

# Check if the request was successful (status code 200)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant data from the HTML
    movie_data = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    #asdfa

    movie_name = []
    year = []
    time = []
    rating = []
    metascore = []
    votes = []
    gross = []
    description = []
    Director = []
    Stars = []

    for movie in movie_data:
        # Extracting data for each movie
        name = movie.find('h3', class_='ipc-title__text').text.strip()
        year_release = movie.find('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item').text.strip()
        runtime = movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')[1].text.strip() if len(movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')) > 1 else None
        imdb_rating = movie.find('span', class_='ipc-rating-star--imdb').text.strip()
        metascore_element = movie.find('span', class_='metacritic-score-box')
        metascore_value = metascore_element.text.strip() if metascore_element else None        
        votes_element = movie.find('div', class_='sc-53c98e73-0 kRnqtn')
        votes_value = votes_element.text.strip().split()[1] if (votes_element and len(votes_element.text.strip().split()) > 1) else None
        gross_value = movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')[2].text.strip() if len(movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')) > 2 else None
        description_text = movie.find('div', class_='ipc-html-content-inner-div').text.strip()
        director = movie.find('div', class_='sc-53c98e73-2 bqBWud').text.strip() if movie.find('div', class_='sc-53c98e73-2 bqBWud') else None
        stars = [star.text.strip() for star in movie.find_all('div', class_='sc-53c98e73-2 bqBWud')[1].find_all('span')] if len(movie.find_all('div', class_='sc-53c98e73-2 bqBWud')) > 1 else None

        # Adding data to lists
        movie_name.append(name)
        year.append(year_release)
        time.append(runtime)
        rating.append(imdb_rating)
        metascore.append(metascore_value)
        votes.append(votes_value)
        gross.append(gross_value)
        description.append(description_text)
        Director.append(director)
        Stars.append(stars)

    # Create a DataFrame from the extracted data
    data = {
        'Movie': movie_name,
        'Year': year,
        'Runtime': time,
        'Rating': rating,
        'Metascore': metascore,
        'Votes': votes,
        'Gross': gross,
        'Description': description,
        'Director': Director,
        'Stars': Stars,
    }

    df = pd.DataFrame(data)

    # Save the DataFrame to a pickle file
    df.to_pickle('data.pkl')

    # Print the extracted movie data
    print(df)

else:
    print(f"Error: {response.status_code}")
