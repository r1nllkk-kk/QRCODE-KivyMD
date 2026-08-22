from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast

import os
import qrcode
from datetime import datetime

class GenerateQrButton(MDRaisedButton):
    def __init__(self, link_input, qr_image, **kwargs):
        kwargs.setdefault("text", "Generate QR")
        kwargs.setdefault("pos_hint", {"center_x": 0.5})
        super().__init__(**kwargs)
        self.link_input = link_input
        self.qr_image = qr_image
        self.current_qr_color = "black"
        self.bind(on_release=self.generate_qr)

    def set_qr_color(self, color_name: str):
        self.current_qr_color = color_name


    def generate_qr(self, *args):
        data = self.link_input.get_value()
        if not data:
            toast("Please paste your URL")
            return
        self.generate_qr_to_image(data, self.current_qr_color)

    def generate_qr_to_image(self, data: str, color_name: str):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=color_name, back_color="white")

        out_dir = "qrcodes"
        os.makedirs(out_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(out_dir, f"qr_{timestamp}.png")

        img.save(out_path)

        self.qr_image.texture = None
        self.qr_image.source = out_path

        toast("QR generated successfully")
