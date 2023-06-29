from django.urls import path
from oauth_flow.github import views

app_name = 'oauth_flow.github'
urlpatterns = [
    path('github/home/', views.home_page, name='Home_page'),
    path('github/exchange_code/', views.get_the_exchange_code, name='exchange_code'),
    path('github/callback/', views.get_the_access_token, name='access_token'),
    path('github/callback/github/repository/', views.access_private_repo, name='repo'),
]
