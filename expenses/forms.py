from django import forms
from .models import Expense, Category
# from multiselectfield import


class ExpenseSearchForm(forms.ModelForm):
    GROPING = ('date', 'category_ascending', 'category_descending')
    SORTING_BY = (
        ('0', ''),
        ('1', 'Ascending'),
        ('2', 'Descending'),
    )
    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))
    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Category.objects.all())
    sort_by_date = forms.ChoiceField(choices=SORTING_BY, initial='')
    sort_by_category = forms.ChoiceField(choices=SORTING_BY, initial='')

    class Meta:
        model = Expense
        fields = ('name', 'date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False
