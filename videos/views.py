from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ResumeForm

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/") 
    else:
        form = ResumeForm
    return render(request, 'videos/resume.html', {'form':form})