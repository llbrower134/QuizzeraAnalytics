from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^profile/$', views.ProfileView.as_view(), name="profile"),
    url(r'^quiz/$', views.QuizView.as_view(), name="quiz"),
    url(r'^profquiz/$', views.ProfileQuizView.as_view(), name="profquiz"),
]
