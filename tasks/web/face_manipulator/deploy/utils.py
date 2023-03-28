import os

from PIL import Image
# https://archive.org/details/1mFakeFaces
arr = os.listdir('fake')

print(arr)

for name in arr:
    path = os.path.join('fake', name)
    im = Image.open(path)
    im = im.resize((512, 512))
    im.save(path)
