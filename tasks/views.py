from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

# Create your views here.
def index(request):
	"""
	A view to display tasks to do and completed tasks 
	with the tasks due soonest at the top 
	"""
	to_do_tasks = Task.objects.filter(completed=False).order_by('due_date')
	done_tasks = Task.objects.filter(completed=True).order_by('due_date')

	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('tasks:index')
	else:
		form = TaskForm()
	
	context = {
		'to_do_tasks': to_do_tasks,
		'done_tasks': done_tasks,
		'form': form,
	}
	return render(request, 'tasks/index.html', context)