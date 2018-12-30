from django import forms

class EmailNotificationForm(forms.Form):
    enabled = forms.BooleanField(required=False)
    channel_id = forms.EmailField(required=True, label="Send emails to")
    notification_id = forms.CharField(widget=forms.HiddenInput(), required=True)

class TelegramNotificationForm(forms.Form):
    enabled = forms.BooleanField(required=False)
    notification_id = forms.CharField(widget=forms.HiddenInput(), required=True)
