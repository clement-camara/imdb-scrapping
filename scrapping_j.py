from bs4 import BeautifulSoup
import requests

uri = ["https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=101&ref_=adv_nxt",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=151&ref_=adv_nxt",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=201&ref_=adv_nxt"]


def get_pages(uri:list):
    pages = []
    for url in uri:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        films = soup.find_all('div', class_="lister-item-content")
        pages.append(films)
    return pages


def get_title(pages:list, data:dict):
    for page in pages:
        for film in page:
            title_film = film.h3.a.text
            data["title"].append(title_film)


def get_date(pages:list, data:dict):
    for page in pages:
        for film in page:
            date_sortie = film.h3.find(
                'span', class_="lister-item-year text-muted unbold").text.strip('I) ()')
            data["date"].append(date_sortie)


def get_rate(pages:list, data:dict):
    for page in pages:
        for film in page:
            rate = film.find('div', class_="inline-block ratings-imdb-rating").strong.text
            data["rate"].append(rate)


def get_director(pages:list, data:dict):
    for page in pages:
        for film in page:
            director = film.find('p', class_="").a.text
            data["director"].append(director)


def get_vote_and_recette(pages:list, data:dict):
    for page in pages:
        for film in page:
            result_vote_recette = film.find_all('p', class_="sort-num_votes-visible")
            for res in result_vote_recette:
                vote_recette = res.find_all('span')
                if len(vote_recette) > 4:
                    vote = vote_recette[1]['data-value']
                    recette = vote_recette[4]['data-value']
                else:
                    vote = vote_recette[1]['data-value']
                    recette = None
                data["vote"].append(vote)
                data["recette"].append(recette)


def scrapp_all(uri:list):
    top_250 = {"title": [], "date": [], "rate": [],
              "director": [], "vote": [], "recette": []}
    pages = get_pages(uri)
    get_title(pages, top_250)
    get_date(pages, top_250)
    get_rate(pages, top_250)
    get_director(pages, top_250)
    get_vote_and_recette(pages, top_250)
    return top_250

print(scrapp_all(uri))

