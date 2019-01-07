from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board
from ..views import BoardListView


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Piwo', description='O piwku.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('boards:topic-list',
                                   kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{board_topics_url}"')
