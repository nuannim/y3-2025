from django import forms
from .models import *

# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)


class StudentForm(forms.Form):
    student_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    # faculty = forms.ForeignKey(Faculty, on_delete=forms.PROTECT)
    # enrolled_sections = forms.ManyToManyField(Section, blank=True)
    
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        empty_label="Select an option",
        required=False,
        widget=forms.RadioSelect
    )

    section_ids = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all(),
        required=False,
    )

    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)

