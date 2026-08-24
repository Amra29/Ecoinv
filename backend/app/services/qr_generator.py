import uuid
import qrcode
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_lote_qr_pdf(uuid_list: list[str], output_pdf_path: str = "qr_exports/etiquetas.pdf"):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    
    x, y = 50, 700
    for index, codigo_uuid in enumerate(uuid_list):
        # Generar imagen QR temporal
        qr_img = qrcode.make(f"https://ecoinv.com/scan/{codigo_uuid}")
        temp_img_path = f"qr_exports/temp_{codigo_uuid}.png"
        qr_img.save(temp_img_path)
        
        # Dibujar en PDF
        c.drawImage(temp_img_path, x, y, width=100, height=100)
        c.drawString(x, y - 10, f"ID: {codigo_uuid[:8]}...")
        
        os.remove(temp_img_path) # Limpieza
        
        x += 130
        if (index + 1) % 4 == 0:
            x = 50
            y -= 130
            if y < 100:
                c.showPage()
                y = 700
                
    c.save()
    return output_pdf_path