from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from datetime import datetime

def index(request):
    request.session.set_test_cookie()
    #LETS GET SOME CATEGORIES FROM THE DATABASE (ORDERED BY LIKES AND ONLY TOP 5)
    category_list = Category.objects.order_by("-likes")[:5]
    pages_list = Page.objects.order_by("-views")[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}



    visitor_cookie_handler(request)

    context_dict['visits'] = request.session['visits']
    context_dict['last_visit'] = request.session['last_visit']
    response = render(request, 'rango/index.html', context_dict)

    return response

def about(request):

    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    print (request.method)
    visitor_cookie_handler(request)
    print(request.user)


    visits = request.session['visits']
    return render(request, 'rango/about.html', {'visits': visits})

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
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, "rango/add_category.html", {"form": form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, "rango/add_page.html", context_dict)

def register(request):
    #A boolean value which tells the template whether registration was successful
    registered = False;

    if request.method == 'POST': #well if its a HTTP POST we want that form data


        #getting that sick form data into delicious info pumped directly into our veins
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() #save form data to database

            #and hash their password and save that
            user.set_password(user.password)
            user.save()

            #~~~DEALING WITH USER PROFILES~~~

            #commit=false so we can avoid integrity problems until we're ready
            profile = profile_form.save(commit=false)
            profile = user

            #if theres a picture, go find it
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            #save them profiles
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        #IF NOT A POST, SHOVE BLANK CLASSES IN HERE
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    #If request is a HTTP POST, get info
    if request.method == 'POST':
        #get username
        #get password
        #we use get as this gives us a None value if it fails
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use django to see if username/password is valid
        user = authenticate(username = username, password=password)
        #if we don't have a user object, we didn't find a user
        if user:
            #ACCOUNT MIGHT BE DISABLED :((
            if user.is_active:

                #but if it exists and is active its fine log in
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HTTPResponse("Your Rango account is disabled.")
        else: #BAD LOGIN DETAILS
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else: #NO HTTP POST

        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    #take user back to homepage
    return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    #Get the number of visits to the site
    #If we can find the visits cookie we turn it into an int
    #else return 1

    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    #if more than day since last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update last visit cookie
        last_visit_cookie = str(datetime.now())
    #update visits cookie
    request.session['visits'] = visits
    request.session['last_visit'] = last_visit_cookie

