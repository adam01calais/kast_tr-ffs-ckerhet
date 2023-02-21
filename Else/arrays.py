from indeapth import func


class phone_camera():
    list = func("https://en.wikipedia.org/wiki/OnePlus_8")
    megaPixles = list[0]
    apperature = list[1]
    image_center_size = list[2]
    pixle_size = list[3]

onePlus8 = phone_camera()
