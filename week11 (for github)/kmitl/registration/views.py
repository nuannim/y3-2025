from django.shortcuts import render, redirect
from registration.models import *
from django.db.models import Value
from django.db.models.functions import Concat
from registration.forms import *
from django.db import transaction

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
        form = StudentForm(request.POST, request.FILES)
        
        print(form.is_valid())
        print(form.errors)

        try:
            with transaction.atomic():

                if form.is_valid():
                    form.save()

                    email = form.cleaned_data['email']
                    phone_number = form.cleaned_data['phone_number']
                    address = form.cleaned_data['address']
                    image = form.cleaned_data['image']

                    print('email:', email)
                    print('phone_number:', phone_number)
                    print('address:', address)
                    print('image:', image)

                    # f = Faculty.objects.get(pk=int(faculty.id))


                    # s = Student.objects.create(
                    #     student_id = student_id,
                    #     first_name = first_name,
                    #     last_name = last_name,
                    #     faculty = f
                    # )
                    # s.enrolled_sections.set(enrolled_sections)

                    s = Student.objects.get(student_id=form.cleaned_data['student_id'])

                    if email and phone_number:
                        StudentProfile.objects.create(
                            student = s,
                            email = email,
                            phone_number = phone_number,
                            address = address,
                            image=image
                        )
                        return redirect('index')
                    else:
                        raise ValueError("Email and phone number are required.")
                else:
                    raise ValueError("Form is not valid.")

                # return render(request, 'create_student.html', {'form': form})
        except Exception as e:
            print(e)






def updatestudent(request, student_id):
    student = Student.objects.get(student_id=student_id)
    studentprofile = student.studentprofile

    if request.method == 'GET':

        # student = Student.objects.get(student_id=student_id)
        # faculty = student.faculty 
        # first_name = student.first_name
        # last_name = student.last_name
        # email = student.studentprofile.email
        # phone_number = student.studentprofile.phone_number
        # address = student.studentprofile.address
        # enrolled_sections = student.enrolled_sections.all()

        # image = student.studentprofile.image

        

        # data = {
        #     'student_id': student_id,
        #     'faculty': faculty,
        #     'first_name': first_name,
        #     'last_name': last_name,
        #     'email': email,
        #     'phone_number': phone_number,
        #     'address': address,
        #     'enrolled_sections': enrolled_sections,
        #     'image': image
        # }

        # form = StudentForm(instance=data)

        # return render(
        #     request,
        #     'update_student.html',
        #     context = {
        #         'form': form
        #     }
        # )

        form = StudentForm(instance=studentprofile, initial={
            'student_id': student.student_id,
            'faculty': student.faculty,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'enrolled_sections': student.enrolled_sections.all(),
        })

        return render(request, 'update_student.html', {'form': form, 'student': student})



    elif request.method == 'POST':

        # form = StudentForm(request.POST)
        form = StudentForm(request.POST, request.FILES, instance=studentprofile)

        if form.is_valid():
            # form.save()

            student_id = form.cleaned_data['student_id']
            faculty = form.cleaned_data['faculty']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            # section_ids = form.cleaned_data['section_ids']
            enrolled_sections = form.cleaned_data['enrolled_sections']

            image = form.cleaned_data['image']

            print('=====')
            print('student_id:', student_id)
            print('faculty:', faculty)
            print('first_name:', first_name)
            print('last_name:', last_name)
            print('email:', email)
            print('phone_number:', phone_number)
            print('address:', address)
            print('enrolled_sections:', enrolled_sections)
            print('image:', image)

            # f = Faculty.objects.get(pk=int(faculty_id))
            f = Faculty.objects.get(pk=int(faculty.id))

            s = Student.objects.get(student_id=student_id)
            s.first_name = first_name
            s.last_name = last_name
            s.faculty = f
            s.enrolled_sections.set(enrolled_sections)
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
            sp.image = image
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


def createcourse(request):
    professors = Professor.objects.all()

    if request.method == 'GET':
        # form = CourseAndSectionForm()
        course = CourseForm()
        section = SectionForm()

        return render(request, 'create_course.html', context= {
            'professors': professors,
            'course': course,
            'section': section
        })

    elif request.method == "POST":
        # form = CourseAndSectionForm(request.POST)
        course = CourseForm(request.POST)
        section = SectionForm(request.POST)
        
        print(course.is_valid())
        print(course.errors)
        print(section.is_valid())
        if course.is_valid() and section.is_valid():
            c = course.save()
            s = section.save(commit=False)
            s.course = c
            s.save()
            return redirect("course")
        course = CourseForm()
        section = SectionForm()
        context = {"course": course, "section": section}

        return render(request, "create_course.html", context)
    
def updatecourse(request, course_id):
    if request.method == 'GET':
        c = Course.objects.get(pk=course_id)
        s = Section.objects.filter(course=c).first()
        course = CourseForm(instance=c)
        section = SectionForm(instance=s)

        return render(request, "create_course.html", {"course": course, "section": section})
    
    elif request.method == 'POST':
        c = Course.objects.get(pk=course_id)
        s = Section.objects.filter(course=c).first()
        
        if not s:
            s = Section(course=c)
        
        course = CourseForm(request.POST, instance=c) 
        section = SectionForm(request.POST, instance=s)

        if course.is_valid() and section.is_valid():
            c = course.save()
            s = section.save(commit=False)
            s.course = c
            s.save()

            return redirect("course")
        return render(request, 'create_course.html', {'course': course, 'section': section})
