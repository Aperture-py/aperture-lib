def resize_image(image, tuple_wh, preserve_aspect=True):
    """Resizes an instance of a PIL Image.

    In order to prevent un-intended side effects,
    this function always returns a copy of the image,
    as the resize function from PIL returns a copy 
    but the thumbnail function does not.

    Args:
        image: An instance of a PIL Image.
        tuple_wh: A tuple containing the (width, height) for resizing.
        preserve_aspect: A boolean that determines whether or not the
            resizing should preserve the image's aspect ratio.

    Returns: A resized copy of the provided PIL image.
    """

    if preserve_aspect:
        img_cpy = image.copy()
        img_cpy.thumbnail(tuple_wh)
        return img_cpy
    else:
        return image.resize(tuple_wh)  # PIL resize returns a copy
