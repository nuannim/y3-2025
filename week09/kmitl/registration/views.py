from django.shortcuts import render, redirect
from registration.models import *
from django.db.models import Value
from django.db.models.functions import Concat
from registration.forms import *


# Create your views here.
def index(request):
    student_list = Student.objects.all()

    search = request.GET.get("search", '')
    filter = request.GET.get('filter')

    

    if search:
        if filter == 'email':
            student_list = student_list.filter(studentprofile__email__icontains=search)
        elif filter == 'faculty':
            student_list = student_list.filter(faculty__name__icontains=search)
        else:
            student_list = student_list.annotate(
                fullname=Concat('first_name', Value(' '), 'last_name')
            )
            student_list = student_list.filter(fullname__icontains=search)
            # student_list = student_list.filter(first_name__icontains=search) | student_list.filter(last_name__icontains=search)

    return render(
        request, 'index.html', 
        context= {
            'total': student_list.count(),
            'student_list': student_list,
            'search': search,
            'filter': filter
            }
        )


def professor(request):
    prof_list = Professor.objects.all()

    search = request.GET.get("search", '')
    filter = request.GET.get('filter')

    if search:
        if filter == 'faculty':
            prof_list = prof_list.filter(faculty__name__icontains=search)
        else:
            # prof_list = prof_list.filter(first_name__icontains=search) | prof_list.filter(last_name__icontains=search)
            prof_list = prof_list.annotate(
                fullname=Concat('first_name', Value(' '), 'last_name')
            )
            prof_list = prof_list.filter(fullname__icontains=search)


    return render(
        request,
        'professor.html',
        context={
            'total': prof_list.count(),
            'professor_list': prof_list,
            'search': search,
            'filter': filter
        }
    )

def course(request):
    course_list = Course.objects.all()

    search = request.GET.get("search", '')

    if search:
        course_list = course_list.filter(course_name__icontains=search)

    return render(
        request,
        'course.html',
        context = {
            'total': course_list.count(),
            'course_list': course_list,
            'search': search
        }
    )


def faculty(request):
    faculty_list = Faculty.objects.all()

    search = request.GET.get("search", '')

    if search:
        faculty_list = faculty_list.filter(name__icontains=search)

    return render( 
        request,
        'faculty.html',
        context = {
            'total': faculty_list.count(),
            'faculty_list': faculty_list,
            'search': search,
        }
    )


# def student_search(request):
#     search = request.GET.get("search", '')
#     filter = request.GET.get('filter')


def createstudent(request):
    faculties = Faculty.objects.all()
    sections = Section.objects.all()

    if request.method == 'GET':
        form = StudentForm()

        return render(
            request,
            'create_student.html',
            context = {
                'faculties': faculties,
                'sections': sections,
                'form': form
            }
        )
    elif request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():


            student_id = form.cleaned_data['student_id']
            faculty = form.cleaned_data['faculty']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            section_ids = form.cleaned_data['section_ids']


            # student_id = request.POST.get('student_id')
            # faculty_id = request.POST.get('faculty_id')
            # first_name = request.POST.get('first_name')
            # last_name = request.POST.get('last_name')
            # email = request.POST.get('email')
            # phone_number = request.POST.get('phone_number')
            # address = request.POST.get('address')
            # section_ids = request.POST.getlist('section_ids')

            print('=====')
            print('student_id:', student_id)
            print('faculty:', faculty)
            print('first_name:', first_name)
            print('last_name:', last_name)
            print('email:', email)
            print('phone_number:', phone_number)
            print('address:', address)
            print('section_ids:', section_ids)

            # f = Faculty.objects.get(pk=int(faculty_id))
            f = Faculty.objects.get(pk=int(faculty.id))


            s = Student.objects.create(
                student_id = student_id,
                first_name = first_name,
                last_name = last_name,
                faculty = f
            )
            s.enrolled_sections.set(section_ids)

            StudentProfile.objects.create(
                student = s,
                email = email,
                phone_number = phone_number,
                address = address
            )

            return redirect('index')
        else:
            form = StudentForm()
        
        return render(request, 'create_student.html', {'form': form})





def updatestudent(request, student_id):
    if request.method == 'GET':

        student = Student.objects.get(student_id=student_id)
        faculty = student.faculty 
        first_name = student.first_name
        last_name = student.last_name
        email = student.studentprofile.email
        phone_number = student.studentprofile.phone_number
        address = student.studentprofile.address
        section_ids = student.enrolled_sections.all()

        data = {
            'student_id': student_id,
            'faculty': faculty,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'address': address,
            'section_ids': section_ids
        }

        form = StudentForm(data)

        return render(
            request,
            'update_student.html',
            context = {
                'form': form
            }
        )

    elif request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():


            student_id = form.cleaned_data['student_id']
            faculty = form.cleaned_data['faculty']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            section_ids = form.cleaned_data['section_ids']


            # student_id = request.POST.get('student_id')
            # faculty_id = request.POST.get('faculty_id')
            # first_name = request.POST.get('first_name')
            # last_name = request.POST.get('last_name')
            # email = request.POST.get('email')
            # phone_number = request.POST.get('phone_number')
            # address = request.POST.get('address')
            # section_ids = request.POST.getlist('section_ids')

            print('=====')
            print('student_id:', student_id)
            print('faculty:', faculty)
            print('first_name:', first_name)
            print('last_name:', last_name)
            print('email:', email)
            print('phone_number:', phone_number)
            print('address:', address)
            print('section_ids:', section_ids)

            # f = Faculty.objects.get(pk=int(faculty_id))
            f = Faculty.objects.get(pk=int(faculty.id))

            s = Student.objects.get(student_id=student_id)
            s.first_name = first_name
            s.last_name = last_name
            s.faculty = f
            s.enrolled_sections.set(section_ids)
            s.save()

            # s = Student.objects.create(
            #     student_id = student_id,
            #     first_name = first_name,
            #     last_name = last_name,
            #     faculty = f
            # )
            # s.enrolled_sections.set(section_ids)

            sp = StudentProfile.objects.get(student=s)
            sp.email = email
            sp.phone_number = phone_number
            sp.address = address
            sp.save()

            # StudentProfile.objects.create(
            #     student = s,
            #     email = email,
            #     phone_number = phone_number,
            #     address = address
            # )

            return redirect('index')
        else:
            form = StudentForm()
        
        return render(request, 'update_student.html', {'form': form})


