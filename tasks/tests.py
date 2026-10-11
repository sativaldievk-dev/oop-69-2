from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewsTest(TestCase):
    def test_task_list_shows_new_tasks_first(self):
        older = Task.objects.create(title='Old task', description='Old')
        newer = Task.objects.create(title='New task', description='New')

        response = self.client.get(reverse('tasks:task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['tasks'])[:2], [newer, older])

    def test_create_task_and_redirect_to_list(self):
        response = self.client.post(
            reverse('tasks:task_create'),
            {'title': 'New todo', 'description': 'Task description'},
        )

        self.assertRedirects(response, reverse('tasks:task_list'))
        self.assertTrue(Task.objects.filter(title='New todo').exists())

    def test_toggle_task_changes_status(self):
        task = Task.objects.create(title='Toggle me', completed=False)

        response = self.client.post(
            reverse('tasks:task_toggle', args=[task.pk]),
            {'next': reverse('tasks:task_list')},
        )

        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.assertRedirects(response, reverse('tasks:task_list'))
