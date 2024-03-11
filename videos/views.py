from django.shortcuts import render
from django.http import HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema

from .forms import ResumeForm

# Создайте здесь представления.
@swagger_auto_schema(request_body=ResumeForm)
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/") 
    else:
        form = ResumeForm()
    return render(request, 'files/upload.html', {'form':form})

