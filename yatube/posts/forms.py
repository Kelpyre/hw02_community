from typing import Literal, Union

from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields: tuple[Literal['text'], Literal['group']] = ('text', 'group')
        widgets: dict[str, Union[forms.Textarea, forms.Select]] = {
            "text": forms.Textarea(attrs={
                'class': 'form-control',
                'cols': '40',
                'rows': '10'
                }
            ),
            "group": forms.Select(attrs={
                'class': 'form-control'
                }
            ),
        }

        def clean_text(self):
            data = self.cleaned_data['text']
            if data is None:
                raise ValidationError('Заполните поле!')
            return data
