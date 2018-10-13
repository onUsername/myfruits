from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, string


# 生成随机字母
def randchar():
    # 字母加数字
    ran = string.ascii_letters + string.digits
    char = ""
    for i in range(4):
        char += random.choice(ran)
    return char


# 随机颜色
def randcolor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def create_code():
    # 创建图片 模式、大小、背景色
    img = Image.new("RGB", (120, 40), (255, 255, 255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype("src.ttf", 25)

    code = randchar()
    # 将字符画在画布上
    for t in range(4):
        draw.text((30 * t + 5, 0), code[t], randcolor(), font)

    #生成干扰点
    for _ in range(random.randint(0,50)):
        #位置 颜色
        draw.point((random.randint(0,120),random.randint(0,30)),fill=randcolor())

    #使用模糊滤镜是图片模糊
    img = img.filter(ImageFilter.BLUR)

    return img,code


if __name__ == '__main__':
    create_code()
