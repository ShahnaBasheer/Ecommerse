from django import forms
from django.contrib.auth.models import User
from .models import CustomUser


GENDER=[('Female','Female'),
         ('Male','Male'),
         ('Transgender','Transgender'),
        ]

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(forms.ModelForm):
    Repeat_Password = forms.CharField(max_length=150,widget=forms.PasswordInput,required=True)
    class Meta:
       model = CustomUser
       fields = ['username','first_name','last_name','email','password',
                 'gender','dob','phone_no']   
       widgets = {
           'dob':DateInput(),
           'gender':forms.RadioSelect(choices=GENDER),
           'first_name':forms.TextInput(attrs={'required':True}),
           'last_name':forms.TextInput(attrs={'required':True}),
           'email':forms.EmailInput(attrs={'required':True}),
           'password':forms.PasswordInput(),
        }
       help_texts = {
           'username':None,           
       }
       labels = {
            'phone_no':'Mobile number',
       }



       
    

        
       