import django_filters

from .models import *
from django import forms

class CasesFilter(django_filters.FilterSet):
    class Meta:
        model = Cases
        fields = {
            'payer': ['exact'],
            'number': ['exact'],
            'closed': ['isnull'],
        }

    def __init__(self, *args, **kwargs):
        super(CasesFilter, self).__init__(*args, **kwargs)
        self.filters['payer'].queryset = CustomUser.objects.filter(role=1, is_staff=False)

        self.filters['payer'].extra.update(
            {
                'widget': forms.Select(attrs={'class': 'form-control'})
            })
