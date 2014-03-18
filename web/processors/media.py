
import os
import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image as PilImage


class UploadImageError(Exception):
    pass


def process_image(image_file):
    """
    resize an uploaded image and convert to png format
    """
    size = 256, 512
    
    image_name = image_file.name
    image_basename, image_format = os.path.splitext(image_name)
    new_image_name = "%s.png" % (image_basename)

    new_image_url = "%s/%s/%s.png" % (settings.MEDIA_ROOT,"event_picture", image_basename)

    #Create a file-like object to write image data
    im_io = StringIO.StringIO()
    
    try:
               
        im = PilImage.open(image_file)

        if max(im.size) > max(size):
            im.thumbnail(size, PilImage.ANTIALIAS)
            print im

        #Write image data to StringIO.StringIO() object. We will later use it to create Django file-like object
        im.save(im_io, "png")
        
    except (IOError, OSError):
        msg = 'Failed while processing image (image_file=%s, image_name=%s, image_new_url=%s).' \
              % (image_file, image_name, new_image_url, )

    #Create a django file like object to be used in models as ImageField
    im_file = InMemoryUploadedFile(im_io, None, new_image_name, 'image/png', im_io.len, None)
    return im_file

def verify_image_size(image_size):

    if image_size > (256 * 1024):
        raise UploadImageError('Image file is too large')
