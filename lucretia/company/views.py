from django.shortcuts import render
from .models import Company

app_name = 'blog'


# Create your views here.
def company(request):
    posts = Company.objects.all()
    return render(request, 'company/post/list.html', {'posts': posts})


def set_companys(requests):
    pass
