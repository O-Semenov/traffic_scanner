import django_tables2 as tables
from .models import Scan


class ScanTable(tables.Table):
    style = {"th": {"class": "text-center text-uppercase  "},
            "td": {"class": "text-center text-secondary font-weight-bolder opacity-7"}}
    id = tables.Column(attrs=style, exclude_from_export=True)
    path_file = tables.Column(attrs=style)
    created_at = tables.Column(attrs=style)
    request = tables.Column(attrs=style)
    status = tables.Column(attrs=style)



    class Meta:
        attrs = {"class": "table align-items-center mb-0"}
        template_name = "django_tables2/bootstrap4.html"