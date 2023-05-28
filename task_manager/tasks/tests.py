from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status

from .factories import TaskFactory

from django import test


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TaskTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='JohnCena',
            password='bingchilling'
        )
        self.client.force_login(self.user)

        self.status = {'name': 'sample_text'}
        self.client.post(reverse('status_create'), data=self.status)

        self.tasks = TaskFactory.create_batch(
            2,
            status=Status.objects.get(name=self.status['name']),
            executor=get_user_model().objects.get(id=self.user.id),
            assigned_by=get_user_model().objects.get(id=self.user.id),
        )

        self.task = TaskFactory.create_fake_task(
            status=Status.objects.get(name=self.status['name']).id,
            executor=get_user_model().objects.get(id=self.user.id).id,
            assigned_by=get_user_model().objects.get(id=self.user.id).id,
        )
        self.incorrect_task = TaskFactory.create_fake_task(
            status=Status.objects.get(name=self.status['name']).id,
            executor=self.tasks[-1].id + 1,
            assigned_by=get_user_model().objects.get(id=self.user.id).id,
        )
        self.id = self.tasks[0].id

    # testing tasks view
    def test_tasks_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Delete'))
        self.assertContains(response, _('Update'))
        for task in self.tasks:
            self.assertContains(response, task.name)
            self.assertContains(response, task.status)
            self.assertContains(response, task.executor)
            self.assertContains(response, task.assigned_by)

    def test_tasks_view_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    # testing task create view
    def test_task_create_get_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('task_create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_create_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.post(
            reverse('task_create'), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_create_get(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create'))

    def test_task_create_post_correct_code(self):
        response = self.client.post(reverse('task_create'), data=self.task)
        self.assertEqual(response.status_code, 302)

    def test_task_create_post_correct_content(self):
        response = self.client.post(
            reverse('task_create'), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Task created successfully!'))

    def test_task_create_post_incorrect(self):
        # duplicate task
        response = self.client.post(reverse('task_create'), data=self.task)
        response = self.client.post(
            reverse('task_create'), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('exists'))

        response = self.client.post(
            reverse('task_create'), data=self.incorrect_task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('required'))

    # testing task update view
    def test_task_update_get_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(
            reverse('task_update', args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_update_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.post(
            reverse('task_update', args=[self.id]), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_update_get(self):
        response = self.client.get(reverse('task_update', args=[self.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'/tasks/{self.id}/update/')

    def test_task_update_post_correct_code(self):
        response = self.client.post(
            reverse('task_update', args=[self.id]), data=self.task
        )
        self.assertEqual(response.status_code, 302)

    def test_task_update_post_correct_content(self):
        response = self.client.post(
            reverse('task_update', args=[self.id]), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Task updated successfully!'))

    def test_task_update_post_incorrect(self):
        self.client.post(reverse('task_create'), data=self.task, follow=True)
        response = self.client.post(
            reverse('task_update', args=[self.id]), data=self.task, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('exists'))

        response = self.client.post(
            reverse('task_update', args=[self.id]),
            data={'name': 'a' * 500},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('update'))

    # testing task delete view
    def test_task_delete_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(
            reverse('task_delete', args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_delete_get(self):
        response = self.client.get(
            reverse('task_delete', args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('delete'))
        self.assertContains(response, f'/tasks/{self.id}/delete/')

    def test_task_delete_post_correct_code(self):
        response = self.client.post(reverse('task_delete', args=[self.id]))
        self.assertEqual(response.status_code, 302)

    def test_task_delete_post_correct_content(self):
        response = self.client.post(
            reverse('task_delete', args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Task deleted successfully!'))
        self.assertNotContains(response, self.tasks[0].name)

    # testing permissions
    def test_task_update_get_in_progress(self):  # TODO
        assert True

    def test_task_delete_get_in_progress(self):  # TODO
        assert True

    def test_status_delete_connected_with_task(self):
        response = self.client.post(
            reverse('status_delete', args=[Status.objects.all()[0].id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            _('Status is connected with one or more tasks and cannot be deleted')  # noqa: E501
        )

    def test_user_delete_connected_with_task(self):
        response = self.client.post(
            reverse('user_delete', args=[User.objects.all()[0].id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            _('User has tasks and cannot be deleted')
        )

    def test_task_filters(self):
        assert True  # TODO
