from django.views.generic import TemplateView
from . import plots


class ProfileView(TemplateView):
    template_name = "components/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        student_id = self.request.GET.get('student_id')
        context['student_id'] = student_id
        context['quiz_avg_student'] = plots.fake_quiz_avg()
        context['quiz_attempts_student'] = plots.plot1d()
        context['quiz_time_student'] = plots.plot1d()
        #context['quiz_avg_student'] = plots.quiz_avg_student(student_id)
        #context['quiz_attempts_student'] = plots.quiz_attempts_student(student_id)
        #context['quiz_time_student'] = plots.quiz_time_student(student_id)
        context['student_id'] = self.request.GET.get('student_id')
        return context


class IndexView(TemplateView):
    template_name = "components/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard"})
        context['quiz_avg_class'] = plots.fake_quiz_avg()
        context['quiz_attempts_class'] = plots.plot1d()
        context['quiz_time_class'] = plots.plot1d()
        return context


class BlankView(TemplateView):
    template_name = "components/blank.html"

    def get_context_data(self, **kwargs):
        context = super(BlankView, self).get_context_data(**kwargs)
        context['quiz_attempts_plot'] = plots.plot1d()
        return context

class QuizAvgView(TemplateView):
    template_name = "components/quizavg.html"

    def get_context_data(self, **kwargs):
        context = super(QuizAvgView, self).get_context_data(**kwargs)
        context['plot'] = plots.fake_quiz_avg()
        return context

class StudentAvgView(TemplateView):
    template_name = "components/studentavg.html"

    def get_context_data(self, **kwargs):
        context = super(StudentAvgView, self).get_context_data(**kwargs)
        context['plot'] = plots.fake_student_avg()
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
