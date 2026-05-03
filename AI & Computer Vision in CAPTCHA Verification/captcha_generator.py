import random
import math
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from captcha.image import ImageCaptcha
import captcha_db


img_dir = Path.cwd() / 'AI & Computer Vision in CAPTCHA Verification'

def string_generator():
    char_condition =  "\\/ilIjyo10Oxsvw.,:;`_^-=*()[}><|+!]{\"\'"
    str_len = random.randint(5,8)
    str_final = ""

    for i in range(str_len):
        while True:
            char_temp = chr(random.randint(33, 125))

            if char_temp not in char_condition:
                str_final += char_temp   
                break

    return list(str_final)


def captcha_generator(number_of_images: int):
    captcha_fonts = ['arialbd.ttf', 'arialbi.ttf', 
                     'timesbd.ttf', 'timesbi.ttf', 
                     'segoeuib.ttf']
    img_width = 400
    img_height = 150

    for i in range(number_of_images):
        char_counter = 0.1
        str_code = string_generator()
        bg_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        luminace = (0.2126*bg_color[0] + 0.7152*bg_color[1] + 0.0722*bg_color[2]) / 255

        text_color = (random.randint(0,70), random.randint(0,70), random.randint(0,70)) if luminace > 0.5 \
                else (random.randint(180,255), random.randint(180,255), random.randint(180,255))
        
        im = Image.new(size=(img_width,img_height), mode="RGB", color=bg_color)

        for j in str_code:
            img_char = Image.new(size=(80,80), mode="RGBA")
            img_char_text = ImageDraw.Draw(img_char)
            img_font = ImageFont.truetype(captcha_fonts[random.randint(0,4)], size=random.randint(55,65))
            img_char_text.text((5,5), j, font=img_font, fill=text_color)    
            img_char = img_char.rotate(random.randint(-40, 40))

            im.paste(img_char, ((int(50*char_counter)),random.randint(0,60)), mask=img_char)
            char_counter += 1

        pixels = im.load() 
        new_img = np.array([[[0,0,0]]*(img_width)]*(img_height))
        new_img = new_img.astype(np.uint8)
        rand_amplitude = random.uniform(4,6)

        for j in range(img_width):
            for k in range(img_height):
                sine_wave = (rand_amplitude * math.sin(0.1 * j + 1))
                new_img[k,j] = pixels[j + sine_wave, k] # type: ignore

        im = Image.fromarray(new_img)
        im_draw = ImageDraw.Draw(im)
         
        for line in range(random.randint(6,8)):
            im_draw.line(([random.randint(0, img_width)-50, random.randint(0, img_height)-50],
                          [random.randint(0, img_width)+50, random.randint(0, img_height)+50]), 
                          fill=text_color, width=random.randint(2,3))
            
        for salt_and_pepper in range(30000):
            im_draw.point([random.randint(0, img_width), random.randint(0, img_height)], fill=text_color)
        
        im_gaussian = ImageFilter.GaussianBlur(radius=random.uniform(1.2, 1.4))
        im = im.filter(im_gaussian)
        str_code = "".join(str_code)

        image = ImageCaptcha(fonts=['arialbd.ttf', 'arialbi.ttf', 
                                    'timesbd.ttf', 'timesbi.ttf', 
                                    'segoeuib.ttf'])
        image.character_rotate = (-40, 40)
        image.character_offset_dx
        image.write(str_code, f'{img_dir}\\opensrc_captcha_images\\os{i}.png')
        
        image_resize = Image.open(f"{img_dir}\\opensrc_captcha_images\\os{i}.png")
        image_resize = image_resize.resize((int(image_resize.width * 2.5), int(image_resize.height * 2.5)))
        image_resize.save(f"{img_dir}\\opensrc_captcha_images\\os{i}.png")
        with open (f"{img_dir}\\opensrc_captcha_images\\os{i}.png", 'rb') as f:
            blob = f.read()
            captcha_db.add_item(table_name="opensource_implementation", file_name=f"os{i}.png", captcha_code=str_code, captcha_image=blob) # type: ignore

        im.save(f"{img_dir}\\author_captcha_images\\a{i}.png")
        with open (f"{img_dir}\\author_captcha_images\\a{i}.png", 'rb') as f:
            blob = f.read()
            captcha_db.add_item(table_name="author_implementation", file_name=f"a{i}.png", captcha_code=str_code, captcha_image=blob) # type: ignore


captcha_db.delte_all(table_name="opensource_implementation") # type: ignore
captcha_db.delte_all(table_name="author_implementation") # type: ignore
captcha_generator(10)
