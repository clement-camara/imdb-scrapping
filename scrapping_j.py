from bs4 import BeautifulSoup
import requests

uri = ["https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=101&ref_=adv_nxt",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=151&ref_=adv_nxt",
      "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=201&ref_=adv_nxt"]

top_250 = {"title": [], "date" : [], "note" : [], "director" : [], "vote" : [], "recette" : []}
for url in uri:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all('h3', class_="lister-item-header")
    for res in result:
        title_film = res.find('a').text
        date_sortie = res.find('span', class_="lister-item-year text-muted unbold").text.strip('I) ()')
        top_250["title"].append(title_film)
        top_250["date"].append(date_sortie)

    result_note = soup.find_all('div', class_="inline-block ratings-imdb-rating")
    for res in result_note:
        note = res.find('strong').text
        top_250["note"].append(note)

    result_director = soup.find_all('p', class_="")
    for res in result_director:
        director = res.find('a').text
        top_250["director"].append(director)

    result_vote_recette = soup.find_all('p', class_="sort-num_votes-visible")
    for res in result_vote_recette:
        vote_recette = res.find_all('span')
        if len(vote_recette) > 4:
            vote = vote_recette[1]['data-value']
            recette = vote_recette[4]['data-value']
        else:
            vote = vote_recette[1]['data-value']
            recette = None
        top_250["vote"].append(vote)
        top_250["recette"].append(recette)

print(top_250)
