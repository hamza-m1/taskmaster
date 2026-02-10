from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import date
from .models import Task, Category


class TaskModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.task = Task.objects.create(
            title="Sample Task",
            due_date=date.today(),
            completed=False,
            category=self.category,
        )

    def test_task_creation(self):
        """A Task can be created with a title, due date, completed status, and category."""
        self.assertEqual(self.task.title, "Sample Task")
        self.assertEqual(self.task.due_date, date.today())
        self.assertFalse(self.task.completed)
        self.assertEqual(self.task.category, self.category)

    def test_str_returns_title(self):
        """__str__ returns the task title."""
        self.assertEqual(str(self.task), "Sample Task")

    def test_default_completed_is_false(self):
        """The `completed` field defaults to False."""
        self.assertFalse(self.task.completed)

    def test_due_date_required(self):
        """`due_date` is required and stores a date."""
        self.assertIsNotNone(self.task.due_date)
        self.assertIsInstance(self.task.due_date, date)

    def test_category_relationship(self):
        """Task has a ForeignKey relationship to Category."""
        self.assertEqual(self.task.category, self.category)

    def test_title_max_length(self):
        """The `title` field enforces max_length (100)."""
        self.assertLessEqual(len(self.task.title), 100)
 
    # generate a unite test that checks for an error if the title is longer then 100 characters
    def test_title_max_length_error(self):
        """An error is raised if the `title` field exceeds max_length."""
        long_title = "A" * 101  # 101 characters
        with self.assertRaises(ValidationError):
            Task.objects.create(
                title=long_title,
                due_date=date.today(),
                completed=False,
                category=self.category,
            )
