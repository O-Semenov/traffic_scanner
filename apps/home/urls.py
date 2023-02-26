from django.urls import path, re_path
from apps.home import views
from apps.home.views import ScanListView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('scaning', views.scaning, name='scaning'),
    path('tables/deleteItem/<int:scanId>', views.deleteItem, name='deleteItem'),
    path('tables', ScanListView.as_view()),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
