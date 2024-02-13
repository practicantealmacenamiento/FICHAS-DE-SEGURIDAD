from django.shortcuts import render
from django.http import JsonResponse
import os
import base64
from django.http import HttpResponse
import mimetypes
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def buscar_pdf_en_onedrive_local(codigo):
    # Ruta completa al directorio local de OneDrive en tu sistema
    onedrive_local_path = r"C:\FDS\FICHAS DE DATOS DE SEGURIDAD"

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
