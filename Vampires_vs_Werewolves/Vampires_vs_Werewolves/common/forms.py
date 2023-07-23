from django import forms


class WorkForm(forms.Form):
    # Define the choices for the hours field from 1 to 12
    HOURS_CHOICES = [(str(i), str(i)) for i in range(1, 13)]
    hours = forms.ChoiceField(choices=HOURS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
