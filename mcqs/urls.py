from django.urls import path
from .views import *
urlpatterns = [
    path('', index,name='index'),
    path('login', user_login,name="login"),
    path('logout/', user_logout,name="logout"),
    path('signup',signup, name='signup'),
    path('forms',FormList.as_view(), name='forms'),
    path('addform',FormCreate.as_view(), name='addform'),
    path('updateform/<int:pk>',FormUpdate.as_view(), name='updateform'),
    path('detailform/<int:pk>/detail',FormDetail.as_view(), name='detailform'),
    path('deleteform/<int:pk>/delete',FormDelete.as_view(), name='deleteform'),
    path('detailform/<int:pk>/addquestion',QuestionCreate.as_view(), name='addquestion'),
    path('detailform/<int:pk2>/deletequestion/<int:pk>',QuestionDelete.as_view(), name='deletequestion'),
    path('detailform/<int:pk2>/updatequestion/<int:pk>',QuestionUpdate.as_view(), name='updatequestion'),
    path('detailform/<int:pk>/addmcq',McqCreate.as_view(), name='addmcq'),
    path('detailform/<int:pk2>/deletemcq/<int:pk>',McqDelete.as_view(), name='deletemcq'),
    path('detailform/<int:pk2>/updatemcq/<int:pk>',McqUpdate.as_view(), name='updatemcq'),
    path('detailform/<int:pk2>/mcq/<int:pk>/addchoice',addchoice.as_view(), name='addchoice'),
    path('formfill/<int:pk>',renderform.as_view(), name='formfill'),
    path('submissions',SubmissionList.as_view(), name='submissions'),
    path('submissions/<int:pk>/detail',SubmissionDetail.as_view(), name='detailsubmission'),
    path('submissions/<int:pk>/delete',SubmissionDelete.as_view(), name='deletesubmission'),
]
