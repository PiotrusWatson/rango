from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    #
    context_dict = {'boldmessage': "HOT DAMN I LOVE VIDEO GAMES"}

    return render(request, 'rango/index.html', context=context_dict)
def about(request):
    return HttpResponse("WELCOME TO THE ABOUT PAGE :) TODAY I WOULD LIKE TO DISCUSS SPROTS. WHAT IS YOUR FAVOURITE SPROT?"
                        "\n MINES FENCE. I AM BIG FAN OF FENCE. IT IS IN THE STABBING WHERE THE ENJOYMENT IS.")