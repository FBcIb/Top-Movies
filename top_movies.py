# Collect top x movies from a given span of years - by imdb rating - prefer sorted by rotten tomatoes score (preferrably an avg of audience and critic scores)
# Raw url - https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short&release_date=-01-01,-12-31&num_votes=70000,&sort=user_rating,desc,&countries=us

from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
from random import randint
from sys import stdout

d1, d2 = input('Enter a span of years (e,g, 2000 2015): ').split(' ')
n = int(input('How many movies per year? '))
years = [str(i) for i in range(int(d1), int(d2) + 1)]
movies = []
start = time()

for year in years:
    url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short&release_date=' +year+ '-01-01,' +year+ '-12-31&num_votes=70000,&sort=user_rating,desc,&countries=us'
    res = get(url)
    html = BeautifulSoup(res.text, 'html.parser')
    movie_container = html.find_all('div', class_ = 'lister-item mode-advanced')
    
    # Track program runtime and progress in terminal - also slows program to avoid flooding
    cur_time = time() - start
    output = ('Year: {} - Time elapsed: {}mins or {}sec(s)'.format(year, round(cur_time/60, 2), round(cur_time, 2)))
    stdout.write('\r' * 50 + output)
    sleep(randint(1,3))

    # Parse through movies and save desired variables
    for container in movie_container[0: n]:
        title = container.h3.a.text
        url = 'https://www.imdb.com'+ container.h3.a['href']
        rating = float(container.strong.text)
        genre = container.find('span', class_ = 'genre').text.replace('\n', '').rstrip()
        combo = [rating, title, genre, year, url]
        movies.append(combo)

# Formatting the print of our data
print('\n')
movies.sort(reverse = True)
c = 1
for i in movies:
    print('{}: "{}" || Score: {} || Genre: {} || Year: {} || IMDB link: {}'.format(c, i[1], i[0], i[2], i[3], i[4]))
    print('\n')
    c += 1

# can sort list of lists by placing score in 1st index - for multiyear parsing