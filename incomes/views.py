from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import Income, Source
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def incomes_search(request):

    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText') 
        incomes = Income.objects.filter(
                owner= request.user, amount__istartswith=search_str) | Income.objects.filter(
                    owner= request.user, date__istartswith=search_str) | Income.objects.filter(
                    owner= request.user, description__icontains=search_str) | Income.objects.filter(
                    owner= request.user, source__icontains=search_str)

        data = incomes.values()

        return JsonResponse(list(data), safe=False)


class IncomeListView(LoginRequiredMixin, ListView):

    template_name = 'incomes/index.html'
    context_object_name = 'incomes'
    model = Income
    paginate_by = 3

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['currency'] = UserPreference.objects.get(user=self.request.user).currency
        return context

class IncomeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'incomes/add_income.html'
    model = Income
    fields = [
        'amount',
        'description',
        'source',
    ]

    def get(self, request, *args, **kwargs):
        context = {}

        return super(IncomeCreateView, self).get(request, *args, **kwargs)

    def post(self, request):
        error_messages = []
        context = {}

        context['values'] = request.POST
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        source = request.POST.get('source')

        
        if not amount:
            error_messages.append('amount field is required')

        if not description:
            error_messages.append('description field is required')

        if not date:
            date = timezone.now()

        if error_messages:
            for message in error_messages:
                messages.error(request, message)

            context['sources'] = get_sources_all(request)
            return render(request, 'incomes/add_income.html', context)

        Income.objects.create(owner=request.user, amount=amount, description=description, source=source, date=date)
        messages.success(request, 'Income saved successfully')

        return redirect('incomes')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sources'] = get_sources_all(self.request)
        return context

class IncomeEditView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    template_name = 'incomes/edit.html'
    model = Income
    success_message = "Income was updated successfully!!"

    fields = [
        "amount",
        "description",
        "source",
        "date"
    ]

    success_url ="/incomes"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sources'] = get_sources_all(self.request)
        return context

class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'incomes/delete.html'
    model= Income

    success_url ="/incomes"

def get_sources_all(request):
    return Source.objects.all()