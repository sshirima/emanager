from django.shortcuts import render
from django.views import View
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
import os
import json

# Create your views here.

class UserPreferenceView(View):

    def get(self, request):
        context = {}

        context['userpreference'] = self.get_user_preference(request)
        context['currencies'] = self.get_currencies_from_files()
        return render(request, 'userpreferences/index.html', context)


    def post(self, request):
        context = {}
        currency = request.POST['currency']

        user_preference = self.get_user_preference(request)
        
        if user_preference:
            user_preference.currency = currency
            messages.info(request, 'Currency preferences updated!')

        else:
            user_preference = UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, 'Currency preferences created!')

        user_preference.save()
        context['userpreference'] = user_preference
        context['currencies'] = self.get_currencies_from_files()
        return render(request, 'userpreferences/index.html', context)


    def get_user_preference(self, request):
        try:
            user_preference = UserPreference.objects.get(user=request.user)
        
            return user_preference

        except UserPreference.DoesNotExist as e:
            print(str(e))
            return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['currencies'] = self.get_currencies_from_files()
        return context

    def get_currencies_from_files(self):
        currencies_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for key, value in data.items():
                currencies_data.append({'name':key, 'value':value})


        return currencies_data

