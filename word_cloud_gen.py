import requests
import urllib


# my key
APP_ACCESS_TOKEN = "5683010082.f0c5981.7724a99b4e794e4a8d4976af727fe38d"
BASE_URL = "https://api.instagram.com/v1/"
search_url = 'tags/search?q=%s&access_token=%s'


def search_words_with_tags():
    req_url = BASE_URL + search_url % ("olympic", APP_ACCESS_TOKEN)
    r = requests.get(req_url).json()
    for i in range(0, len(r['data'])):
        print r['data'][i]['name']



search_words_with_tags()



#
# from os import path
# from wordcloud import WordCloud
#
# d = path.dirname(__file__)
#
# # Read the whole text.
# text = open(path.join(d, 'constitution.txt')).read()
#
# # Generate a word cloud image
# wordcloud = WordCloud().generate(text)
#
# # Display the generated image:
# # the matplotlib way:
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
#
# # lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()