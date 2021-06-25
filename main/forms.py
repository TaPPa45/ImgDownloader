from django import forms
from .models import Images


class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Images
        fields = ('title', 'image', 'url')
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['image'].required = False
        self.fields['title'].label = 'Название'
        self.fields['image'].label = 'Файл'
        self.fields['url'].required = False
        self.fields['url'].label = 'Ссылка'

class ResizeForm(forms.Form):
    width = forms.IntegerField(required=False, label='Ширина')
    height = forms.IntegerField(required=False, label='Высота')
