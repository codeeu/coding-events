import os
import uuid

from django.conf import settings
from django.template.defaultfilters import slugify
from PIL import Image as PilImage


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

	new_image_url = "%s/%s/%s" % (settings.MEDIA_ROOT, settings.MEDIA_UPLOAD_FOLDER, new_image_name)

	try:
		im = PilImage.open(image_file)
		if max(im.size) > max(size):
			im.thumbnail(size, PilImage.ANTIALIAS)

		im.save(new_image_url, "png")

	except IOError as e:
		msg = 'Failed while processing image (image_file=%s, image_name=%s, image_new_url=%s, error_number=%s, error=%s).' \
		      % (image_file, image_name, new_image_url, e.errno, e.strerror, )
		raise UploadImageError(msg)

	return new_image_url

