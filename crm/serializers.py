import datetime
import json

from django.utils import timezone, dateformat

from crm.models import House

houses = House.objects.prefetch_related('sections').all()


def my_serialize(queryset):
    json_data = json.loads(json.dumps([{'number': str(obj.number).zfill(10),
                                        'status': obj.get_status_display(),
                                        'date': obj.date.strftime("%d.%m.%Y"),
                                        'month': dateformat.format(obj.date, 'F Y'),
                                        'house': str([x.name for x in houses
                                                      if obj.apartment.section in x.sections.all()][0]),
                                        'section': obj.apartment.section.name,
                                        'apartment': obj.apartment.number,
                                        'meter': obj.meter.name,
                                        'expense': obj.expense,
                                        'unit': obj.meter.unit.name} for obj in queryset]))
    return json_data
