import email
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        if 'delete_student' in request.POST:
            student_id = request.POST.get('delete_student')
            try:
                student = Student.objects.get(id=student_id)
                student.delete()
            except Student.DoesNotExist:
                pass
            return redirect('home')
            
        if 'filter' in request.POST:
            # Handle filter
            filter_course = request.POST.get('filter_course', '')
            filter_year = request.POST.get('filter_year', '')
            name_search = request.POST.get('name_search', '')
            
            students = Student.objects.all()
            
            if filter_course:
                students = students.filter(course=filter_course)
            if filter_year:
                students = students.filter(year_of_study=filter_year)
            if name_search:
                students = students.filter(name__icontains=name_search)
                
            students = students.order_by('-date_registered')
            
            # Get unique courses and years for filter dropdowns
            courses = Student.objects.values_list('course', flat=True).distinct()
            years = Student.objects.values_list('year_of_study', flat=True).distinct()
            
            return render(request, 'home.html', {
                'students': students,
                'courses': courses,
                'years': years,
                'selected_course': filter_course,
                'selected_year': filter_year,
                'name_search': name_search
            })
        else:
            # Handle student registration
            name = request.POST.get('name')
            student_id = request.POST.get('student_id')
            course = request.POST.get('course')
            year_of_study = request.POST.get('year_of_study')
            address = request.POST.get('address')

            try:
                student = Student.objects.create(
                    name=name,
                    student_id=student_id,
                    course=course,
                    year_of_study=year_of_study,
                    address=address
                )
                student.save()
            except Exception as e:
                students = Student.objects.all().order_by('-date_registered')
                courses = Student.objects.values_list('course', flat=True).distinct()
                years = Student.objects.values_list('year_of_study', flat=True).distinct()
                return render(request, 'home.html', {
                    'error': 'Student ID or email already exists',
                    'students': students,
                    'courses': courses,
                    'years': years
                })

    # Initial page load
    students = Student.objects.all().order_by('-date_registered')
    courses = Student.objects.values_list('course', flat=True).distinct()
    years = Student.objects.values_list('year_of_study', flat=True).distinct()
    return render(request, 'home.html', {
        'students': students,
        'courses': courses,
        'years': years
    })

def register(request):
    print("Register view called")
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1 == password2:
            try:
                user = User.objects.create_user(email=email, username=username, password=password1)
                user.save()
                return redirect('login')
            except:
                return render(request, 'register.html', {'error': 'Username already exists'})
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')