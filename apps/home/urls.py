from django.urls import path, re_path
from apps.home import views
from apps.home.views import ScanListView

urlpatterns = [

    # The home page
    path('scanning', views.scanning, name='scanning'),
    path('profile', views.profile, name='profile'),
    path('tables', ScanListView.as_view(), name='tables'),
    path('tables/deleteItem/<int:scanId>', views.deleteItem, name='deleteItem'),
    path('tables/download/<int:scanId>', views.download, name='download'),
    path('tables/scanItem/<int:scanId>', views.scanItem, name='scanItem'),

    re_path(r'^(?P<scan_id>[0-9]+)*', views.index, name='home'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
