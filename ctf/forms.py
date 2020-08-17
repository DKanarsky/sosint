
from django import forms

class SubmitForm(forms.Form):
    flag_id = forms.IntegerField(
        widget=forms.HiddenInput()
        )
    answer = forms.CharField(
        max_length=100, 
        min_length=1, 
        strip=True, 
        required=True, 
        label="Ответ",
        widget=forms.TextInput(
            attrs={
                'class': 'mdc-text-field__input',
                'id':'submit-answer-input',
                'autocomplete': 'off'
            }
        ))