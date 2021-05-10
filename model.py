import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq


main_url = 'https://www.imdb.com'

# function to get page soup from html page
def get_page_soup(url):    
    # opening connection
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    #html parser
    return BeautifulSoup(page_html, "html.parser")

# functon to get new url from the html page
def get_new_url_from_page(page_soup):    
    url = page_soup.find("div", {"class":"desc"}).find("a", {"class":"lister-page-next next-page"})
    if url != None:
        url = url['href']
        url = main_url + url
    return url

headers = ['Titre', 'Année', 'Score', 'Réalisateur', 'Votes', 'Recette', 'Genre', 'Durée']
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

def add_vote_and_recette():
    for i in range(5):
        if i % 5 == 1:
            vote = film.find("p", {"class": "sort-num_votes-visible"}).find_all("span")[1]["data-value"]
            row.append(vote)
        elif i % 5 == 4:
            if len(film.find("p", {"class": "sort-num_votes-visible"}).find_all("span")) < 4:
                row.append("0")
            else:
                gross = film.find("p", {"class": "sort-num_votes-visible"}).find_all("span")[4]["data-value"].replace(',', '')
                row.append(gross)
        else:
            pass

def add_directors():
    directors = film.find("p", {"class":""}).text.strip().split(':\n')[1].replace(', ', '').split('\n')[:-2]
    row.append(directors)

def add_genre():
    genre = film.find("span", {"class":"genre"}).text.strip(" ").strip('\n').split(', ')
    row.append(genre)

def add_duree():
    durée = film.find("span", {"class":"runtime"}).text.strip(' min')
    row.append(durée)

def scrapp_all():
    global film, row
    url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&ref_=adv_prv'
    films = []
    while url is not None:
        page = get_page_soup(url)
        url = get_new_url_from_page(page)
    
        films_on_page = page.findAll("div", {"class":"lister-item-content"})
        films = films + films_on_page

    for film in films:
        row = []
        add_title()
        add_year()
        add_rate()
        add_directors()
        add_vote_and_recette()
        add_genre()
        add_duree()
        length = len(movies)
        movies.loc[length] = row
    

scrapp_all()


#print(movies.head(25))
