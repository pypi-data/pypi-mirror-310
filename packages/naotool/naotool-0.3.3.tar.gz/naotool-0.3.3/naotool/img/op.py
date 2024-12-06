import hashlib
from PIL import Image


colors = {
    "blue": (34, 52, 73),
    "yellow": (224, 164, 25),
    "white": (237, 239, 241),
    "black": (50, 50, 50),
    "pink": (255, 105, 180),
}


def img_md5hex(img: Image.Image) -> str:
    """计算一个图片的md5"""
    # 将图片转换为二进制数据
    img_bytes = img.tobytes()
    # 创建一个MD5哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象，img一般不会大，不用分块处理
    md5_hash.update(img_bytes)
    return md5_hash.hexdigest()


def add_top_border(
    image: Image.Image, border_height: int, border_color=colors["black"]
) -> Image.Image:
    """为图像顶部添加黑色边框。

    Args:
        image (Image.Image): 原始图像 (PIL.Image 对象)
        border_height (int): 边框的高度（像素）
        border_color (_type_, optional): 边框颜色，默认为黑色 (RGB)

    Returns:
        Image.Image: 添加边框后的图像
    """
    original_width, original_height = image.size
    new_height = original_height + border_height
    new_image = Image.new("RGB", (original_width, new_height), border_color)
    new_image.paste(image, (0, border_height))
    return new_image


def remove_bottom_border(image: Image.Image, crop_height: int) -> Image.Image:
    """从图像底部裁剪指定高度。

    Args:
        image (Image.Image): 原始图像 (PIL.Image 对象)
        crop_height (int): 要裁剪掉的高度（像素）

    Returns:
        Image.Image: 裁剪后的图像
    """
    original_width, original_height = image.size
    crop_height = min(crop_height, original_height)
    cropped_image = image.crop(
        (
            0,
            0,
            original_width,
            original_height - crop_height,
        )
    )
    return cropped_image


def crop_to_max_height(image: Image.Image, max_height: int) -> Image.Image:
    """裁剪图片使其最大高度不超过指定值。

    Args:
        image (Image.Image): 原始图像 (PIL.Image 对象)
        max_height (int): 最大允许高度(像素)

    Returns:
        Image.Image: 裁剪后的图像
    """
    width, height = image.size
    if height <= max_height:
        return image
    cropped_image = image.crop((0, 0, width, max_height))
    return cropped_image
