#!/usr/bin/env python3
"""Generate QR code for Mallku GitHub repository."""

import qrcode

# Create QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data("https://github.com/fsgeek/Mallku")
qr.make(fit=True)

# Create QR code image
img = qr.make_image(fill_color="rgb(54, 54, 54)", back_color="rgb(245, 237, 220)")

# Save the QR code
img.save("mallku-qr-code.png")
print("QR code generated: mallku-qr-code.png")
