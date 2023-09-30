import random
from PIL import Image, ImageDraw, ImageFont


def gen_verified_image():
    width, height, font_size, font_num = 120, 35, 25, 4
    bg_color = (245, 245, 245)
    image = Image.new(mode='RGB', size=(width, height), color=bg_color)
    draw = ImageDraw.Draw(image, mode='RGB')
    font = ImageFont.truetype("gadugi.ttf", font_size)      # 导入字体文件
    verify = str()
    for i in range(font_num):
        x = random.randint(i * (width / font_num) + 2, (i + 1) * (width / font_num) - font_size - 2)
        y = 0
        char = str(random.choice([x for x in range(10)]))
        verify += char
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.text((x, y), char, fill=color, font=font)
    print("图片验证码是；",verify)
    return image, verify


if __name__ == '__main__':
    """怎么使用"""
    image, verify = gen_verified_image()
    print(verify)
    image.show()
