from django.views.generic import TemplateView
from . import plots
from . import search
from . import datafetch
import random


class IndexView(TemplateView):
    template_name = "components/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard"})

        quiz_data = datafetch.get_quiz_data()
        attempt_data = datafetch.get_attempt_data()

        context['quiz_avg_class'] = plots.avgscore_class_plot(attempt_data)
        context['quiz_attempts_class'] = plots.attempts_class_plot(attempt_data)
        context['quiz_time_class'] = plots.completion_time_class_plot(attempt_data)
        return context

class ProfileView(TemplateView):
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

class BlankView(TemplateView):
    template_name = "components/blank.html"

    def get_context_data(self, **kwargs):
        context = super(BlankView, self).get_context_data(**kwargs)
        context['quiz_attempts_plot'] = plots.plot1d()
        return context


class ButtonsView(TemplateView):
    template_name = "components/buttons.html"

    def get_context_data(self, **kwargs):
        context = super(ButtonsView, self).get_context_data(**kwargs)
        context.update({'title': "Buttons"})
        return context


class FlotView(TemplateView):
    template_name = "components/flot.html"

    def get_context_data(self, **kwargs):
        context = super(FlotView, self).get_context_data(**kwargs)
        context.update({'title': "Flot Charts"})
        return context


class FormsView(TemplateView):
    template_name = "components/forms.html"

    def get_context_data(self, **kwargs):
        context = super(FormsView, self).get_context_data(**kwargs)
        context.update({'title': "Forms"})
        return context


class GridView(TemplateView):
    template_name = "components/grid.html"

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)
        context.update({'title': "Grid"})
        return context


class IconsView(TemplateView):
    template_name = "components/icons.html"

    def get_context_data(self, **kwargs):
        context = super(IconsView, self).get_context_data(**kwargs)
        context.update({'title': "Icons"})
        return context


class LoginView(TemplateView):
    template_name = "components/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({'title': "Log In"})
        return context


class MorrisView(TemplateView):
    template_name = "components/morris.html"

    def get_context_data(self, **kwargs):
        context = super(MorrisView, self).get_context_data(**kwargs)
        context.update({'title': "Morris Charts"})
        return context


class NotificationsView(TemplateView):
    template_name = "components/notifications.html"

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context.update({'title': "Notifications"})
        return context


class PanelsView(TemplateView):
    template_name = "components/panels-wells.html"

    def get_context_data(self, **kwargs):
        context = super(PanelsView, self).get_context_data(**kwargs)
        context.update({'title': "Panels and Wells"})
        return context


class TablesView(TemplateView):
    template_name = "components/tables.html"

    def get_context_data(self, **kwargs):
        context = super(TablesView, self).get_context_data(**kwargs)
        context.update({'title': "Tables"})
        return context


class TypographyView(TemplateView):
    template_name = "components/typography.html"

    def get_context_data(self, **kwargs):
        context = super(TypographyView, self).get_context_data(**kwargs)
        context.update({'title': "Typography"})
        return context
