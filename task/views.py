from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from . models import *
from . forms import *
from . decorators import unauthenticated_user, allowed_users, admin_only

import sweetify
# Create your views here.

def home(request):

    form = SuscribersForm()
    form1 = ContactForm()

    if request.method == 'POST':
        try:
            if request.POST['name']:
                form1 = ContactForm(request.POST)
                if form1.is_valid():
                    form1.save()
                    sweetify.success(request, title='Message Received',
                                     text='Thank you for contacting us. We\'ll get back to you shortly.',
                                     icon='success',
                                     button='Ok', extra_tags='contact')
                    return redirect('/')

                else:
                    sweetify.error(request, title='Error',
                                   text='An error occured while trying to send your message.\nPlease try again.\n We sincerely apologize for any inconveniences.',
                                   icon='error', button='Ok', extra_tags='contact')
                    return redirect('/')

        except:
            form = SuscribersForm(request.POST)
            if form.is_valid():
                form.save()
                sweetify.success(request, title='Email Received',
                                 text='You have successfully suscribed to our newsletter',
                                 icon='success', button='Ok', extra_tags='newsletter')
                return redirect('/')
            else:
                sweetify.error(request, title='Error',
                               text='An error occured while trying to send in your email address.\nPlease try again.\n We sincerely apologize for any inconveniences.',
                               icon='error', button='Ok', extra_tags='contact')
                return redirect('/')


    context = {'form':form, 'form1':form1}

    return render(request, 'task/home.html', context)

def faqs(request):

    form = SuscribersForm()

    if request.method == 'POST':
        form = SuscribersForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, title='Email Received', text='You have successfully suscribed to our newsletter', icon='success', button='Ok', extra_tags='newsletter')
            return redirect('faqs')
        else:
            sweetify.error(request, title='Error',
                           text='An error occured while trying to send your email address.\nPlease try again.\n We sincerely apologize for any inconveniences.',
                           icon='error', button='Ok', extra_tags='contact')
            return redirect('faqs')


    context = {'form':form}
    return render(request,'task/faqs.html', context)

@unauthenticated_user
def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            sweetify.success(request, title='Success!', text='Account was created for ' + username, icon='success', button='Ok')

            return redirect('login')

    context = {'form':form}


    return render(request, 'task/reg.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            sweetify.info(request, title='Warning', text='Username OR password is incorrect', icon='warning', button='Ok')
    context = {}
    return render(request, 'task/log.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def dashboard(request):

    tasks = AdminTask.objects.all().order_by('-date_created')
    workers = Worker.objects.all().order_by('-date_created')

    taskitems = TaskItem.objects.all().order_by('-date_performed')

    total_tasks = tasks.count()
    tasks_attempted = taskitems.count()
    verified = taskitems.filter(status='Verified').count()
    pending = taskitems.filter(status='Pending').count()

    context = {'tasks':tasks, 'workers': workers, 'taskitems': taskitems, 'total_tasks':total_tasks, 'tasks_attempted': tasks_attempted, 'verified': verified, 'pending': pending}
    return render(request, 'task/dashboard.html', context)

def tasks(request):

    tasks = AdminTask.objects.all().order_by('-date_created')

    context = {'tasks':tasks}
    return render(request, 'task/tasks.html', context)

@login_required(login_url='login')
@admin_only
def worker(request, pk_test):
    worker = Worker.objects.get(id=pk_test)

    tasks = worker.admintask_set.all()
    taskitems = worker.taskitem_set.all()

    task_count = tasks.count()
    verified = taskitems.filter(status='Verified').count()
    pending = taskitems.filter(status='Pending').count()

    context = {'worker':worker, 'tasks': tasks, 'taskitems':taskitems, 'task_count': task_count, 'verified': verified, 'pending': pending}
    return render(request, 'task/workers_id.html', context)

def save_task_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            tasks = AdminTask.objects.all()
            data['html_task_list'] = render_to_string('task/partial_task_list.html', {
                'tasks': tasks
            })
        else:
            data['form_is_valid'] = False

    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
@admin_only
def createTask(request):

    if request.method == 'POST':
        form = AdminTaskForm(request.POST)
    else:
        form = AdminTaskForm()

    return save_task_form(request, form, 'task/partial_task_create.html')

def updateTask(request, pk):

    task = get_object_or_404(AdminTask, id=pk)

    if request.method == 'POST':
        form = AdminTaskForm(request.POST, instance=task)

    else:
        form = AdminTaskForm(instance=task)
    return save_task_form(request, form, 'task/partial_task_update.html')

def deleteTask(request, pk):
    task = get_object_or_404(AdminTask, id=pk)
    data = dict()
    if request.method == 'POST':
        task.delete()

        data['form_is_valid'] = True
        tasks = AdminTask.objects.all()
        data['html_task_list'] = render_to_string('task/partial_task_list.html', {'tasks':tasks})
    else:
        context = {'task':task}
        data['html_form'] = render_to_string('task/partial_task_delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
def userPage(request):

    tasks = request.user.worker.admintask_set.all()
    taskitems = request.user.worker.taskitem_set.all()

    total_tasks = tasks.count()
    verified = taskitems.filter(status='Verified').count()
    pending = taskitems.filter(status='Pending').count()

    context = {'tasks':tasks, 'taskitems': taskitems, 'total_tasks': total_tasks, 'verified': verified, 'pending': pending}
    return render(request, 'task/userpage.html', context)
