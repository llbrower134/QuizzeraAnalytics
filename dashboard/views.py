from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import plots
from . import search
from . import datafetch
import random


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "components/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard"})

        quiz_data = datafetch.get_quiz_data()
        attempt_data = datafetch.get_attempt_data()

        context['quiz_avg_class'] = plots.avgscore_class_plot(attempt_data)
        context['quiz_attempts_class'] = plots.attempts_class_plot(attempt_data)
        context['quiz_time_class'] = plots.completion_time_class_plot(attempt_data)
        context['quiz_stddev_class'] = plots.stddev_class_plot(attempt_data)
        context['clusters_class'] = plots.kmeans_class_plot(attempt_data)
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "components/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        student_id = self.request.GET.get('student_id')

        quiz_data = datafetch.get_quiz_data()
        attempt_data = datafetch.get_attempt_data()

        context['student_name'] = datafetch.get_student_name(student_id)
        #context['student_name'] = "Lukas Brower"
        context['net_id'] = student_id
        #context['class_year'] = search.get_student_class(student_id)
        context['class_year'] = "2017"
        #context['major'] = search.get_student_major(student_id)
        #context['image'] =
        context['quiz_avg'] = random.randrange(70, 100)
        context['quiz_avg_student'] = plots.avgscore_student_plot(attempt_data, student_id)
        context['quiz_attempts_student'] = plots.attempts_student_plot(attempt_data, student_id)
        context['quiz_time_student'] = plots.completion_time_student_plot(attempt_data, student_id)
        context['student_id'] = self.request.GET.get('student_id')
        return context

##################### Visual Specific Pages #####################

class QuizAvgView(TemplateView):
    template_name = "components/quizavg.html"

    def get_context_data(self, **kwargs):
        context = super(QuizAvgView, self).get_context_data(**kwargs)
        context['plot'] = plots.avg_score_class()
        return context

class QuizAttemptsView(TemplateView):
    template_name = "components/quizavg.html"

    def get_context_data(self, **kwargs):
        context = super(QuizAvgView, self).get_context_data(**kwargs)
        context['plot'] = plots.attempts_class()
        return context

class QuizTimeView(TemplateView):
    template_name = "components/quizavg.html"

    def get_context_data(self, **kwargs):
        context = super(QuizAvgView, self).get_context_data(**kwargs)
        context['plot'] = plots.completion_time_class()
        return context

###############################################################
