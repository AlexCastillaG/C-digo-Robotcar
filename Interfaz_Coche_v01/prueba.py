from PIL import Image
from time import sleep
i=0

while True:
    i=i+1

    im = Image.open('images\\volante_original.png')
    im=im.rotate(i)
    im.save('images\\volante.png')
