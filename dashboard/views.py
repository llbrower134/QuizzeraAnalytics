from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import plots
from . import datafetch
import random


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "components/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard"})

        attempt_data = datafetch.get_attempt_data()
        quiz_titles = datafetch.get_quiz_titles()

        context['quiz_avg_class'] = plots.avgscore_class_plot(attempt_data, quiz_titles)
        context['quiz_attempts_class'] = plots.attempts_class_plot(attempt_data, quiz_titles)
        context['quiz_time_class'] = plots.completion_time_class_plot(attempt_data, quiz_titles)
        context['quiz_stddev_class'] = plots.stddev_class_plot(attempt_data, quiz_titles)
        context['clusters_class'] = plots.kmeans_class_plot(attempt_data)
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "components/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        student_id = self.request.GET.get('student_id')

        quiz_titles = datafetch.get_quiz_titles()
        attempt_data = datafetch.get_attempt_data()

        titles_list = list(datafetch.get_quiz_titles().values())
        titles_list.sort()

        student_name = datafetch.get_student_name(student_id)
        context['student_id'] = student_id

        if student_name != "":
            context['quiz_list'] = titles_list
            context['student_id'] = student_id
            context['student_name'] = datafetch.get_student_name(student_id)
            context['quiz_avg_student'] = plots.avgscore_student_plot(attempt_data, quiz_titles, student_id)
            context['quiz_attempts_student'] = plots.attempts_student_plot(attempt_data, quiz_titles, student_id)
            context['quiz_time_student'] = plots.completion_time_student_plot(attempt_data, quiz_titles, student_id)
            context['student_id'] = self.request.GET.get('student_id')
        return context

class QuizView(LoginRequiredMixin, TemplateView):
    template_name = "components/quiz.html"

    def get_context_data(self, **kwargs):
        context = super(QuizView, self).get_context_data(**kwargs)
        attempt_data = datafetch.get_attempt_data()

        titles_list = list(datafetch.get_quiz_titles().values())
        titles_list.sort()
        context['quiz_list'] = titles_list

        # Quiz to be displayed
        quiz_title = self.request.GET.get('quiz_title')
        context['quiz_title'] = quiz_title

        if quiz_title != "" and quiz_title != None:
            quiz_id = datafetch.quiz_title_to_id(quiz_title, datafetch.get_quiz_titles())
            context['question_avg_class'] = plots.question_avgscore_class_plot(attempt_data, quiz_id)
            context['question_attempts_class'] = plots.question_attempts_class_plot(attempt_data, quiz_id)
            context['question_completion_time_class'] = plots.question_completion_time_class_plot(attempt_data, quiz_id)
            context['question_stddev_class'] = plots.question_stddev_class_plot(attempt_data, quiz_id)

        return context

class ProfileQuizView(LoginRequiredMixin, TemplateView):
    template_name = "components/profile-quiz.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileQuizView, self).get_context_data(**kwargs)
        attempt_data = datafetch.get_attempt_data()
        quiz_titles = list(datafetch.get_quiz_titles().values())
        quiz_titles.sort()
        context['quiz_list'] = quiz_titles

        # Quiz to be displayed
        profid_title = self.request.GET.get('quiz_title').split("-")
        student_id = profid_title[0]
        quiz_title = profid_title[1]
        context['student_id'] = student_id
        context['student_name'] = datafetch.get_student_name(student_id)
        context['quiz_title'] = quiz_title

        if quiz_title != "" and quiz_title != None:
            quiz_id = datafetch.quiz_title_to_id(quiz_title, datafetch.get_quiz_titles())
            context['question_avg_student'] = plots.question_avgscore_student(attempt_data, quiz_id, student_id)
            context['question_attempts_student'] = plots.question_attempts_student(attempt_data, quiz_id, student_id)
            context['question_completion_time_student'] = plots.question_completion_time_student(attempt_data, quiz_id, student_id)

        return context