from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages

from mainapp import forms
from mainapp.models import Disease
from mainapp import tasks as mainapp_tasks


# Create your views here.
class HomeView(ListView):
    model = Disease
    template_name = 'mainapp/home_disease_list.html'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Disease.objects.filter(deleted=False).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редкие болезни - сообщества пациентов'
        return context


class DiseaseDetaileView(DetailView):
    model = Disease
    template_name = 'mainapp/disease_detaile.html'

    def get_queryset(self):
        return Disease.objects.filter(deleted=False, slug=self.kwargs['slug'])


class DiseaseByTag(ListView):
    template_name = 'mainapp/home_disease_list.html'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Disease.objects.filter(deleted=False, tags__slug=self.kwargs['slug'])


class Search(ListView):
    template_name = 'mainapp/search.html'
    paginate_by = 4

    def get_queryset(self):
        return Disease.objects.filter(Q(deleted=False) & Q(title__icontains=self.request.GET.get('s')) | Q(
            search__icontains=self.request.GET.get('s')) | Q(codemkb__icontains=self.request.GET.get('s')) | Q(
            tags__title__icontains=self.request.GET.get('s'))).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('s')
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        context["form"] = forms.MailFeedbackForm()
        return context

    def post(self, *args, **kwargs):
        form = forms.MailFeedbackForm(self.request.POST)
        if form.is_valid():
            human = True
            mainapp_tasks.send_feedback_mail.delay({"message": f'Subject: {self.request.POST.get("title")}\n Messages: {self.request.POST.get("message")}', })
            messages.success(self.request, 'Письмо отправлено!')
        else:
            messages.error(self.request, 'Ошибка валидации')
            return render(self.request, self.template_name, {"form": form})
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))

