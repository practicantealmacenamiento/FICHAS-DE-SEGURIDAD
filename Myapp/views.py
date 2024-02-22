import os
import base64
import mimetypes
import json
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, "index.html")


def obtener_nombres_pdf(request):
    directorio_pdf = r"C:\Users\prac.almacenamiento\OneDrive - Prebel S.A\FDS\FICHAS DE DATOS DE SEGURIDAD"
    nombres_pdf = []

    # Obtener todos los nombres de archivos PDF en el directorio
    for filename in os.listdir(directorio_pdf):
        if filename.endswith(".pdf"):
            nombres_pdf.append(filename)

    return JsonResponse({"nombres_pdf": nombres_pdf})


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


def buscar(request):
    if request.method == "POST":
        try:
            codigo = request.POST.get("codigo")
            pdf_local_path = buscar_pdf_en_onedrive_local(codigo)

            if pdf_local_path:
                with open(pdf_local_path, "rb") as f:
                    pdf_content = f.read()
                response = HttpResponse(pdf_content, content_type="application/pdf")
                response["Content-Disposition"] = f"inline; filename={codigo}.pdf"
                return response
            else:
                return JsonResponse(
                    {
                        "error": "El código ingresado no se encuentra. Por favor, pruebe con otro código.",
                        "status": "error",
                    },
                    status=404,
                )
        except Exception as e:
            # Maneja cualquier excepción y devuelve una respuesta adecuada
            return JsonResponse(
                {"error": f"Error inesperado: {str(e)}", "status": "error"}, status=500
            )

    return JsonResponse(
        {"error": "Método no permitido.", "status": "error"}, status=405
    )


def buscar_pdf_similares(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo", "")
        directorio_pdf = r"C:\Users\prac.almacenamiento\OneDrive - Prebel S.A\FDS\FICHAS DE DATOS DE SEGURIDAD"  # Ruta del directorio de PDFs
        nombres_pdf = []
        for filename in os.listdir(directorio_pdf):
            if filename.endswith(".pdf") and codigo.lower() in filename.lower():
                nombres_pdf.append(filename)
        # Devolver una respuesta JSON con los nombres de los archivos PDF
        return JsonResponse({"nombres_pdf": nombres_pdf})
    return JsonResponse({"error": "Método no permitido"}, status=405)
