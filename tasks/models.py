from django.db import models

# a model for Category to store category names
# category names are unique and no longer than 50 characters

class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name


# a model for Task to store task title, due date,
# task completed status, and category.
# task title is no longer than 100 characters,
# completed status is False by default
# and category is a foreign key to Category.

class Task(models.Model):
	title = models.CharField(max_length=100)
	due_date = models.DateField()
	completed = models.BooleanField(default=False)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	

