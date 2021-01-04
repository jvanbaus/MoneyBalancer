import django_filters
from django_filters import DateFilter

from .models import *

class accountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = {
            'account_balance' : {'exact'},
            'account_inital_balance' : {'exact'},
            'account_catagory' : {'exact'},
            'account_subcatagory': {'exact'},
        }

class journalFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="journal_creation_date", lookup_expr='gte')
    end_date = DateFilter(field_name="journal_creation_date", lookup_expr='lte')

    class Meta:
        model = Journal
        fields = {
            'journal_status': {'exact'},
            'journal_user' : {'exact'},
        }
        exclude = ['journal_creation_date']



