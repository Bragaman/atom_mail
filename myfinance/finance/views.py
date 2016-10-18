from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home_page(request):
    return HttpResponse(
        '''
        <h1>Hello, Dad!</h1>
        <a href="/charges/"/>go to Dads page<a/>
        '''
    )

def charges_page(request):
    return HttpResponse(
        '''
        <a href="/"/>go home<a/>
        
        '''
    )