import os

import requests

for id_patient in range(1, 101):
    data = requests.get('https://thispersondoesnotexist.com')
    photofile_title = f"{id_patient}.jpg"
    photofile_path = os.path.join('media', "photos", photofile_title)

    with open(photofile_path, "wb") as file:
        file.write(data.content)
        