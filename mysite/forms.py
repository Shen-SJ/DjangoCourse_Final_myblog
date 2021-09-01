from django import forms
from . import models
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    user_email = forms.EmailField()
    user_message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].label = '您的名子'
        self.fields['user_email'].label = '您的電子信箱'
        self.fields['user_message'].label = '您的意見'
        self.fields['captcha'].label = '確定你不是機器人'

        # for field in iter(self.fields):
        #     if field == 'user_school':
        #         continue
        #     self.fields[field].widget.attrs.update(
        #         {
        #             'class': 'form-control'
        #         }
        #     )
