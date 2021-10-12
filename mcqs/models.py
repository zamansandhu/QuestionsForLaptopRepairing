from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class choice(models.Model):
    name=models.CharField(max_length=100,default="test")
    def __str__(self):
        return self.name
class mcq(models.Model):
    question=models.CharField(max_length=500,default="")
    choices=models.ManyToManyField(choice)
    answer=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.question
    def get_cname(self):
        return 'mcq'

class questions(models.Model):
    question=models.CharField(max_length=500,default="")
    answer=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.question
    def get_cname(self):
        return 'question'
    
class myForm(models.Model):
    name=models.CharField(max_length=100,default="Question Survey")
    mcqs=models.ManyToManyField(mcq)
    questions=models.ManyToManyField(questions)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detailform',kwargs={"pk":self.pk})
    def get_update_url(self):
        return reverse('updateform',kwargs={"pk":self.pk})
    def get_delete_url(self):
        return reverse('deleteform',kwargs={"pk":self.pk})

class submission(models.Model):
    submittedby=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,default="Question Survey")
    mcqs=models.ManyToManyField(mcq)
    questions=models.ManyToManyField(questions)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detailsubmission',kwargs={"pk":self.pk})
    def get_delete_url(self):
        return reverse('deletesubmission',kwargs={"pk":self.pk})