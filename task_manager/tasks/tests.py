from django.test import TestCase
from .factories import TaskFactory
from django.utils.translation import gettext as _
from django.urls import reverse


class TaskTest(TestCase):

    def setUp(self):
        self.tasks = TaskFactory.create_batch(2)
        self.task = {
            'name': 'sample_text'
        }
        self.id = self.tasks[0].id
        self.user = {
            'password1': 'PswrdNmrc1',
            'password2': 'PswrdNmrc1',
            'first_name': 'John',
            'last_name': 'Cena',
            'username': 'bingchilling'
        }
        self.login_data = {
            'password': self.user['password1'],
            'username': self.user['username']
        }
        self.client.post(reverse('user_create'), data=self.user)
        self.client.post(reverse('user_login'), data=self.login_data)

    # testing tasks view
    def test_tasks_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.task_code, 200)
        for task in self.tasks:
            self.assertContains(response, task.name)

    def test_tasks_view_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Password'))

    # testing task create view
    def test_task_create_get_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('task_create'), follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_create_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.post(reverse('task_create'), data=self.task, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_create_get(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Create'))

    def test_task_create_post_correct_code(self):
        response = self.client.post(reverse('task_create'), data=self.task)
        self.assertEqual(response.task_code, 302)

    def test_task_create_post_correct_content(self):
        response = self.client.post(reverse('task_create'), data=self.task, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Task created successfully!'))

    def test_task_create_post_incorrect(self):
        response = self.client.post(reverse('task_create'), data=self.task)
        response = self.client.post(reverse('task_create'), data=self.task, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('exists'))

        response = self.client.post(reverse('task_create'), data={'name': 'a'*500}, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Create'))


    # testing task update view
    def test_task_update_get_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('task_update', args=[self.id]), follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_update_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.post(reverse('task_update', args=[self.id]), data=self.task, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_update_get(self):
        response = self.client.get(reverse('task_update', args=[self.id]))
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, f'/tasks/{self.id}/update/')

    def test_task_update_get_in_progress(self):  # TODO
        assert True

    def test_task_update_post_correct_code(self):
        response = self.client.post(reverse('task_update', args=[self.id]), data=self.task)
        self.assertEqual(response.task_code, 302)

    def test_task_update_post_correct_content(self):
        response = self.client.post(reverse('task_update', args=[self.id]), data=self.task, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Task updated successfully!'))

    def test_task_update_post_incorrect(self):
        self.client.post(reverse('task_create'), data=self.task, follow=True)
        response = self.client.post(reverse('task_update', args=[self.id]), data=self.task, follow=True)

        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('exists'))

        response = self.client.post(reverse('task_update', args=[self.id]), data={'name': 'a'*500}, follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('update'))

    # testing task delete view
    def test_task_delete_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('task_delete', args=[self.id]), follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Password'))

    def test_task_delete_get(self):
        response = self.client.get(reverse('task_delete', args=[self.id]), follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('delete'))
        self.assertContains(response, f'/tasks/{self.id}/delete/')

    def test_task_delete_get_in_progress(self):  # TODO
        assert True

    def test_task_delete_post_correct_code(self):
        response = self.client.post(reverse('task_delete', args=[self.id]))
        self.assertEqual(response.task_code, 302)

    def test_task_delete_post_correct_content(self):
        response = self.client.post(reverse('task_delete', args=[self.id]), follow=True)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, _('Task deleted successfully!'))
        self.assertNotContains(response, self.tasks[0].name)
