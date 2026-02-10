from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Task, Category
from .forms import TaskForm

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='testuser', 
            password='testpass', 
            email='test@example.com'
            )
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Test Category")
        self.task = Task.objects.create(
            title="Test Task",
            due_date="2024-12-31",
            completed=False,
            category=self.category,
        )
        self.task2 = Task.objects.create(
            title="Completed Task",
            due_date="2024-10-31",
            completed=True,
            category=self.category,
        )

    def test_task_list_view_status_code(self):
        """GET the task list view returns 200 and uses the correct template."""
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_task_list_view_context_contains_tasks(self):
        """Task list view provides tasks in context."""
        response = self.client.get(reverse('tasks:index'))
        self.assertIn('to_do_tasks', response.context)
        self.assertIn('done_tasks', response.context)
        self.assertIn(self.task, response.context['to_do_tasks'])
        self.assertIn(self.task2, response.context['done_tasks'])

    def test_task_create_view_renders_form(self):
        """GET the create view renders the creation form."""
        response = self.client.get(reverse('tasks:index'))  # Assuming form is on index page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_create_view_post_creates_task(self):
        """POST to create view creates a task and redirects appropriately."""
        form_data = {
            'title': 'New Task',
            'due_date': '2024-11-30',
            'completed': False,
            'category': self.category.id,
        }
        response = self.client.post(reverse('tasks:index'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_invalid_task_creation_does_not_create_task(self):
        """POST with invalid data does not create a task and re-renders form."""
        form_data = {
            'title': '',  # Title is required, so this is invalid
            'due_date': '2024-11-30',
            'completed': False,
            'category': self.category.id,
        }
        response = self.client.post(reverse('tasks:index'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(Task.objects.filter(due_date='2024-11-30').exists())
