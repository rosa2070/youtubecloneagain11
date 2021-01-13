from django import forms
from .models import Video, Comment


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            'description',
            'file',
            'photo',
        ]

class Commentform(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'