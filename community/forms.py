from django import forms
from community.models import Column, Event


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title', 'content', 'image',]
        labels = {
            'title': '컬럼 제목',
            'content': '컬럼 내용',
            'image': '컬럼 이미지',
            'author': '작성자',
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        labels = {
            'title': '이벤트 제목',
            'content': '이벤트 내용',
            'image': '이벤트 이미지',
        }
