from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse


# Create your views here.

def home_page(request):
    return render(request, 'github/home.html')


def get_the_exchange_code(request):
    return redirect('https://github.com/login/oauth/authorize?client_id=89f6bf27704fa92ade50&scope=repo%3Astatus')


def get_the_access_token(request):
    exchange_code = request.GET.get('code')
    params_allow = {
        "client_id": "89f6bf27704fa92ade50",
        "client_secret": "b6cdd9dcde9d38a16b312f9b3361b77880c7867c",
        "code": f"{exchange_code}"

    }

    r = requests.post('https://github.com/login/oauth/access_token', params=params_allow,
                      headers={"Accept": "application/json"}).json()

    access_token = r['access_token']

    request.session['access_token'] = access_token

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    r_access = requests.get('https://api.github.com/user', headers=headers).json()

    return redirect('github/repository')


def access_private_repo(request):
    access_token = request.session.get('access_token')
    repos_url = 'https://api.github.com/user/repos'
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    r = requests.get(repos_url, headers=header, data={"visibility": "private"}).json()
    repo_name = [repo['name'] for repo in r]
    context = {
        'repo_name': repo_name
    }
    return render(request, 'github/show_repo.html', context)
