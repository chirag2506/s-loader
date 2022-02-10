

from django.shortcuts import render
from django.http import HttpResponse
from .resources import PersonResource
from tablib import Dataset
from .models import Person
from django.contrib import messages


def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_person = request.FILES['myfile']
        
        if not new_person.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request,'upload.html')

        imported_data = dataset.load(new_person.read(),format='xlsx')
        for data in imported_data:
            value=Person(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()
    return render(request,'upload.html')   
