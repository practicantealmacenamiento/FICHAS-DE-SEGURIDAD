from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


def enviar_correo_django(request):
    try:
        codigo = request.GET.get("codigo")
        subject = f"Solicitud de PDF - Código {codigo}"
        message = f"Estimado usuario,\n\nEl código {codigo} no se encuentra en el sistema. Por favor, revise la solicitud."
        from_email = settings.EMAIL_HOST_USER
        to_email = ["practicante.almacenamiento@prebel.com.co"]

        send_mail(subject, message, from_email, to_email, fail_silently=False)
        return HttpResponse("Correo enviado correctamente", status=200)
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return HttpResponse("Error al enviar el correo", status=500)
