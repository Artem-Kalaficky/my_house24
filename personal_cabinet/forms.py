import datetime

from django.forms import ModelForm, Select, TimeInput, Textarea

from crm.forms import DateInputWidget
from crm.models import Application, House, Apartment


# region Applications
class OwnerApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.datetime.today().strftime('%d.%m.%Y')
        self.fields['time'].initial = datetime.datetime.today().strftime('%H:%MM')

    class Meta:
        model = Application
        fields = ('date', 'time', 'description', 'apartment', 'type_master', 'status')
        widgets = {'date': DateInputWidget(attrs={'class': 'form-control',
                                                  'type': 'text'}),
                   'time': TimeInput(attrs={'class': 'form-control',
                                            'type': 'text'}),
                   'description': Textarea(attrs={'rows': 5,
                                                  'class': 'form-control'}),
                   'apartment': Select(attrs={'class': 'form-select'}),
                   'type_master': Select(attrs={'class': 'form-select'}),
                   'status': Select(attrs={'class': 'form-select',
                                           'hidden': 'true'})}
# endregion Applications
