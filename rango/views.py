from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from rango.models import Page

def index(request):
    #LETS GET SOME CATEGORIES FROM THE DATABASE (ORDERED BY LIKES AND ONLY TOP 5)
    category_list = Category.objects.order_by("-likes")[:5]
    pages_list = Page.objects.order_by("-views")[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}

    return render(request, 'rango/index.html', context_dict)
def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try: #POPULATING DICT
        #look for a category name slug with the given name
        category = Category.objects.get(slug=category_name_slug)
        #find all the pages associated with that category
        pages = Page.objects.filter(category=category)
        #add all results to the template context
        context_dict['pages'] = pages
        #add the category object from database to context dict
        context_dict['category'] = category
    except Category.DoesNotExist: #SHIT NOTHINGS THERE
        #if we can't find it we don't do shit
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)
