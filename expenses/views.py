from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import Category, Expense
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
# Create your views here.

def expenses_search(request):

    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner= request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner= request.user) | Expense.objects.filter(
            description__icontains=search_str, owner= request.user) | Expense.objects.filter(
            category__icontains=search_str, owner= request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)

class ExpenseListView(LoginRequiredMixin, ListView):

    template_name = 'expenses/index.html'
    context_object_name = 'expenses'
    model = Expense
    paginate_by = 2

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['currency'] = UserPreference.objects.get(user=self.request.user).currency
        return context

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'expenses/add_expense.html'
    model = Expense
    fields = [
        "amount",
        "description",
        "category",
    ]

    def get(self, request,  *args, **kwargs):
        context = {}
        
        return super(ExpenseCreateView, self).get(request, *args, **kwargs)
        #return render(request, 'expenses/add_expense.html', context)

    def post(self, request):
        error_messages = []
        context = {}

        context['values'] = request.POST
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        category = request.POST.get('category')

        
        if not amount:
            error_messages.append('amount field is required')

        if not description:
            error_messages.append('description field is required')

        if not date:
            date = timezone.now()

        if error_messages:
            for message in error_messages:
                messages.error(request, message)

            context['categories'] = get_categories_all(request)
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['categories'] = get_categories_all(self.request)
        return context


class ExpenseEditView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    template_name = 'expenses/edit.html'
    model = Expense
    success_message = "Expense was updated successfully!!"

    fields = [
        "amount",
        "description",
        "category",
        "date"
    ]

    success_url ="/expenses"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['categories'] = get_categories_all(self.request)
        return context

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'expenses/delete.html'
    model= Expense

    success_url ="/"


def expense_category_summary(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30*6)

    expenses = Expense.objects.filter(owner= request.user, date__gte=six_months_ago, date__lte=today)
    
    data = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))
    

    def get_expense_category_amount(category):
        amount = 0 
        filtered_by_category = expenses.filter(category = category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for expense in expenses:
        for category in category_list:
            data[category] = get_expense_category_amount(category)
    

    return JsonResponse({'expense_category_data':data}, safe= False)

def expense_stats(request):
    return render(request, 'expenses/stats.html')

def get_categories_all(request):
    return Category.objects.all()