import datetime
import json
import random

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View


def load_news_json():
    with open(settings.NEWS_JSON_PATH) as news_json:
        return json.load(news_json)


test_json = [
    {
        "created": "2020-02-02 16:40:00",
        "text": "A new star appeared in the sky.",
        "title": "The birth of the star",
        "link": 9234732
    },
    {
        "created": "2020-02-02 16:39:59",
        "text": "A new star appeared in the sky.",
        "title": "The raise of Jupyter",
        "link": 2389742
    },
]


# Create your views here.
class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        entry = [{
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": str(request.POST.get('text')),
            "title": str(request.POST.get('title')),
            "link": random.randint(1000, 2000)
        }]

        dump_json = load_news_json() + entry

        with open(settings.NEWS_JSON_PATH, 'w') as json_file_2:
            json.dump(dump_json, json_file_2, indent=4)

        return redirect('/news/')


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


class NewsBaseView(View):
    def get(self, request, *args, **kwargs):
        
        
        query = str(request.GET.get('q'))
        news = load_news_json()
        news_list = []
        for news_articles in news:
            if query in news_articles['title'] and query != "":
                news_list.append(news_articles['link'])

        if news_list == []:
            return render(request, 'news/index.html', context={"news_json": load_news_json()})

        else:
            new_news = []
            for x in news_list:
                for news_ in news:
                    if x in news_.values():
                        new_news.append(news_)

            return render(request, 'news/index.html', context={"news_json": new_news})



        


class NewsView(View):
    def get(self, request, link, *args, **kwargs):

        news_json = load_news_json()

        news_feed = {}
        for news in news_json:
            if news["link"] == int(link):
                news_feed = news

        for test in test_json:
            if test["link"] == int(link):
                news_feed = test

        return render(request, 'news/news_piece.html', context = news_feed)