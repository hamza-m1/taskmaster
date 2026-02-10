from django.test import TestCase
from .models import Category
from .forms import TaskForm

class formsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_task_form_valid_data(self):
        """TaskForm is valid with correct data."""
        form_data = {
            'title': 'Test Task',
            'due_date': '2024-12-31',
            'completed': False,
            'category': self.category.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_data(self):
        """TaskForm is invalid with missing required fields."""
        form_data = {
            'title': '',  # Title is required
            'due_date': '',  # Due date is required
            'completed': False,
            'category': self.category.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('due_date', form.errors)

    def test_task_form_category_field(self):
        """TaskForm category field is a ModelChoiceField with correct queryset."""
        form = TaskForm()
        self.assertIn('category', form.fields)
        self.assertEqual(form.fields['category'].queryset.count(), 1)
        self.assertEqual(form.fields['category'].queryset.first(), self.category)

    def test_task_form_due_date_field(self):
        """TaskForm due_date field is a DateField."""
        form = TaskForm()
        self.assertIn('due_date', form.fields)
        self.assertEqual(form.fields['due_date'].__class__.__name__, 'DateField')
    

    
    def test_task_form_title_field(self):
        """TaskForm title field is a CharField with max_length 100."""
        form = TaskForm()
        self.assertIn('title', form.fields)
        self.assertEqual(form.fields['title'].__class__.__name__, 'CharField')
        self.assertEqual(form.fields['title'].max_length, 100)
    
    def test_task_form_invalid_category(self):
        """TaskForm is invalid if category does not exist."""
        form_data = {
            'title': 'Test Task',
            'due_date': '2024-12-31',
            'completed': False,
            'category': 999,  # Non-existent category ID
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_task_form_title_too_long(self):
        """TaskForm is invalid if title exceeds max_length."""
        long_title = "A" * 101  # 101 characters
        form_data = {
            'title': long_title,
            'due_date': '2024-12-31',
            'completed': False,
            'category': self.category.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_task_form_invalid_due_date(self):
        """TaskForm is invalid if due_date is not a valid date."""
        form_data = {
            'title': 'Test Task',
            'due_date': 'invalid-date',  # Invalid date format
            'completed': False,
            'category': self.category.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)
    
    def test_task_form_missing_category(self):
        """TaskForm is invalid if category is missing."""
        form_data = {
            'title': 'Test Task',
            'due_date': '2024-12-31',
            'completed': False,
            # 'category' is missing
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
    
    def test_task_form_missing_completed(self):
        """TaskForm is valid if completed field is missing (should default to False)."""
        form_data = {
            'title': 'Test Task',
            'due_date': '2024-12-31',
            # 'completed' is missing
            'category': self.category.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertFalse(task.completed)  # Should default to False if not provided
    
    def test_task_form_missing_due_date(self):
        """TaskForm is invalid if due_date is missing."""
        form_data = {
            'title': 'Test Task',
            # 'due_date' is missing
            'completed': False,
            'category': self.category.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)