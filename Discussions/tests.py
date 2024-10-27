from django.test import TestCase
from django.urls import reverse
from .models import DiscussionThread, DiscussionComment
from .forms import DiscussionThreadForm, DiscussionCommentForm

# Create your tests here.

class DiscussionModelTest(TestCase):
    def test_create_thread(self):
        thread = DiscussionThread.objects.create(
            title='Test Thread',
            content='This is a test thread content.',
            product_id=1
        )
        self.assertEqual(thread.title, 'Test Thread')
        self.assertEqual(thread.content, 'This is a test thread content.')

    def test_create_comment(self):
        thread = DiscussionThread.objects.create(
            title='Test Thread',
            content='This is a test thread content.',
            product_id=1
        )
        comment = DiscussionComment.objects.create(
            thread=thread,
            content='This is a test comment.'
        )
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.thread, thread)

class DiscussionFormTest(TestCase):
    def test_valid_thread_form(self):
        form_data = {'title': 'Test Thread', 'content': 'This is a test thread content.'}
        form = DiscussionThreadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_thread_form(self):
        form_data = {'title': '', 'content': 'This is a test thread content.'}
        form = DiscussionThreadForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_comment_form(self):
        form_data = {'content': 'This is a test comment.'}
        form = DiscussionCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form_data = {'content': ''}
        form = DiscussionCommentForm(data=form_data)
        self.assertFalse(form.is_valid())

class DiscussionViewsTest(TestCase):
    def setUp(self):
        self.thread = DiscussionThread.objects.create(
            title='Test Thread',
            content='This is a test thread content.',
            product_id=1
        )


    def test_add_comment_view(self):
        response = self.client.post(reverse('Discussions:add_comment', args=[self.thread.id]), {
            'content': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a tests comment.')
