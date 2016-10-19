from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home_page(request):
    return HttpResponse(
        '''
        <h1>Hello, People!</h1>
        <a href="/charges/"/>go to your charges page<a/>
        '''
    )

def charges_page(request):
    return HttpResponse(
        '''
        <a href="/"/>go to home page<a/>
        <table border="1">
            <caption>Charges table</caption>
            <tr>
                <th>date time</th>
                <th>sum</th>
            </tr>
            <tr>
                <td>2016-09-09</td>
                <td>-300</td>
            </tr>
            <tr>
                <td>2016-09-10</td>
                <td>500</td>
            </tr>
        </table>
        '''
    )