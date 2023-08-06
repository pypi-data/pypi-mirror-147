import pillow_avif  # noqa
from willow.image import ImageFile
from willow.plugins.pillow import PillowImage
from willow.registry import registry


class AVIFImageFile(ImageFile):
    format_name = "avif"


def pillow_save_avif(image, filename, quality=50, **options):
    image.get_pillow_image().save(filename, "avif", quality=quality, **options)
    return AVIFImageFile(filename)


registry.register_operation(PillowImage, "save_as_avif", pillow_save_avif)
