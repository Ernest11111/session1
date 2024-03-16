import os
import qrcode

for id_patient in range(1,101):
    qr_file = qrcode.make(id_patient)
    qrfile_name = f'{id_patient}.png'
    qrfile_path = os.path.join('media', 'qrcodes', qrfile_name)
    qr_file.save(qrfile_path)
