from app import app
import secrets, os, io
from PIL import Image

def save_picture(img, folder):

    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + ".jpg"
    picture_path = os.path.join(app.root_path, f'static/{folder}', picture_fn)

    # let's resize our picture to 150x150
    #output_size = (150, 150)
    buffer = io.BytesIO(img)
    i = Image.open(buffer)
    i.convert('RGB')
    i.save(picture_path)

    return picture_fn