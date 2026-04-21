import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageColor

img_dir = Path.cwd() / 'AI & Computer Vision in CAPTCHA Verification' / 'captcha_images'

def string_generator():
    char_condition =  "\\/ilIjo0O.,:;`_^-=*()[}><|+!]{\"\'"
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
                     'segoeuib.ttf', 'segoeuiz.ttf', 
                     'robotob.ttf', 'robotobi.ttf']
    img_width = 340
    img_height = 110

    for i in range(number_of_images):
        char_counter = 0
        str_code = string_generator()
        bg_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        luminace = (0.2126*bg_color[0] + 0.7152*bg_color[1] + 0.0722*bg_color[2]) / 255

        text_color = (random.randint(0,70), random.randint(0,70), random.randint(0,70)) if luminace > 0.5 \
                else (random.randint(180,255), random.randint(180,255), random.randint(180,255))
        
        im = Image.new(size=(img_width,img_height), mode="RGB", color=bg_color)
        im_draw = ImageDraw.Draw(im)

        for j in str_code:
            img_char = Image.new(size=(50,50), mode="RGBA")
            img_char_text = ImageDraw.Draw(img_char)
            img_font = ImageFont.truetype(captcha_fonts[random.randint(0,1)], size=random.randint(35,40))
            img_char_text.text((5,5), j, font=img_font, fill=text_color)    
            img_char = img_char.rotate(random.randint(-55, 55))

            im.paste(img_char, ((42*char_counter),random.randint(0,60)), mask=img_char)
            char_counter += 1

        pixels = list(im.getdata()) # type: ignore
        
        for pixel in pixels:
            ...

        """for line in range(random.randint(4,8)):
            im_draw.line(([random.randint(0, img_width)-50, random.randint(0, img_height)-50],
                          [random.randint(0, img_width)+50, random.randint(0, img_height)+50]), 
                          fill=text_color, width=random.randint(2,3))
            
        for salt_and_pepper in range(12000):
            im_draw.point([random.randint(0, img_width), random.randint(0, img_height)], fill=text_color)
        
        im_gaussian = ImageFilter.GaussianBlur(radius=random.uniform(1.2, 1.8))
        im =im.filter(im_gaussian)"""
        str_code = "".join(str_code).replace("?","0")

        im.save(fr"{img_dir}\\{i}.{str_code}.png")

  



  
print(captcha_generator(1))
