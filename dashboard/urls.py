from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^profile/$', views.ProfileView.as_view(), name="profile"),
    #url(r'^profile/(?P<student_id>\d+)/$', views.ProfileView.as_view(), name="profile"),

    # Visual specific pages for testing
    url(r'^quizavg/$', views.QuizAvgView.as_view(), name="quizavg"),
    url(r'^quizattempts/$', views.QuizAttemptsView.as_view(), name="quizattempts"),
    url(r'^quiztime/$', views.QuizTimeView.as_view(), name="quiztime"),


]
