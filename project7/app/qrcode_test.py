import qrcode

data = 'datadatadata'
a = qrcode.make(data)
a.save("test.png")