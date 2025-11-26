from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()

class NoteViewSetTest(APITestCase):
    def setUp(self):
        # Create a primary user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token = Token.objects.create(user=self.user)
        
        # Create a second user to test data isolation
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.other_token = Token.objects.create(user=self.other_user)

        # Create a note belonging to the primary user
        self.note = Note.objects.create(
            title='My Note',
            content='Content of my note',
            user=self.user
        )

        # Create a note belonging to the other user
        self.other_note = Note.objects.create(
            title='Other Note',
            content='Content of other note',
            user=self.other_user
        )

        # Authenticate the primary user by adding the Token to the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # URLs
        self.list_url = reverse('note-list')
        self.detail_url = reverse('note-detail', kwargs={'pk': self.note.pk})

    def test_unauthenticated_access(self):
        """Test that unauthenticated requests are rejected."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_notes(self):
        """Test retrieving a list of notes for the authenticated user."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see 1 note (the one belonging to self.user)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'My Note')

    def test_retrieve_note(self):
        """Test retrieving a single note detail."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'My Note')

    def test_create_note(self):
        """Test creating a new note."""
        data = {
            'title': 'New Note',
            'content': 'New content'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 3) # 2 existing + 1 new
        self.assertEqual(Note.objects.get(title='New Note').user, self.user)

    def test_update_note(self):
        """Test updating an existing note (PATCH)."""
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')

    def test_delete_note(self):
        """Test deleting a note."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_user_cannot_access_other_users_note(self):
        """Test that a user cannot retrieve a note belonging to another user."""
        # Try to access the note belonging to 'other_user'
        other_note_url = reverse('note-detail', kwargs={'pk': self.other_note.pk})
        response = self.client.get(other_note_url)
        
        # Should return 404 because get_queryset filters it out
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_users_note(self):
        """Test that a user cannot update a note belonging to another user."""
        other_note_url = reverse('note-detail', kwargs={'pk': self.other_note.pk})
        data = {'title': 'Hacked Title'}
        response = self.client.patch(other_note_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_note.refresh_from_db()
        self.assertNotEqual(self.other_note.title, 'Hacked Title')