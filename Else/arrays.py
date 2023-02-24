from indeapth import func


class Phone_Camera:
    list = None
    megaPixels = None
    apperature = None
    image_center_size_ = None
    pixel_size_ = None

    def __init__(self, URL):
        self.list = func(URL)
        self.megaPixels = self.list[0]
        self.apperature = self.list[1]
        try:
            self.image_center_size_ = self.list[2]
            self.pixel_size_ = self.list[3]
        except IndexError:
            self.image_center_size_ = None
            self.pixel_size_ = None





