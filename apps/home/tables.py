import django_tables2 as tables
from django_tables2 import TemplateColumn


class ScanTable(tables.Table):
    style = {"th": {"class": "text-center text-uppercase"},
             "td": {"class": "text-center text-secondary font-weight-bolder opacity-7", 'data-href': '/index.html'}}
    counter = tables.Column(verbose_name='#', empty_values=(), orderable=False, attrs=style)
    path_file = tables.Column(verbose_name='File name', attrs=style)
    created_at = tables.Column(verbose_name='Date', attrs=style)
    request = tables.Column(attrs=style)
    status = tables.Column(attrs=style)
    action = TemplateColumn(attrs=style,
                            template_name='includes/button_template.html')

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

    def render_path_file(self, value):
        value = str(value)
        return value[value.find('/') + 1:]

    class Meta:
        attrs = {"class": "table align-items-center mb-0"}
        template_name = "django_tables2/bootstrap4.html"
