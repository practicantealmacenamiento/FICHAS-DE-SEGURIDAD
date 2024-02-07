import win32com.client as win32


def enviar_correo(
    subject="practicante.almacenamiento@prebel.com.co",
    emails="practicante.almacenamiento@prebel.com.co",
    emails_cc="",
    importance=False,
    html_contend="",
    img_attachment=None,
    files_attachment=None,
):
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)

    mail.Subject = subject
    mail.To = emails
    mail.CC = emails_cc

    # Adjuntar imágenes
    if img_attachment:
        for img_path, id in img_attachment.items():
            attachment = mail.Attachments.Add(img_path)
            attachment.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", id
            )

    # Adjuntar archivos
    if files_attachment:
        for address in files_attachment:
            mail.Attachments.Add(address)

    # Importancia
    if importance:
        mail.Importance = 2

    mail.HTMLBody = html_contend

    mail.Send()
