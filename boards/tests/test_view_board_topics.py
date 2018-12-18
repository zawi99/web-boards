from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board
from ..views import board_detail


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Random', description="Random stuff")

    def test_board_topics_view_success_status_code(self):
        url = reverse('board-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board-detail', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_view_resolve_board_topic_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_detail)

    def test_board_topics_view_contains_navigation_links(self):
        """
        An unauthorized user should not see the "new topic" link
        """
        home_url = reverse('home')
        board_topics_url = reverse('board-detail', kwargs={'pk': 1})
        new_topic_url = reverse('topic-new', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, f'href="{home_url}"')
        self.assertNotContains(response, f'href="{new_topic_url}"')
