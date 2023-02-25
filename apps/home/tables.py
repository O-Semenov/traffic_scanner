import django_tables2 as tables
from django_tables2 import TemplateColumn


class ScanTable(tables.Table):
    style = {"th": {"class": "text-center text-uppercase  "},
             "td": {"class": "text-center text-secondary font-weight-bolder opacity-7", "header": "header"}}
    # id = tables.Column(attrs=style, exclude_from_export=True)
    counter = tables.Column(verbose_name='#', empty_values=(), orderable=False, attrs=style)
    path_file = tables.Column(verbose_name='File name', attrs=style)
    created_at = tables.Column(verbose_name='Date', attrs=style)
    request = tables.Column(attrs=style)
    status = tables.Column(attrs=style)
    action = TemplateColumn(attrs=style, template_code='<a href="" class="btn btn-success">Scan</a>')

    def render_counter(self, record):
        records = list(self.data)
        index = records.index(record)
        counter = index + 1
        return counter

    class Meta:
        attrs = {"class": "table align-items-center mb-0"}
        template_name = "django_tables2/bootstrap4.html"
