import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageColor

def string_generator():
    char_condition =  "\\/ilIo0O.,:`_-=*()[}><|+!]{\"\'"
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
    captcha_fonts = ['arialbd.ttf','arialbi.ttf']
    img_width = 320
    img_height = 110

    for i in range(number_of_images):
        str_code = string_generator()
        bg_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        
        im = Image.new(size=(img_width,img_height), mode="RGB", color=bg_color)

        for j in str_code:
            img_char = Image.new(size=(50,50), mode="RGBA", color=(0,0,0,0))
            img_char_text = ImageDraw.Draw(img_char)
            img_font = ImageFont.truetype(captcha_fonts[random.randint(0,1)], size=random.randint(35,40))
            img_char_text.text((5,5), j, font=img_font)    
            img_char.rotate(random.randint(-55,-50))

            im.paste(img_char, ((45*str_code.index(j)),random.randint(0,60)), mask=img_char)
        im.save(f"{"".join(str_code)}_{i}.png")

"""
fix: not rotation for chars;
fix: same char on top of the same char - if both the same
add: random spacing 40-50 between paste


"""
            



  
print(captcha_generator(1))
