from PIL import Image
from PIL import ImageDraw, ImageFont
import os
import requests
import io

dirname, filename = os.path.split(os.path.abspath(__file__))
font = ImageFont.truetype(f"{dirname}/data/font/SourceHanSansCN-Normal.ttf", 50)


def image_cache(url):
    filename = url.split("/")[-1]
    if not os.path.exists(f"{dirname}/data/image/{filename}"):
        with open(f"{dirname}/data/image/{filename}", "wb") as f:
            r = requests.get(url, stream=True)
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)
    return Image.open(f"{dirname}/data/image/{filename}")


def pad_image(images, max_widen):
    result = []
    for image in images:
        iw, ih = image.size
        h = int((max_widen/iw) * ih)
        result.append(image.resize((max_widen, h), Image.BICUBIC))
    return result


def draw_rank(img, rank):
    draw = ImageDraw.Draw(img)
    draw.text(xy=(img.size[0] // 2 - 50, img.size[1] // 2 + 90), text="#" + str(rank), fill='white', font=font)
    return img


def draw_profile(data):
    img_leged = image_trans(image_cache(data.get("legends").get("selected").get("ImgAssets").get("icon")))
    result = Image.open(f"{dirname}/data/image/base.png")
    result.paste(img_leged, box=(0, 0), mask=img_leged)
    img_rank = image_cache(data.get("global").get("rank").get("rankImg"))
    if data.get("global").get("rank").get("rankName") == "Apex Predator":
        img_rank = draw_rank(img_rank, data.get("global").get("rank").get("ladderPosPlatform"))
    # img_rank.show()
    draw = ImageDraw.Draw(result)
    profile_font = ImageFont.truetype(f"{dirname}/data/font/SourceHanSansCN-Normal.ttf", 20)
    img_rank = image_trans(pad_image([img_rank], 150)[0])
    result.paste(img_rank, box=(0, 0), mask=img_rank)
    draw.text(xy=(40, 150), text=str(data.get("global").get("rank").get("rankScore")) + "pt", fill='white', font=profile_font)
    img_arena = image_cache(data.get("global").get("arena").get("rankImg"))
    if data.get("global").get("arena").get("rankName") == "Apex Predator":
        img_arena = draw_rank(img_arena, data.get("global").get("arena").get("ladderPosPlatform"))
    img_arena = image_trans(pad_image([img_arena], 150)[0])
    result.paste(img_arena, box=(0, 200), mask=img_arena)
    draw.text(xy=(40, 350), text=str(data.get("global").get("arena").get("rankScore")) + "pt", fill='white', font=profile_font)
    level_text = f'id： {data.get("global").get("name")}\n等级：{data.get("global").get("level")}\n{data.get("realtime").get("currentStateAsText")}'
    draw.text(xy=(result.size[0]-200, 0), text=level_text, fill='white', font=profile_font)
    badges_text = "\n".join([f'{i.get("name")}:{i.get("value")}' for i in data.get("legends").get("selected").get("gameInfo").get("badges")])
    draw.text(xy=(result.size[0] - 200, result.size[1] - 150), text="追踪器:\n" + ("无" if not badges_text else badges_text), fill='white', font=profile_font)
    b = io.BytesIO()
    result.save(b, 'png')
    return b.getvalue()


def image_trans(image):
    image = image.convert("RGBA")
    fg_img_trans = Image.new("RGBA", image.size)
    fg_img_trans = Image.blend(fg_img_trans, image, 1)
    return fg_img_trans


def draw_map(data):  # 3840*1200
    images = []
    map_type = ["battle_royale", "arenas", "ranked", "arenasRanked"]
    for index in map_type:
        images.append(image_cache(data.get(index).get("current").get("asset")))
    length = 0  # 空白长图的长
    max_widen = 999999  # 空白长图的宽
    for i in images:
        if max_widen > i.size[0]:
            max_widen = i.size[0]
    images = pad_image(images, max_widen)
    for i in images:
        length += i.size[1]
    result = Image.new(images[0].mode, (max_widen, length))
    draw = ImageDraw.Draw(result)
    length = 0
    for i in range(len(images)):
        image = images[i]
        result.paste(image, box=(0, length))
        text = f'模式:{map_type[i]}\n当前地图：{data.get(map_type[i]).get("current").get("map")}\n下张地图：{data.get(map_type[i]).get("next").get("map")}\n剩余时间：{data.get(map_type[i]).get("current").get("remainingTimer")}'
        length += image.size[1]
        # 在图片上写字：位置(x左右，y上下)，文字，颜色，字体
        draw.text(xy=(0, length - 250), text=text, fill='white', font=font)
    result = pad_image([result], 800)[0]
    b = io.BytesIO()
    result.save(b, 'png')
    return b.getvalue()


if __name__ == "__main__":
    print(dirname)
