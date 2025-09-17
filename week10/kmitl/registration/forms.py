from django import forms
from .models import *

from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError


# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)


# class StudentForm(forms.Form):
#     student_id = forms.CharField(max_length=10)
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)

#     # faculty = forms.ForeignKey(Faculty, on_delete=forms.PROTECT)
#     # enrolled_sections = forms.ManyToManyField(Section, blank=True)
    
#     faculty = forms.ModelChoiceField(
#         queryset=Faculty.objects.all(),
#         empty_label="Select an option",
#         required=False,
#         widget=forms.RadioSelect
#     )

#     # section_ids = forms.ModelMultipleChoiceField(
#     #     queryset=Section.objects.all(),
#     #     required=False,
#     # )
#     enrolled_sections = forms.ModelMultipleChoiceField(
#         queryset=Section.objects.all(),
#         required=False,
#     )

#     email = forms.EmailField(required=True)
#     phone_number = forms.CharField(max_length=10)
#     address = forms.CharField(widget=forms.Textarea)


class StudentForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'faculty': forms.RadioSelect,
            'enrolled_sections' : forms.SelectMultiple,
            # 'address': forms.Textarea(attrs={'rows': 3}),
            # 'email': forms.EmailInput(),
        }
    def clean_email(self):
        # cleaned_data = super().clean()
        email = self.cleaned_data.get('email')

        if not email.endswith('@kmitl.ac.th'):
            # self.add_error('email', 'Email must be a kmitl.ac.th address.')
            raise forms.ValidationError(
                'Email must be a kmitl.ac.th address.'
                )

        return email


# class CourseAndSectionForm(ModelForm):
#     course_code = forms.CharField(max_length=20) 
#     course_name = forms.CharField(max_length=200)
#     credits = forms.IntegerField()
    
#     class Meta:
#         model = Section
#         fields = '__all__'

#         # widgets = {
#         #     'start_time': forms.SplitDateTimeWidget(
#         #         date_attrs={"class": "input", "type": "date"},
#         #         time_attrs={"class": "input", "type": "time"}
#         #     ),
#         #     'end_time': forms.SplitDateTimeWidget(
#         #         date_attrs={"class": "input", "type": "date"},
#         #         time_attrs={"class": "input", "type": "time"}
#         #     )
#         # }
#         widgets = {
#             # 'start_time': forms.TimeInput(attrs={"class": "input", "type": "time"}),
#             # 'end_time': forms.TimeInput(attrs={"class": "input", "type": "time"}),        
#         }

#     def clean_courseAndSection(self):
#         cleaned_data = super().clean()

#         return cleaned_data


# class CourseAndSectionForm(ModelForm):
#     start_time = forms.TimeField(
#         widget=forms.TimeInput(attr={'class':'input', 'type': 'time'})
#     )
#     start_time = forms.TimeField(
#         widget=forms.TimeInput(attr={'class':'input', 'type': 'time'})
#     )
#     section_number = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'class':'input', 'type': 'text'}))
#     semester = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'input', 'type': 'number'}))
#     professor = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'input'}))
#     day_of_week = forms.ChoiceField(
#         choices=Section.DAY_OF_WEEK_CHOICES(),
#         widget=forms.Select(attrs={'class':'input'}),
#         required=True
#     )
#     capacity = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(attrs={'class':'input'}))

#     class Meta:
#         model = Section
#         fields = '__all__'

#         widgets = {
#             'course_code': forms.TextInput(attrs={'class':'input', 'type': 'text'}),
#             'course_name': forms.TextInput(attrs={'class':'input', 'type': 'text'}),
#             'credits': forms.NumberInput(attrs={'class':'input', 'type': 'number'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')
#         capacity = cleaned_data.get('capacity')

#         if end_time and start_time and end_time <= start_time:
#             self.add_error('end_time', 'End time must be after start time.')
#         if capacity <= 20:
#             self.add_error('capacity', 'Capacity must be greater than 20.')

        
        # return super().clean()



    
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ["section_number", "semester", "professor","day_of_week","start_time","end_time","capacity"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"class": "input", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "input", "type": "time"})
        }
    def clean(self):
        cleaned_data = super().clean()
        
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        capacity = cleaned_data.get("capacity")
        
        if start_time and end_time and end_time <= start_time:
            self.add_error("end_time", "End time must be greater than start time.")
        
        if capacity and capacity <= 20:
            self.add_error("capacity", "Capacity must be greater than 20.")
        
        return cleaned_data