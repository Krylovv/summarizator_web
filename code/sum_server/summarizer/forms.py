from django import forms


class UserForm(forms.Form):
    news = forms.CharField(max_length=1000, label="Введите новость")

