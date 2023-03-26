import django_tables2 as tables
from django_tables2 import TemplateColumn


class ScanTable(tables.Table):
    style = {"th": {"class": "text-center text-uppercase"},
             "td": {"class": "text-center text-secondary font-weight-bolder opacity-7"},
             "tr": {'class': 'clickable-row', 'data-href': '/index.html'}}
    counter = tables.Column(verbose_name='№', empty_values=(), orderable=False, attrs=style)
    # path_file = tables.Column(verbose_name='File name', attrs=style)
    path_file = TemplateColumn(verbose_name='File name', attrs=style, template_name='includes/link-template.html')
    created_at = tables.Column(verbose_name='Date', attrs=style)
    request = tables.Column(attrs=style)
    status = tables.Column(attrs=style)
    action = TemplateColumn(attrs=style,
                            template_name='includes/button-template.html')

    def render_counter(self, record):
        records = list(self.data)
        index = records.index(record)
        counter = index + 1
        return counter

    def render_status(self, value):
        if value == 0:
            return '-'
        else:
            return 'OK'

    class Meta:
        attrs = {"class": "table align-items-center mb-0"}
        template_name = "django_tables2/bootstrap4.html"
