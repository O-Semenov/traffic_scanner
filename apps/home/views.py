from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .forms import ScanForm
from django.shortcuts import render
from django_tables2 import SingleTableView
from django.views.generic import ListView
from .models import Scan
from .tables import ScanTable
from pprint import pprint


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def scaning(request):
    if request.method == 'POST':
        form = ScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.user = request.user
            scan.save()
            return HttpResponseRedirect("/tables")
    else:
        form = ScanForm
    return render(request, 'home/scaning.html', {'form': form, 'segment': 'scaning'})


class ScanListView(SingleTableView):
    table_class = ScanTable
    template_name = 'home/tables.html'

    def get(self, request):
        self.queryset = Scan.objects.filter(user=request.user)
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'tables'
        return context


def deleteItem(request, scanId):
    Scan.objects.filter(id=scanId).delete()

    return HttpResponseRedirect("/tables")
