from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import TruncMonth
from django.db.models.functions import Coalesce
from .models import Expense


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
            .annotate(category_name=Coalesce('category__name', Value('-')))
            .order_by()
            .values('category_name')
            .annotate(s=Sum('amount'))
            .values_list('category_name', 's')
    ))


def summary_per_year_month(queryset):
    return OrderedDict(sorted(
        queryset
            .annotate(
            year_month=TruncMonth('date'),
        )
            .order_by()
            .values('year_month')
            .annotate(sum=Sum('amount'))
            .values_list('year_month', 'sum')
    ))


def total_amount():
    all_amount = Expense.objects.aggregate(s=Sum('amount'))
    return float(all_amount['s'])


def total_amount_delete(pk):
    amount_by_category = Expense.objects.all().filter(category__pk=pk).aggregate(sum=Sum('amount'))
    if amount_by_category['sum'] is None:
        return 0
    else:
        return amount_by_category['sum']

