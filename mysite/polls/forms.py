from django import forms
from .models import Question, Choice
from django.forms import formset_factory


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)
        labels = {'question_text': 'Enter the question text'}


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)
        labels = {'choice_text': 'Enter the choice text'}


ChoiceFormSet = formset_factory(ChoiceForm, extra=10)
