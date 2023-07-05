from django.shortcuts import render, redirect
import requests
from django.urls import reverse
from .serializer import RepositoryInfoSerializer
from dotenv import load_dotenv, find_dotenv
import os


# request.session.get will set the default value = None is key doesn't exist.
def home_page(request):
    authenticated_url = 'https://github.com/login/oauth/authorize?client_id=89f6bf27704fa92ade50&scope=repo%20user3Astatus'
    if request.session.get('access_token') is None:
        context = {
            "destination": authenticated_url
        }
        return render(request, 'github/home.html', context=context)
    else:
        context = {
            "destination": reverse('oauth_flow.github:repo')
        }
        return render(request, 'github/home.html', context=context)


def access_token_require(request):
    load_dotenv(find_dotenv())
    client_secret = os.environ['client_secret']
    exchange_code = request.GET.get('code')
    params = {
        "client_id": "89f6bf27704fa92ade50",
        "client_secret": client_secret,
        "code": exchange_code
    }

    access_token_response = requests.post('https://github.com/login/oauth/access_token', params=params,
                                          headers={"Accept": "application/json"}).json()

    access_token = access_token_response['access_token']
    request.session['access_token'] = access_token

    return redirect(reverse('oauth_flow.github:repo'))


def repo_page(request):
    access_token = request.session.get('access_token')
    repos_url = 'https://api.github.com/user/repos'
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    repo_info_response = requests.get(repos_url, headers=header)
    if repo_info_response.status_code == 401:
        return redirect(
            'https://github.com/login/oauth/authorize?client_id=89f6bf27704fa92ade50&scope=repo%20user3Astatus')
    else:
        repo_info_response = repo_info_response.json()
        serializer = RepositoryInfoSerializer(data=repo_info_response, many=True)
        serializer.is_valid(raise_exception=True)
        all_repo_info = serializer.save()

        context = {
            "all_repo_info": all_repo_info
        }
        return render(request, 'github/show_repo.html', context)
