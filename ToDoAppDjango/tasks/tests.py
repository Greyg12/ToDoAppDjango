from django.test import TestCase
from django.urls import reverse
from tasks.models import Task

class TaskModelTest(TestCase):
    def test_create_task(self):
        # Test creating a Task instance
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            progress=50,
            completed_at=None
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.progress, 50)
        self.assertIsNone(task.completed_at)

class TaskViewTest(TestCase):
    def setUp(self):
        # Create a sample task for view tests
        self.task = Task.objects.create(
            title="Sample Task",
            description="Sample description",
            progress=20,
            completed_at=None
        )

    def test_task_list_view(self):
        # Test that the task list view returns a 200 response and contains the task
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Task")

    def test_create_task_view(self):
        # Test creating a new task via the view
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'New description',
            'progress': 10,
            'completed_at': ''
        })
        self.assertEqual(response.status_code, 200)  # Should return with error (missing completed_at)
        # Now test with completed_at
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'New description',
            'progress': 10,
            'completed_at': '2025-05-16T12:00'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())
