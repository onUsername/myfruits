from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse("mysite2首页")
    return render(request, "fruits/index.html", {})
