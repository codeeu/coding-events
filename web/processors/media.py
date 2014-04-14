import os
import uuid

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.defaultfilters import slugify
from PIL import Image as PilImage
import StringIO


class UploadImageError(Exception):
	pass


class ImageSizeTooLargeException(Exception):
	pass


def process_image(image_file):
	"""
	resize an uploaded image and convert to png format
	"""
	size = 256, 512
	image_name = image_file.name
	image_basename, image_format = os.path.splitext(image_name)
	new_image_name = "%s_%s.png" % (slugify(image_basename), uuid.uuid4())

	try:
		im = PilImage.open(image_file)
		if max(im.size) > max(size):
			im.thumbnail(size, PilImage.ANTIALIAS)

		thumb_io = StringIO.StringIO()
		im.save(thumb_io, format='png')
		return InMemoryUploadedFile(thumb_io, None, new_image_name, 'image/png', thumb_io.len, None)

	except IOError as e:
		msg = 'Failed while processing image (image_file=%s, image_name=%s, error_number=%s, error=%s).' \
		      % (image_file, new_image_name, e.errno, e.strerror, )
		raise UploadImageError(msg)



