from django import forms
from .models import Expense, Category
# from multiselectfield import


class ExpenseSearchForm(forms.ModelForm):
    GROPING = ('date',)
    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))
    #
    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Category.objects.all())


    class Meta:
        model = Expense
        fields = ('name', 'date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False
