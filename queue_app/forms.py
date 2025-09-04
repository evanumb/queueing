from django import forms

class TakeTicketForm(forms.Form):
    confirm = forms.BooleanField(initial=True, required=True, label='Confirm to take a ticket')
