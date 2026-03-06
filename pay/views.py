#pay/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from packages.models import Packages
from yogui.models import Yogui
from pay.service import PayService
from invoice.models import Invoice

class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 1. Aseguramos que el usuario que intenta comprar es un Yogui
            yogui = Yogui.objects.get(user=request.user)
            
            # 2. Obtenemos el ID del paquete desde el FrontEnd
            package_id = request.data.get('package_id')
            want_invoice = request.data.get('want_invoice', False) # Checkbox en el frontend

            if not package_id:
                return Response({'error': 'Falta el ID del paquete.'}, status=status.HTTP_400_BAD_REQUEST)

            package = get_object_or_404(Packages, id=package_id)

            # 3. Llamamos a nuestro poderoso MOTOR SECRETO (PayService)
            service = PayService()
            pay = service.process_pay(yogui, package)

            # 4. Si el Yogui quiere comprobante legal, se lo creamos al vuelo:
            invoice_url = None
            if want_invoice:
                # Vamos a suponer que no cobramos impuestos extra, todo está en el precio final
                tax_amount = 0 
                subtotal = pay.final_amount - tax_amount

                # Creamos el registro de Factura en BD
                invoice = Invoice.objects.create(
                    pay=pay,
                    invoice_number=f"F-2026-{pay.id:06d}", # Ejemplo: F-2026-000001
                    client_name=f"{yogui.user.first_name} {yogui.user.last_name}",
                    client_document=yogui.id_card,
                    subtotal=subtotal,
                    tax_amount=tax_amount,
                    total_amount=pay.final_amount,
                    active=True
                )
                
                # Generamos el PDF con ReportLab (lo que acabas de hacer)
                invoice_url = invoice.generate_invoice_pdf()

            return Response({
                'message': '¡Compra realizada con éxito! ¡Namasté!',
                'invoice_url': invoice_url, # Será None si no lo pidió, o el link al PDF
                'pay_id': pay.id
            }, status=status.HTTP_200_OK)

        except Yogui.DoesNotExist:
            return Response({'error': 'Solamente los Yoguis pueden comprar paquetes.'}, status=status.HTTP_403_FORBIDDEN)
        # Si nuestra validación Transaccional lanza una Excepción de las tuyas, entra aquí:
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
