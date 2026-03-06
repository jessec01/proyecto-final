from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.db import transaction
from unittest.mock import patch
from .views import ReadDashboardInitialConfigView
from userYC.models import User

class CenterAdminMegaTransactionIntegrationTests(TestCase):
    """Integration-style tests for the center administrator initial config endpoint.
    
    This tests the mega-transaction that creates multiple related models 
    (Center Administrator, Center, Rules, Packages, Policy, Promotion, ClassYoga).
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ReadDashboardInitialConfigView.as_view({'post': 'procesar_cadena'})
        self.user = User.objects.create_user(
            username="testadmin",
            first_name="Test",
            last_name="Admin",
            phone="+584121234567",
            email="testadmin@example.com",
            password="StrongPassword123",
            is_center_administrator=True
        )
        self.valid_payload = {
            "center": {
                "code": "YOGACEN123",
                "name": "Yoga Center Name",
                "address": "123 Yoga Street test",
                "phone": "+584121234567",
                "email": "yogacenter@example.com",
                "hours_of_operation": {
                    "days": "Monday, Tuesday, Wednesday",
                    "start_time": "08:00",
                    "end_time": "20:00"
                },
                "description": "Yoga Center Description test"
            },
            "center_administrator": {
                "role": "Director testing",
                "experience_years": 5
            },
            "rules": {
                "name": "General Rule",
                "description": "General Description testing",
                "operator": ">",
                "value": "0",
                "active": True,
                "type_rule": "package_rule"
            },
            "packages": {
                "name": "Basic Package",
                "description": "Basic Package Desc",
                "price": 29.99,
                "duration": {"months": 1},
                "level_package": "beginner",
                "category": "monthly",
                "stackclass": "class"
            },
            "promotion": {
                "name": "New Year Promo",
                "description": "Promo description test",
                "discount_type": "percentage",
                "discount_value": 15,
                "active": True
            },
            "policy": {
                "is_refundable": True,
                "is_transferable": False,
                "is_discountable": True,
                "is_acumulative": False,
                "is_active_suspension": False
            },
            "classyoga": {
                "name": "Hatha Yoga test",
                "description": "Hatha Yoga Description length",
                "category": "Hatha Category",
                "schedules": {
                    "days": ["Monday", "Wednesday"],
                    "hour_start": "09:00",
                    "hour_end": "10:00",
                    "modality": "in-person"
                },
                "instructor": 1,
                "center": 1
            }
        }

    @patch("center_administration.serializer.CenterAdminConfiginitialSerializer.is_valid", return_value=True)
    @patch("center_administration.serializer.CenterAdminConfiginitialSerializer.save")
    def test_procesar_cadena_success_returns_201(self, mock_save, mock_is_valid):
        mock_save.return_value = self.user.centeradministrator if hasattr(self.user, 'centeradministrator') else None
        request = self.factory.post("/api/dashboard/config/", self.valid_payload, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("mensaje"), "Proceso completado exitosamente")

    def test_procesar_cadena_invalid_center_data_returns_400(self):
        # Mutate the payload to have an invalid email and a missing required code
        invalid_payload = self.valid_payload.copy()
        invalid_payload["center"]["email"] = "invalid-email"
        invalid_payload["center"].pop("code", None)
        
        request = self.factory.post("/api/dashboard/config/", invalid_payload, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        
        self.assertEqual(response.status_code, 400)
        # Should contain validation errors for "center"
        self.assertIn("center", str(response.data))

    def test_procesar_cadena_raises_transaction_error_returns_400(self):
        # Simulate a transaction error during the save block
        with patch("center_administration.serializer.CenterAdminConfiginitialSerializer.save", 
                   side_effect=transaction.TransactionManagementError("db tx failure")):
            with patch("center_administration.serializer.CenterAdminConfiginitialSerializer.is_valid", return_value=True):
                request = self.factory.post("/api/dashboard/config/", self.valid_payload, format="json")
                force_authenticate(request, user=self.user)
                response = self.view(request)
                
                self.assertEqual(response.status_code, 400)
                self.assertIn("Transaction error", str(response.data))
