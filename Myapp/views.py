from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import win32com.client as win32
import pythoncom
import os
import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from pdf2image import convert_from_path
import traceback


def index(request):
    return render(request, "index.html")


def buscar_pdf_en_onedrive_local(codigo):
    # Ruta completa al directorio local de OneDrive en tu sistema
    onedrive_local_path = r"C:\Users\prac.almacenamiento\OneDrive - Prebel S.A\FDS\FICHAS DE DATOS DE SEGURIDAD"

    # Construye la ruta completa al PDF
    pdf_local_path = os.path.join(onedrive_local_path, f"{codigo}.pdf")

    # Verifica si el archivo existe en la ruta local
    if os.path.exists(pdf_local_path):
        return pdf_local_path
    else:
        return None


def convertir_pdf_a_imagen(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page_number in range(doc.page_count):
        page = doc[page_number]
        image = page.get_pixmap()
        img = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Convertir la imagen a bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        images.append(img_bytes.getvalue())

    return images


@csrf_exempt
def buscar(request):
    if request.method == "POST":
        try:
            codigo = request.POST.get("codigo")
            pdf_local_path = buscar_pdf_en_onedrive_local(codigo)

            if pdf_local_path:
                imagenes = convertir_pdf_a_imagen(pdf_local_path)

                if imagenes:
                    # Convertir imágenes a bytes y enviar al cliente
                    response_data = {
                        "images": [str(img, "latin-1") for img in imagenes],
                    }
                    return JsonResponse(response_data)
                else:
                    enviar_correo(codigo)
                    return JsonResponse(
                        {
                            "error": "El código ingresado no tiene imágenes.",
                            "status": "error",
                        },
                        status=404,
                    )
            else:
                enviar_correo(codigo)
                return JsonResponse(
                    {
                        "error": "El código ingresado no se encuentra. Por favor, pruebe con otro código.",
                        "status": "error",
                    },
                    status=404,
                )
        except Exception as e:
            # Maneja cualquier excepción y devuelve una respuesta adecuada
            traceback.print_exc()
            return JsonResponse(
                {"error": f"Error inesperado: {str(e)}", "status": "error"}, status=500
            )

    return JsonResponse(
        {"error": "Método no permitido.", "status": "error"}, status=405
    )


def enviar_correo(codigo):
    try:
        # Lógica para enviar correo electrónico
        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)

        mail.Subject = f"Solicitud de PDF - Código {codigo}"
        mail.To = "practicante.almacenamiento@prebel.com.co"
        mail.CC = ""
        mail.Importance = 2

        mail.HTMLBody = f"<p>Estimado usuario,</p><p>El código {codigo} no se encuentra en el sistema. Por favor, revise la solicitud.</p>"

        mail.Send()

        # Liberar los recursos de pythoncom
        # pylint: disable=no-member
        pythoncom.CoUninitialize()

        return HttpResponse("Correo electrónico enviado correctamente.")
    except Exception as e:
        # Maneja cualquier excepción y devuelve una respuesta adecuada
        return HttpResponse(f"Error al enviar correo: {str(e)}", status=500)
