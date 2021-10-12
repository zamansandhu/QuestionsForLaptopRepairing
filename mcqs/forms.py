from django import forms
from django.contrib.auth import authenticate
from .models import *


class UserLoginForm(forms.Form):
    query=forms.CharField(label="username/Email",widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'type':'password','class':'form-control'}))
    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get("query")
        password=self.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        if(user):
            self.cleaned_data["user_obj"]=user
        else:
            raise forms.ValidationError("Invalid Creditional")
        return super(UserLoginForm,self).clean(*args,**kwargs)
class myFormForm(forms.ModelForm):
    class Meta:
        model=myForm
        fields=('name',)
class questionForm(forms.ModelForm):
    class Meta:
        model=questions
        fields=('question',)

class mcqForm(forms.ModelForm):
    class Meta:
        model=mcq
        fields=('question',)