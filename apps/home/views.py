import numpy as np
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from core.settings import BASE_DIR, READY_FILES_ROOT
from .forms import ScanForm
from django.shortcuts import render
from django_tables2 import SingleTableView
from .models import Scan
from .tables import ScanTable
from apps.algo.scanning import Scanning
import os


@login_required(login_url="/login/")
def index(request, scan_id=None):
    print(scan_id)
    scan = Scan()
    if scan_id:
        row = scan.getById(scan_id)
    else:
        row = scan.getLastActive(request.user)
    scanning = Scanning()
    values = scanning.getOutputData(row.path_result)
    sorted_values = np.column_stack(values)
    time_count = scanning.getTime(row.path_result)

    context = {
        'segment': 'index',
        'labels': values[0],
        'values': values[1],
        'sorted': sorted_values[sorted_values[:, 1].argsort()[::-1]][:3],
        'sum_count_query': np.sum(values[1]),
        'time_labels': time_count[0],
        'time_values': time_count[1],
    }
    return render(request, 'home/index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
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
        scan = Scan()
        self.queryset = scan.getByUser(request.user)
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'tables'
        return context

@login_required(login_url="/login/")
def deleteItem(request, scanId):
    scan = Scan()
    row = scan.getById(scanId)
    os.remove(READY_FILES_ROOT + '/' + str(row.path_result))
    row.delete()
    return HttpResponseRedirect("/tables")

@login_required(login_url="/login/")
def scanItem(request, scanId):
    scan = Scan()
    row = scan.getById(scanId)
    action = Scanning()
    file = action.scan(row.path_file)
    os.remove(BASE_DIR + '/' + str(row.path_file))
    scan.updateScan(scanId, 1, 'scanning', file)
    return HttpResponseRedirect("/tables")


@login_required(login_url="/login/")
def profile(request):

    return render(request, 'home/profile.html', {'segment': 'profile'})
