import qrcode

# CHANGE THIS IP TO YOUR SYSTEM IP
url = "http://10.216.59.53:5000/?location=Lab-1"

qr = qrcode.make(url)
qr.save("Lab1_QR.png")

print("QR Code Generated Successfully")
