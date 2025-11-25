from django.test import TestCase
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()

class NoteModelTest(TestCase):
    def setUp(self):
        # Create a user to associate with the note
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        # Create a sample note
        self.note = Note.objects.create(
            title='Test Note',
            content='This is the content of the test note.',
            user=self.user
        )

    def test_note_creation(self):
        """Test that the note is correctly created with the provided attributes."""
        self.assertTrue(isinstance(self.note, Note))
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.content, 'This is the content of the test note.')
        self.assertEqual(self.note.user, self.user)
        
        # created_at is automatically generated, so we just check it is not None
        self.assertIsNotNone(self.note.created_at)

    def test_note_str_representation(self):
        """Test that the __str__ method returns the note title."""
        self.assertEqual(str(self.note), 'Test Note')