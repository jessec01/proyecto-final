from django.test import TestCase
from .models import User


class UserManagerTests(TestCase):
    def test_create_user_hashes_password_and_sets_fields(self):
        u = User.objects.create_user(
            email='test@example.com',
            password='P@ssw0rd1',
            username='testuser',
            first_name='Ana',
            last_name='B',
            phone='+584123456789',
        )

        # password must be hashed and check_password should return True
        u.full_clean()  # validate the model instance
        self.assertTrue(u.check_password('P@ssw0rd1'))
        self.assertNotEqual(u.password, 'P@ssw0rd1')

        # basic fields
        self.assertEqual(u.email, 'test@example.com')
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.first_name, 'Ana')
        self.assertEqual(u.last_name, 'B')
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_superuser)

    def test_create_superuser_sets_flags_and_password(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='AdminP@ss1',
            email='admin@example.com',
            first_name='Admin',
            last_name='I',
            phone='+584121234567',
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password('AdminP@ss1'))

# Create your tests here.
