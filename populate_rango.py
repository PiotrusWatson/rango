import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tango.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    """ Create lists of dicts with each page we want in each category
        Then a dict of dicts for each category
        THE ENDS JUSTIFY THE MEANS"""
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greemteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"}
    ]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/"}
    ]
    other_pages = [
        {"title": "Bottle",
        "url":"http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"}
    ]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}}

    """OK SO now we go through the cats dictionary, and add literally everything"""

    for cat, cat_data in cats.iteritems():
        c = add_cat(cat, cat_data["views"], cat_data["likes"]) #adds a cat to a database
        for p in cat_data["pages"]: #then loops through and adds a page under each category
            add_page(c, p["title"], p["url"])
    #PRINTING
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    """This adds a page to the database, using the page model, sets its attributes and then saves it"""
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    """see: add_page but with categories :)"""
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

#IT BEGINS
if __name__=="__main__": #If run as usual
    print("STARTING RANGO POPULATION SCRIPT...")
    populate()