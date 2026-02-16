from django.test import TestCase
from rest_framework.test import APIRequestFactory
from unittest.mock import patch
from django.db import IntegrityError
from django.db.utils import OperationalError

from .views import SaveUserView


class AuditoriaProfundaTests(TestCase):
    """Tres pruebas de auditoría crecientes sobre el endpoint de registro.

    1) Básico: entradas inválidas y chequeo de errores expuestos.
    2) Intermedio: violación de integridad (IntegrityError) simulada.
    3) Potente: fallos de infraestructura (OperationalError), excepción genérica
       y fuzzing con payloads extremos.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SaveUserView.as_view()

    def test_basico_campos_obligatorios_y_validaciones(self):
        # Missing confirmation_password and invalid first_name -> 400
        data = {
            "email": "audit_basic@example.com",
            "password": "StrongP@ss1",
            # "confirmation_password" intentionally missing
            "username": "auditbasic",
            "first_name": "Ana",  # inválido: < 4 letras
            "last_name": "User",
            "phone": "+584121234567",
        }
        req = self.factory.post("/api/save-user/", data, format="json")
        resp = self.view(req)
        self.assertEqual(resp.status_code, 400)
        # No debe exponer stack traces en la respuesta
        self.assertNotIn("Traceback", str(resp.data))

    def test_intermedio_integrity_error_en_guardado(self):
        data = {
            "email": "audit_dup@example.com",
            "password": "StrongP@ss1",
            "confirmation_password": "StrongP@ss1",
            "username": "auditdup",
            "first_name": "Anna",
            "last_name": "Dup",
            "phone": "+584121234567",
        }
        # Simulamos que el create/ save lanza IntegrityError (duplicado/constraint)
        with patch("userYC.serializer.UserYCSerializer.create", side_effect=IntegrityError("unique constraint")):
            req = self.factory.post("/api/save-user/", data, format="json")
            resp = self.view(req)
            # Aceptamos 400/409/500 según implementación, pero no debe filtrar stack
            self.assertIn(resp.status_code, (400, 409, 500))
            self.assertNotIn("Traceback", str(resp.data))

    def test_potente_operational_exception_generica_y_fuzz(self):
        good = {
            "email": "audit_ops@example.com",
            "password": "StrongP@ss1",
            "confirmation_password": "StrongP@ss1",
            "username": "audittest",
            "first_name": "Anna",
            "last_name": "Ops",
            "phone": "+584121234567",
        }

        # 1) Simular BD caída (OperationalError)
        with patch("userYC.views.UserYCSerializer.save", side_effect=OperationalError("db down")):
            req = self.factory.post("/api/save-user/", good, format="json")
            resp = self.view(req)
            # Ideal: 500/503 y sin leaks de error técnico
            self.assertIn(resp.status_code, (500, 503))
            self.assertNotIn("OperationalError", str(resp.data))

        # 2) Simular excepción genérica inesperada
        with patch("userYC.views.UserYCSerializer.save", side_effect=Exception("boom")):
            req = self.factory.post("/api/save-user/", good, format="json")
            resp = self.view(req)
            self.assertIn(resp.status_code, (500,))
            self.assertNotIn("boom", str(resp.data))

        # 3) Fuzzing simple: campos extremadamente largos / caracteres de control
        fuzz = good.copy()
        fuzz["username"] = "u" * 20000
        fuzz["first_name"] = "\x00\x01\x02<script>alert(1)</script>"
        req = self.factory.post("/api/save-user/", fuzz, format="json")
        resp = self.view(req)
        # Esperamos que la app responda con manejo (400/413/500), pero no crash
        self.assertIn(resp.status_code, (400, 413, 500))
        self.assertNotIn("Traceback", str(resp.data))
