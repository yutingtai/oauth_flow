from django.urls import path
from oauth_flow.github import views

app_name = 'oauth_flow.github'
urlpatterns = [
    path('github/home/', views.home_page, name='home_page'),
    path('github/callback/', views.github_oauth_callback, name='access_token'),
    path('github/repository/', views.repo_page, name='repo'),
]
