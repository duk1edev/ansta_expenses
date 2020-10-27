from django import forms
from .models import Expense


class ExpenseSearchForm(forms.ModelForm):
    GROPING = ('date',)
    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))

    class Meta:
        model = Expense
        fields = ('name', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False
