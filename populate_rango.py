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
         "url": "http://docs.python.org/2/tutorial/",
         "views": 40},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greemteapress.com/thinkpython/",
         "views": 200},
        {"title":"Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 856}
    ]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views":9800},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": 20}
    ]
    other_pages = [
        {"title": "Bottle",
        "url":"http://bottlepy.org/docs/dev/",
         "views": 201},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": 10}
    ]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}}

    """OK SO now we go through the cats dictionary, and add literally everything"""

    for cat, cat_data in cats.iteritems():
        c = add_cat(cat, cat_data["views"], cat_data["likes"]) #adds a cat to a database
        for p in cat_data["pages"]: #then loops through and adds a page under each category
            add_page(c, p["title"], p["url"], p["views"])
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

def add_cat(name, views=0, likes=0):
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