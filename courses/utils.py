from PIL import Image, ImageDraw, ImageFont
import random
import os
import textwrap
from django.utils.text import slugify
from enstructor.settings import MEDIA_ROOT, BASE_DIR

COLORS = ['red', 'blue', 'green', 'yellow', 'pink', 'cyan', 'black']


def _generate_text_color_for(color):
    if color == 'red' or color == 'blue' or color == 'green' \
        or color == 'black':
        return 'white'
    elif color == 'cyan' or color == 'yellow':
        return 'black'
    else:
        return 'black'

def generate_custom_course_banner(course_name):
    course_name_paragraph = textwrap.wrap(course_name, width=25)
    # Width and height of the banner
    W, H = 300, 220
    # Choose a random color for the banner
    bg_color = random.choice(COLORS)
    # Create an image
    img = Image.new('RGBA', (W, H), bg_color)
    # Make a canvas
    draw = ImageDraw.Draw(img)

    # font setup
    font_location = os.path.join(BASE_DIR, 'static/fonts/')
    custom_font = ImageFont.truetype(font_location + 'arial.ttf', 22)

    # text alignment on the image
    current_h, pad = 50, 10  # current_h should be calculated based off of H
    for line in course_name_paragraph:
        w, h = draw.textsize(line, font=custom_font)
        draw.text(
            ((W - w) / 2, current_h),
            line,
            font=custom_font,
            fill=_generate_text_color_for(bg_color)
        )
        current_h += h + pad
    
    # Process saving the image
    save_path = os.path.join(MEDIA_ROOT, 'courses/banners/')
    img_name = slugify(course_name) + '.png'
    img.save(
        save_path + img_name, "PNG"
    )
    return f'{save_path}/{img_name}'
