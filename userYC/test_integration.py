from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.db import transaction
from unittest.mock import patch
from .views import SaveUserView


class UserRegistrationIntegrationTests(TestCase):
    """Integration-style tests for the user registration endpoint.

    These tests use DRF's test utilities and call the view callable
    directly via `APIRequestFactory` so they exercise request parsing,
    serializer validation and the view exception handling.

    Exceptions that the view is expected to handle (and that tests cover):
    - `rest_framework.serializers.ValidationError` => HTTP 400
    - `django.db.transaction.TransactionManagementError` => HTTP 500
    - Model/DB integrity errors will surface as 400/500 depending on
      how the serializer/save raises them (e.g. IntegrityError)
    - Other DB errors (psycopg2.OperationalError) are not caught by the
      view and will error the test runner (we do not simulate them here).
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SaveUserView.as_view()

    def test_register_success_returns_201(self):
        data = {
            "email": "inttest@example.com",
            "password": "StrongP@ss1",
            "confirmation_password": "StrongP@ss1",
            "username": "intuser",
            "first_name": "Anna",   # 4 letras -> válido
            "last_name": "Test",
            "phone": "+584121234567",
        }
        request = self.factory.post("/api/save-user/", data, format="json")
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("email"), data["email"])
        self.assertEqual(response.data.get("username"), data["username"])

    def test_register_invalid_phone_returns_400(self):
        data = {
            "email": "badphone@example.com",
            "password": "StrongP@ss1",
            "confirmation_password": "StrongP@ss1",
            "username": "badphone",
            "first_name": "Anna",
            "last_name": "Phone",
            # invalid / too short number
            "phone": "+34123",
        }
        request = self.factory.post("/api/save-user/", data, format="json")
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        # response.data['error'] contiene el dict de errores como string; parsearlo
        err_text = response.data.get("error", "")
        self.assertIn("phone", err_text)

    def test_register_serializer_raises_transaction_error_returns_500(self):
        data = {
            "email": "dberror@example.com",
            "password": "StrongP@ss1",
            "confirmation_password": "StrongP@ss1",
            "username": "dberror",
            "first_name": "Anna",
            "last_name": "Error",
            "phone": "+584121234567",
        }

        with patch("userYC.views.UserYCSerializer.save", side_effect=transaction.TransactionManagementError("db tx")):
            request = self.factory.post("/api/save-user/", data, format="json")
            response = self.view(request)
            self.assertEqual(response.status_code, 500)
            self.assertIn("Database transaction error", str(response.data))
