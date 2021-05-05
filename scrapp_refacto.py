import pandas as pd
import requests
from bs4 import BeautifulSoup


page1 = requests.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating")
page2 = requests.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt")
page3 = requests.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=101&ref_=adv_nxt")
page4 = requests.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=151&ref_=adv_nxt")
page5 = requests.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=201&ref_=adv_nxt")
pages = [page1, page2, page3, page4, page5]

headers = ['Titre', 'Année', 'Score', 'Réalisateur', 'Votes', 'Recette']
movies = pd.DataFrame(columns=headers)


def add_title():
    title = film.h3.a.text
    row.append(title)


def add_year():
    year = film.h3.find("span", {"class": "lister-item-year text-muted unbold"}).text.strip('I ()')
    row.append(year)


def add_rate():
    rate = film.find("div", {"class": "ratings-imdb-rating"}).strong.text
    row.append(rate)


def add_director():
    director = film.find_all('p')[2].a.text
    row.append(director)


def add_vote_and_recette():
    for i in range(5):
        if i % 5 == 1:
            vote = film.find("p", {"class": "sort-num_votes-visible"}).find_all("span")[1]["data-value"]
            row.append(vote)
        elif i % 5 == 4:
            if len(film.find("p", {"class": "sort-num_votes-visible"}).find_all("span")) < 4:
                row.append("0")
            else:
                gross = film.find("p", {"class": "sort-num_votes-visible"}).find_all("span")[4]["data-value"]
                row.append(gross)
        else:
            pass


def scrapp_all():
    global film, row
    for page in pages:
        soup = BeautifulSoup(page.content, 'html.parser')
        films = soup.find_all("div", {"class": "lister-item-content"})
        for film in films:
            row = []
            add_title()
            add_year()
            add_rate()
            add_director()
            add_vote_and_recette()
            length = len(movies)
            movies.loc[length] = row


scrapp_all()


#print(movies)