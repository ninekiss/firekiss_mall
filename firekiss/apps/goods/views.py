from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'index.html')
