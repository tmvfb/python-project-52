from django import test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .factories import TaskFactory


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TaskTest(TestCase):
    def setUp(self):
        # simulate user login
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="JohnCena", password="bingchilling"
        )
        self.client.force_login(self.user)

        # create status
        self.status = {"name": "sample_text"}
        self.client.post(reverse("status_create"), data=self.status)

        # create labels
        self.label_1 = {"name": "sample_label_1"}
        self.label_2 = {"name": "sample_label_2"}
        self.client.post(reverse("label_create"), data=self.label_1)
        self.client.post(reverse("label_create"), data=self.label_2)

        # create tasks
        self.tasks = TaskFactory.create_batch(
            2,
            status=Status.objects.get(name=self.status["name"]),
            executor=get_user_model().objects.get(id=self.user.id),
            assigned_by=get_user_model().objects.get(id=self.user.id),
            labels=list(Label.objects.all()),  # all labels
        )
        # this task does not have executor and contains only 1st label
        self.task = TaskFactory.create_fake_task(
            status=Status.objects.get(name=self.status["name"]).id,
            assigned_by=get_user_model().objects.get(id=self.user.id).id,
            labels=[Label.objects.first().id],  # only 1st label
        )
        # this task does not have executor and contains both labels
        self.another_task = TaskFactory.create_fake_task(
            status=Status.objects.get(name=self.status["name"]).id,
            assigned_by=get_user_model().objects.get(id=self.user.id).id,
            labels=list(
                Label.objects.values_list("id", flat=True)
            ),  # all lbls
        )
        # this task has no author and no status
        self.incorrect_task = TaskFactory.create_fake_task(
            status="",
        )

        # some vars to avoid magic numbers later
        self.task_1_id = self.tasks[0].id
        self.label_1_id = 1
        self.label_2_id = 2
        self.status_id = 1
        self.user_id = 1

    # testing tasks view
    def test_tasks_view(self):
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Delete"))
        self.assertContains(response, _("Update"))
        for task in self.tasks:
            self.assertContains(response, task.name)
            self.assertContains(response, task.status)
            self.assertContains(response, task.executor)
            self.assertContains(response, task.assigned_by)

    def test_tasks_view_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(reverse("tasks"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    # testing task create view
    def test_task_create_get_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(reverse("task_create"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_task_create_post_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.post(
            reverse("task_create"), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_task_create_get(self):
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Create"))

    def test_task_create_post_correct_code(self):
        response = self.client.post(reverse("task_create"), data=self.task)
        self.assertEqual(response.status_code, 302)

    def test_task_create_post_correct_content(self):
        response = self.client.post(
            reverse("task_create"), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Task created successfully!"))

    def test_task_create_post_incorrect(self):
        # duplicate task
        response = self.client.post(reverse("task_create"), data=self.task)
        response = self.client.post(
            reverse("task_create"), data=self.task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("exists"))

        response = self.client.post(
            reverse("task_create"), data=self.incorrect_task, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("required"))

    # testing task update view
    def test_task_update_get_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(
            reverse("task_update", args=[self.task_1_id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_task_update_post_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.post(
            reverse("task_update", args=[self.task_1_id]),
            data=self.task,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_task_update_get(self):
        response = self.client.get(
            reverse("task_update", args=[self.task_1_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"/tasks/{self.task_1_id}/update/")

    def test_task_update_post_correct_code(self):
        response = self.client.post(
            reverse("task_update", args=[self.task_1_id]), data=self.task
        )
        self.assertEqual(response.status_code, 302)

    def test_task_update_post_correct_content(self):
        response = self.client.post(
            reverse("task_update", args=[self.task_1_id]),
            data=self.task,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Task updated successfully!"))

    def test_task_update_post_incorrect(self):
        self.client.post(reverse("task_create"), data=self.task, follow=True)
        response = self.client.post(
            reverse("task_update", args=[self.task_1_id]),
            data=self.task,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("exists"))

        response = self.client.post(
            reverse("task_update", args=[self.task_1_id]),
            data={"name": "a" * 500},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Update"))

    # testing task delete view
    def test_task_delete_post_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(
            reverse("task_delete", args=[self.task_1_id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_task_delete_get(self):
        response = self.client.get(
            reverse("task_delete", args=[self.task_1_id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("delete"))
        self.assertContains(response, f"/tasks/{self.task_1_id}/delete/")

    def test_task_delete_post_correct_code(self):
        response = self.client.post(
            reverse("task_delete", args=[self.task_1_id])
        )
        self.assertEqual(response.status_code, 302)

    def test_task_delete_post_correct_content(self):
        response = self.client.post(
            reverse("task_delete", args=[self.task_1_id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Task deleted successfully!"))
        self.assertNotContains(response, self.tasks[0].name)

    # testing tasks show view
    def test_task_show_view(self):
        response = self.client.get(reverse("task_show", args=[self.task_1_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[0].description)
        for label in self.tasks[0].labels.all():
            self.assertContains(response, label)
        self.assertContains(response, _("Update"))

    # testing permissions
    def test_label_delete_connected_with_task(self):
        response = self.client.post(
            reverse("label_delete", args=[Label.objects.all()[0].id]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            _("Label is connected with one or more tasks and cannot be deleted"),  # noqa: E501
        )

    def test_status_delete_connected_with_task(self):
        response = self.client.post(
            reverse("status_delete", args=[Status.objects.all()[0].id]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            _("Status is connected with one or more tasks and cannot be deleted"),  # noqa: E501
        )

    def test_user_delete_connected_with_task(self):
        response = self.client.post(
            reverse("user_delete", args=[User.objects.all()[0].id]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, _("User has tasks and cannot be deleted")
        )

    # testing filters
    def test_status_filter(self):
        self.client.post(reverse("task_create"), data=self.task, follow=True)
        response = self.client.get(
            reverse("tasks"), {"status": self.status_id}, follow=True
        )
        self.assertContains(response, self.task["name"])
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[1].name)

    def test_executor_filter(self):
        self.client.post(reverse("task_create"), data=self.task, follow=True)
        response = self.client.get(
            reverse("tasks"), {"executor": self.user_id}, follow=True
        )
        self.assertNotContains(response, self.task["name"])
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[1].name)

    def test_label_filter(self):
        self.client.post(reverse("task_create"), data=self.task, follow=True)
        response = self.client.get(
            reverse("tasks"), {"labels": self.label_2_id}, follow=True
        )
        self.assertNotContains(response, self.task["name"])
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[1].name)

    def test_is_mine_filter(self):
        self.client.post(reverse("task_create"), data=self.task, follow=True)
        response = self.client.get(
            reverse("tasks"), {"mine": "on"}, follow=True
        )
        self.assertContains(response, self.task["name"])
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[1].name)
        self.assertContains(response, "checked")

    def test_multiple_filters(self):
        self.client.post(reverse("task_create"), data=self.task, follow=True)
        self.client.post(
            reverse("task_create"), data=self.another_task, follow=True
        )
        response = self.client.get(
            reverse("tasks"), {"labels": self.label_2_id}, follow=True
        )
        self.assertNotContains(response, self.task["name"])
        self.assertContains(response, self.another_task["name"])
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[1].name)

        response = self.client.get(
            reverse("tasks"), {"executor": self.user_id}, follow=True
        )
        self.assertNotContains(response, self.task["name"])
        self.assertNotContains(response, self.another_task["name"])
        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[1].name)
