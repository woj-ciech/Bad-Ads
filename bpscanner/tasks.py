import celery
import feedparser
from celery import shared_task
from bpscanner_app.models import *
from celery.exceptions import Ignore
from bs4 import BeautifulSoup
import requests
import wget
import imagehash
from PIL import Image

from celery_progress.backend import ProgressRecorder
app = celery.Celery('bpscanner', broker="redis://localhost:6379")

headers = {
    "Cookie": "visid_incap_1675433=VZrtTZ/UQY2QlReiMAi5P/Wl+F4AAAAAQUIPAAAAAADPnhf2LuncG6r3cyWPC7xt; _ga=GA1.2.1530690978.1593354655; __tawkuuid=e::bedpage.com::hc4vVnVei07+YeekIHqUClDNk5KWT5jqwRPJhcp4emWfe1rK+jrXHN6AMSLWTPW9::2; incap_ses_878_1675433=ZYniLnwWLwvyWrFuaUgvDN24KV8AAAAA5QS64Ahxv4xBwmU9tYxVuQ==; _gid=GA1.2.330329676.1596566030; ci_session=5feit0s88bqba5q315nhjmqaj4iero81; incap_ses_305_1675433=sGHhUpDF5TmQ/bI6DJQ7BJy7KV8AAAAAgpzO9jy6z67InkVEUDBLkA==","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

bad_words = ['young','petite','lolita','gfe','hardcore','schoolgirl','hotel','road','ave','street',"amber","alert", "cops","police"]

@shared_task(bind=True,ignore_result=True)
def search_city_task(self, fk=None, city=None):
    results1 = []
    search = Search.objects.get(id=fk)
    print(city)
    bad = False
    current_ad = {}
    try:
        d = feedparser.parse("https://" + city + ".bedpage.com/Escorts/Rss.xml")
        for c, i in enumerate(d.entries):

            if Ad.objects.filter(link=i.link).exists():
                pass
            else:
                current_ad = {"title": i.title, "timestamp": i.published, "description": i.summary,
                              "link": i.link}
                results1.append(current_ad)
                for j in bad_words:
                    if j.lower() in i.title.lower() or j.lower() in i.summary.lower():
                        bad = True
                        break
                    else:
                        bad = False

            ad = Ad(search=search, title=i.title, timestamp=i.published, link=i.link,
                    desc=i.summary, bad=bad)
            ad.save()

        self.update_state(state="SUCCESS",
                          meta={"total": 51, 'current': 51, 'result': results1})
    except Exception as e:
        print(e)

@shared_task(bind=True)
def check_person_task(self,fk=None,link=""):
    progress_recorder = ProgressRecorder(self)

    ad = Ad.objects.get(id=fk)

    req = requests.get(link, headers=headers)

    bs = BeautifulSoup(req.content, features="html.parser")

    age = ""
    email = ""
    mobile = ""
    location = ""
    try:
        for i in bs.find_all('div',{"style":"padding-left:2em;"}):
            text = i.contents[0].split(":")[0].split(" ")
            for j in text:
                if j == "age":
                    age = i.contents[0].split(":")[1]
                if j == "Email":
                    email = i.contents[0].split(":")[1]
                if j == "Mobile":
                    mobile = i.contents[0].split(":")[1]
                if j == "Location":
                    location = i.contents[0].split(":")[1]
    except Exception as e:
        print(e)

    person = Person(ad=ad, email=email, age=age, phone=mobile, location=location)
    person.save()


@shared_task(bind=True)
def check_photo_task(self,fk, link=""):
    progress_recorder = ProgressRecorder(self)
    hashes = []
    print(fk)

    req = requests.get(link, headers=headers)

    bs = BeautifulSoup(req.content, features="html.parser")
    print(req)
    for i in bs.find_all("ul", {"id": "viewAdPhotoLayout"}):
        for j in i.contents:
            try:
                local = wget.download(j.contents[1].attrs['src'])

                print(local)
                hash = imagehash.average_hash(Image.open(local))
                hashes.append(str(hash))
                print(hash)
                # print(j.contents[1].attrs['src'])
            except:
                pass

    imag = Images(images=hashes)
    imag.save()
    Person.objects.filter(id=fk).update(images=imag)




