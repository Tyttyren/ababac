import cv2
import os
import sys
import datetime
from generate_license_plate_number import LicensePlateNoGenerator
from generate_chars_image import CharsImageGenerator
from generate_plate_template import LicensePlateImageGenerator
from augment_image import ImageAugmentation

from PIL import Image

if __name__=="__main__":
    plate_type = 'single_blue'
    batch_size = 100
   # 生成车牌号
    license_plate_no_generator = LicensePlateNoGenerator(plate_type)
    plate_nums = license_plate_no_generator.generate_license_plate_numbers(batch_size)
    # 生成车牌号图片：白底黑字
    chars_image_generator = CharsImageGenerator(plate_type)
    chars_images = chars_image_generator.generate_images(plate_nums)
    # 生成车牌底牌
    license_template_generator = LicensePlateImageGenerator(plate_type)
    template_image = license_template_generator.generate_template_image(chars_image_generator.plate_width,
                                                                            chars_image_generator.plate_height)
    augmentation = ImageAugmentation(plate_type, template_image)
    Image.fromarray(template_image).show()
