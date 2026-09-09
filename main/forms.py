from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control"
            }),

            'introduction': forms.Textarea(attrs={
                'class': "form-control",
                'rows': 4,
            }),
            'category': forms.Select(attrs={
                "class": "form-select"
            }),
            'price': forms.NumberInput(attrs={
                "class": "form-control"
            }),
            'image': forms.FileInput(attrs={
                'class': "form-control"
            })
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError(
                "Narx 0 dan katta bo'lishi kerak"
            )

        return price

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title and " " in title:
            raise ValidationError(
                "Kitob nomi orasida bo'sh joy bo'lmasligi kerak"
            )

        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': "form-control",
                'rows': "3",
                "placeholder": "Kitob bo'yicha tahliliy fikringiz..."
            })
        }








