from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserLoginForm,myFormForm,questionForm,mcqForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,get_user_model ,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.views import View
import json
from django.middleware import csrf
# Create your views here.

@login_required(login_url='/login')
def index(request):
    forms=myForm.objects.all()
    context={'forms':forms}
    return render(request,'home.html',context)
class renderform(View):
    def get(self,*args,**kwargs):
        context={"object":myForm.objects.get(pk=self.kwargs['pk'])}
        context['csrf_token']=csrf.get_token(self.request)
        return render(self.request,'form.html',context)
    def post(self,*args,**kwargs):
        error=False
        try:
            obj=myForm.objects.get(pk=self.kwargs['pk'])
            newsubmission=submission(name=obj.name,submittedby=self.request.user)
            newsubmission.save()
            for q in obj.questions.all():
                print(q)
                answer=self.request.POST['question-'+str(q.pk)]
                newq=questions(question=q.question,answer=answer)
                newq.save()
                newsubmission.questions.add(newq)
            for m in obj.mcqs.all():
                print(m)
                answer=self.request.POST['mcq-'+str(m.pk)]
                newq=mcq(question=m.question,answer=answer)
                newq.save()
                newsubmission.mcqs.add(newq)
        except:
            error=True
        context={"error":error}
        return render(self.request,'submission.html',context)
        
def user_login(request,*args,**kwargs):
    print('login request')
    if(request.user.is_authenticated):
        print('user already authenticated')
        return HttpResponseRedirect('/')
    form =UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj=form.cleaned_data.get("user_obj")
        c=login(request,user_obj)
        print("Form is created login",user_obj.username,c,form)
        return HttpResponseRedirect('/')
    else:
        print('invalid')
    return render(request,"login.html",{"form":form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")
class SubmissionList(ListView):
    model = submission
    template_name='Submissions/list.html'
class SubmissionDetail(DetailView):
    model=submission
    template_name='Submissions/detail.html'
    
class SubmissionDelete(DeleteView):
    model=submission
    template_name='Submissions/delete.html'
    success_url='/submissions'
class FormList(ListView):
    model = myForm
    template_name='Forms/list.html'
class FormCreate(CreateView):
    form_class=myFormForm
    template_name='Forms/create.html'
    success_url='/forms'
class FormUpdate(UpdateView):
    model=myForm
    form_class=myFormForm
    template_name='Forms/update.html'
    success_url = '/forms'
class FormDetail(DetailView):
    model=myForm
    template_name='Forms/detail.html'
    def get_context_data(self, *args, **kwargs):
        context = (super(FormDetail, self).get_context_data)(*args, **kwargs)
        context['pk'] = self.kwargs['pk']
        return context
class FormDelete(DeleteView):
    model=myForm
    template_name='Forms/delete.html'
    success_url='/forms'
class QuestionCreate(CreateView):
    form=questionForm
    template_name='Questions/create.html'
    fields=('question',)
    def get_queryset(self):
        new_context=questions.objects.all()
        return new_context
    def form_valid(self, form):
        form.save()
        myform=myForm.objects.get(pk=self.kwargs['pk'])
        myform.questions.add(form.instance)
        return HttpResponseRedirect(reverse('detailform', kwargs={"pk":self.kwargs['pk']}))
class QuestionDelete(DeleteView):
    model=questions
    template_name='Questions/delete.html'
    success_url = '/forms'
    def delete(self, request, *args, **kwargs):
        x=(super(QuestionDelete, self).delete)(request,*args, **kwargs)
        return HttpResponseRedirect(reverse('detailform', kwargs={"pk":self.kwargs['pk2']}))
class QuestionUpdate(UpdateView):
    model=questions
    form_class=questionForm
    template_name='Questions/update.html'
    success_url = '/forms'
    def get_success_url(self):
        return reverse('detailform', kwargs={"pk":self.kwargs['pk2']})

class McqCreate(CreateView):
    form=mcqForm
    template_name='MCQS/create.html'
    fields=('question',)
    def get_queryset(self):
        new_context=mcq.objects.all()
        return new_context
    def form_valid(self, form):
        form.save()
        myform=myForm.objects.get(pk=self.kwargs['pk'])
        myform.mcqs.add(form.instance)
        return HttpResponseRedirect(reverse('detailform', kwargs={"pk":self.kwargs['pk']}))

class McqDelete(DeleteView):
    model=mcq
    template_name='MCQS/delete.html'
    success_url = '/forms'
    def get_success_url(self):
        return reverse('detailform', kwargs={"pk":self.kwargs['pk2']})
class McqUpdate(UpdateView):
    model=mcq
    form_class=mcqForm
    template_name='MCQS/update.html'
    success_url = '/forms'
    def get_success_url(self):
        return reverse('detailform', kwargs={"pk":self.kwargs['pk2']})
class addchoice(View):
    def post(self,*args,**kwargs):
        data = json.loads(self.request.body.decode('utf8').replace("'", '"'))
        try:
            newchoice=choice(name=data['value'])
            newchoice.save()
            currentmcq=mcq.objects.get(pk=data['id'])
            currentmcq.choices.add(newchoice)
            return HttpResponse('ok')
        except:
            return HttpResponse('failed')
    