import random

from PIL import Image, ImageFont
from PIL import ImageDraw


def randomColor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def randomXy(maxX: int, maxY: int):
    return random.randint(0, maxX), random.randint(0, maxY)


def checkdeImage(width: int, height: int, checkcode: str):
    img = Image.new('RGB', (width, height), randomColor())
    draw = ImageDraw.Draw(img)

    for i in range(50):
        draw.line((randomXy(width, height), randomXy(width, height)), fill=randomColor())

    for i, c in enumerate(checkcode):
        draw.text((5 + i * width // (len(checkcode) + 1), 10), c,
                  fill=randomColor(), font=ImageFont.truetype('arial.ttf', 30))

    return img


if __name__ == '__main__':
    im = checkdeImage(150, 50, "054410")
    im.show()
