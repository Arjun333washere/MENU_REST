import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(menu):
    # Ensure that menu_url uses the correct menu ID
    menu_url = f"http://192.168.29.230:8000/menu/menus/{menu.id}/"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Save the image to the menu's qr_code field
    filename = f"qr_code_{menu.id}.png"
    menu.qr_code.save(filename, File(img_io), save=True)
