from django.db import models
from django import forms


class User(models.Model):   #пользователь
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=False)
    bill = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=False)
    surname = models.CharField(max_length=255, null=False)


class Bet(models.Model):  #ставка
    idBet = models.IntegerField(unique=True)
    size = models.IntegerField(null=False)
    result = models.BooleanField(null=False)


class Fight(models.Model):  #бой
    idFight = models.IntegerField(unique=True)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    boxer1 = models.TextField(max_length=255, null=False)
    boxer2 = models.TextField(max_length=255, null=False)
    idBoxer1 = models.IntegerField(null=True)
    idBoxer2 = models.IntegerField(null=True)

    def __str__(self):
        return self.boxer1

    #def __unicode__(self):
    #    return self.boxer1


class Boxer(models.Model):  #Боксёр
    idBoxer = models.IntegerField(unique=True)
    title = models.TextField(max_length=255)
    boxer_first_name = models.CharField(max_length=255, null=False)
    boxer_last_name = models.CharField(max_length=255, null=False)

#---------------------------------------------------------------------------


class RegisterForm(forms.Form):
    login = forms.CharField(label='Login', min_length=5)
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    email = forms.CharField(label='Email', min_length=1)
    #userBill = forms.IntegerField(label='Bill')
    surname = forms.CharField(label='Surname', min_length=1)
    name = forms.CharField(label='Name', min_length=1)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Пароли не совпадают")
        usrs = User.objects.filter(username=cleaned_data.get('login'))
        if len(usrs) > 0:
            raise forms.ValidationError("Пользователь с данным логином уже существует")
