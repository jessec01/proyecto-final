#invoice/models.py

#importaciones de django
from django.db import models
from django.core.files.base import ContentFile
import io

#importaciones internas
from pay.models import Pay

# Si reportlab no está instalado, fallará silenciosamente sin quebrar el código
# Se forzó un reload para cargar reportlab después de instalarlo
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    canvas = None

class Invoice(models.Model):
    # 1. Relación estricta con el Pago (Si se borra el pago, se borra la factura)
    pay = models.OneToOneField(Pay, on_delete=models.CASCADE, related_name='invoice')
    
    # 2. Número de Factura o Recibo (Debe ser único)
    invoice_number = models.CharField(max_length=50, unique=True)
    
    # 3. Fotografía de los datos del cliente en ESE momento exacto
    client_name = models.CharField(max_length=150)
    client_document = models.CharField(max_length=20) # DNI, Pasaporte o RUC
    
    # 4. Desglose matemático (Igual que en Pay, usamos DecimalField para dinero)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # 5. Fechas y Estado
    status = models.CharField(
        max_length=20, 
        choices=[('issued', 'Emitida'), ('voided', 'Anulada')], 
        default='issued'
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True) # Mejor por defecto True
    
    # 6. Archivo físico para guardar el PDF
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"Factura {self.invoice_number} - {self.client_name}"
        
    def generate_invoice_pdf(self):
        # Si la factura no está activa o no tienes reportlab instalado, salimos
        if not self.active or canvas is None:
            print("No se pudo generar el PDF. Verifica si 'reportlab' está instalado vía pip.")
            return None
            
        buffer = io.BytesIO()
        # Inicializamos el canvas de PDF con un tamaño de papel carta (letter)
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Dibujamos en el PDF (Coordenadas x, y desde abajo hacia arriba)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Yoga Center - Factura Comercial")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 710, f"Número de Factura: {self.invoice_number}")
        p.drawString(100, 690, f"Fecha de Emisión: {self.issued_at.strftime('%Y-%m-%d %H:%M') if self.issued_at else 'N/A'}")
        p.drawString(100, 670, f"Cliente: {self.client_name}")
        p.drawString(100, 650, f"Documento: {self.client_document}")
        
        # Detalles de la compra
        p.drawString(100, 600, "-" * 80)
        # Nos protegemos en caso de que pay.package no exista
        package_name = self.pay.package.name if (self.pay and self.pay.package) else "Servicio General"
        p.drawString(100, 580, f"Paquete adquirido: {package_name}")
        p.drawString(100, 560, "-" * 80)
        
        # Cálculos de dinero (alineados a la derecha)
        p.drawString(350, 520, f"Subtotal: ${self.subtotal}")
        p.drawString(350, 500, f"Impuestos: ${self.tax_amount}")
        p.setFont("Helvetica-Bold", 12)
        p.drawString(350, 480, f"Total a Pagar: ${self.total_amount}")
        
        # Mensaje de despedida
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(100, 400, "¡Gracias por transformar tu mente y cuerpo con nosotros!")
        
        # Cerramos y guardamos el documento PDF en el "buffer" de memoria
        p.showPage()
        p.save()
        
        # Volvemos al inicio del archivo virtual
        buffer.seek(0)
        
        # Guardamos el PDF en el FileField de nuestra Base de Datos
        file_name = f"Factura_{self.invoice_number}.pdf"
        self.invoice_file.save(file_name, ContentFile(buffer.read()), save=True)
        
        # Devolvemos la URL donde se guardó el documento PDF
        return self.invoice_file.url