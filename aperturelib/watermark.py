from PIL import Image, ImageDraw, ImageFont
from pkg_resources import resource_exists, resource_filename, cleanup_resources


def watermark_image(image, wtrmrk_path, corner=2):
    '''Adds a watermark image to an instance of a PIL Image.

    If the provided watermark image (wtrmrk_path) is
    larger than the provided base image (image), then
    the watermark image will be automatically resized to 
    roughly 1/8 the size of the base image.

    Args:
        image: An instance of a PIL Image. This is the base image.
        wtrmrk_path: Path to the watermark image to use.
        corner: An integer between 0 and 3 representing the corner
            where the watermark image should be placed on top of the
            base image. 0 is top left, 1 is top right, 2 is bottom
            right and 3 is bottom left. NOTE: Right now, this is 
            permanently set to 2 (bottom right) but this can be 
            changed in the future by either creating a new cmd-line
            flag or putting this in the config file.

    Returns: The watermarked image
    '''
    padding = 2
    wtrmrk_img = Image.open(wtrmrk_path)

    #Need to perform size check in here rather than in options.py because this is
    # the only place where we know the size of the image that the watermark is
    # being placed onto
    if wtrmrk_img.width > (image.width - padding * 2) or wtrmrk_img.height > (
            image.height - padding * 2):
        res = (int(image.width / 8.0), int(image.height / 8.0))
        resize_in_place(wtrmrk_img, res)

    pos = get_pos(corner, image.size, wtrmrk_img.size, padding)

    was_P = image.mode == 'P'
    was_L = image.mode == 'L'

    # Fix PIL palette issue by converting palette images to RGBA
    if image.mode not in ['RGB', 'RGBA']:
        if image.format in ['JPG', 'JPEG']:
            image = image.convert('RGB')
        else:
            image = image.convert('RGBA')

    image.paste(wtrmrk_img.convert('RGBA'), pos, wtrmrk_img.convert('RGBA'))

    if was_P:
        image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
    elif was_L:
        image = image.convert('L')

    return image


def watermark_text(image, text, corner=2):
    '''Adds a text watermark to an instance of a PIL Image.

    The text will be sized so that the height of the text is
    roughly 1/20th the height of the base image. The text will 
    be white with a thin black outline.

    Args:
        image: An instance of a PIL Image. This is the base image.
        text: Text to use as a watermark.
        corner: An integer between 0 and 3 representing the corner
            where the watermark image should be placed on top of the
            base image. 0 is top left, 1 is top right, 2 is bottom
            right and 3 is bottom left. NOTE: Right now, this is 
            permanently set to 2 (bottom right) but this can be 
            changed in the future by either creating a new cmd-line
            flag or putting this in the config file.

    Returns: The watermarked image
    '''

    # Load Font
    FONT_PATH = ''
    if resource_exists(__name__, 'resources/fonts/SourceSansPro-Regular.ttf'):
        FONT_PATH = resource_filename(
            __name__, 'resources/fonts/SourceSansPro-Regular.ttf')

    padding = 5

    was_P = image.mode == 'P'
    was_L = image.mode == 'L'

    # Fix PIL palette issue by converting palette images to RGBA
    if image.mode not in ['RGB', 'RGBA']:
        if image.format in ['JPG', 'JPEG']:
            image = image.convert('RGB')
        else:
            image = image.convert('RGBA')

    # Get drawable image
    img_draw = ImageDraw.Draw(image)

    fontsize = 1  # starting font size

    # portion of image width you want text height to be.
    # default font size will have a height that is ~1/20
    # the height of the base image.
    img_fraction = 0.05

    # attempt to use Aperture default font. If that fails, use ImageFont default
    try:
        font = ImageFont.truetype(font=FONT_PATH, size=fontsize)
        was_over = False
        inc = 2
        while True:
            if font.getsize(text)[1] > img_fraction * image.height:
                if not was_over:
                    was_over = True
                    inc = -1
            else:
                if was_over:
                    break
            # iterate until the text size is just larger than the criteria
            fontsize += inc
            font = ImageFont.truetype(font=FONT_PATH, size=fontsize)
        fontsize -= 1
        font = ImageFont.truetype(font=FONT_PATH, size=fontsize)
    except:
        # replace with log message
        print('Failed to load Aperture font. Using default font instead.')
        font = ImageFont.load_default()  # Bad because default is suuuuper small

    # get position of text
    pos = get_pos(corner, image.size, font.getsize(text), padding)

    # draw a thin black border
    img_draw.text((pos[0] - 1, pos[1]), text, font=font, fill='black')
    img_draw.text((pos[0] + 1, pos[1]), text, font=font, fill='black')
    img_draw.text((pos[0], pos[1] - 1), text, font=font, fill='black')
    img_draw.text((pos[0], pos[1] + 1), text, font=font, fill='black')

    # draw the actual text
    img_draw.text(pos, text, font=font, fill='white')

    # Remove cached font file
    cleanup_resources()
    del img_draw

    if was_P:
        image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
    elif was_L:
        image = image.convert('L')

    return image


# Internal method
def resize_in_place(image, res):
    image.thumbnail(res)


# Internal method
def get_pos(corner, main_size, sub_size, padding):
    if (corner == 0):  #top left
        position = (padding, padding)
    elif (corner == 1):  #top right
        position = ((main_size[0] - sub_size[0] - padding), padding)
    elif (corner == 3):  #bottom left
        position = (padding, (main_size[1] - sub_size[1] - padding))
    else:  #bottom right (default)
        position = ((main_size[0] - sub_size[0] - padding),
                    (main_size[1] - sub_size[1] - padding))
    return position