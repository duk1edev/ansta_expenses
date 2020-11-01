from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month, total_amount
from collections import Counter
from django.db.models import Sum

class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            total_amount()
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            category = form.cleaned_data['category']
            if category:
                queryset = queryset.filter(category__id__in=category.all())
                if queryset.count() > 5:
                    self.paginate_by = queryset.count()

            # search by date
            date = form.cleaned_data['date']
            if date:
                queryset = queryset.filter(date=date)

            grouping = form.cleaned_data['grouping']
            if grouping == 'date':
                queryset = queryset.order_by('date', '-pk')
            if grouping == 'category_ascending':
                queryset = queryset.order_by('category__name', 'category__pk')
            if grouping == 'category_descending':
                queryset = queryset.order_by('-category__name', 'category__pk')

            sort_by_date = form.cleaned_data['sort_by_date']
            if sort_by_date == '1':
                queryset = Expense.objects.order_by('date')

            if sort_by_date == '2':
                queryset = Expense.objects.order_by('-date')

            sort_by_category = form.cleaned_data['sort_by_category']
            if sort_by_category == '1':
                queryset = Expense.objects.order_by('category__name')
            if sort_by_category == '2':
                queryset = Expense.objects.order_by('-category__name')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            total_amount=total_amount(),
            **kwargs)


class CategoryView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expenses/category_form.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['count_category'] = Category.objects.annotate(Count('expense')).values('id', 'name', 'expense__count')
        return context


class CreateCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'expenses/category_create_form.html'
    success_url = reverse_lazy('expenses:category-list')


class UpdateCategory(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'expenses/category_update_form.html'
    success_url = reverse_lazy('expenses:category-list')

    def form_valid(self, form):
        if Category.objects.filter(name=form.cleaned_data.get('name')).exists():
            messages.error(self.request, "Category with this Name already exists.")
            return redirect(reverse_lazy('expenses:category-edit', kwargs={'pk': self.kwargs['pk']}))
        else:
            super().form_valid(form)
            return HttpResponseRedirect(self.get_success_url())


class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum'] = Expense.objects.all().filter(category__pk=self.kwargs.get('pk')).aggregate(Sum('amount'))
        return context

