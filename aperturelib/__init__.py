''' Aperturelib '''

# Supported formats may be found here: http://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.gif', '.png')

from PIL import Image
from .resize import resize_image as resize
from .watermark import watermark_image
from .watermark import watermark_text


def open(f):
    '''Opens an instance of a PIL Image.

    This is a wrapper for the PIL Image open function.
    
    Args:
        f: File path or File object.

    Returns:
        (PIL.Image) An instance of a PIL image.
    '''
    return Image.open(f)


def format_image(path, options):
    '''Formats an image.

    Args:
        path (str): Path to the image file.
        options (dict): Options to apply to the image.

    Returns:
        (list) A list of PIL images. The list will always be of length
        1 unless resolutions for resizing are provided in the options. 
    '''
    image = Image.open(path)
    image_pipeline_results = __pipeline_image(image, options)
    return image_pipeline_results


def save(image, out_file, **kwargs):
    '''Saves an instance of a PIL Image to the system.

    This is a wrapper for the PIL Image save function.

    Args:
        img: An instance of a PIL Image.
        out_file: Path to save the image to.
        **kwargs: Additonal save options supported by PIL.
            (see https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html)
    '''
    image.save(out_file, **kwargs)


# Internal Methods
# =========================


def __pipeline_image(image, options):
    '''Sends an image through a processing pipeline.
    Applies all (relevant) provided options to a given image.
    Args:
        image: An instance of a PIL Image.
        options: Options to apply to the image (i.e. resolutions).
    Returns:
        A list containing instances of PIL Images. This list will always be length
        1 if no options exist that require multiple copies to be created for a single
        image (i.e resolutions).
    '''
    results = []

    # Begin pipline

    # 1. Create image copies for each resolution

    if 'resolutions' in options:
        resolutions = options['resolutions']  # List of resolution tuples
        for res in resolutions:
            img_rs = resize(image, res)  # Resized image

            # Add image to result set. This result set will be pulled from
            # throughout the pipelining process to perform more processing (watermarking).
            results.append(img_rs)

    # 2. Apply watermark to each image copy
    wtrmk_path = options['wmark-img']
    if wtrmk_path:
        if len(results) == 0:
            image = watermark_image(image, wtrmk_path)  #watermark actual image?
        else:
            for i in range(0, len(results)):
                results[i] = watermark_image(
                    results[i], wtrmk_path)  #watermark actual image

    wtrmk_txt = options['wmark-txt']
    if wtrmk_txt:
        if len(results) == 0:
            image = watermark_text(image, wtrmk_txt)  #watermark actual image?
        else:
            for i in range(0, len(results)):
                results[i] = watermark_text(results[i],
                                            wtrmk_txt)  #watermark actual image

    # Fallback: Nothing was done to the image
    if len(results) == 0:
        results.append(image)

    return results