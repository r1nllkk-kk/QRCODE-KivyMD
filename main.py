from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar


from color_dropdown import ColorDropdown
from link_input import LinkInput
from generate_qr_button import GenerateQrButton
from settings_store import SettingsStore
from settings_screen import SettingsScreen
from qr_storage_screen import QrStorageScreen



class QrCodeApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        
        # Initialize settings store and load saved settings
        self.settings_store = SettingsStore()
        settings = self.settings_store.load()
        self.theme_cls.theme_style = settings.get("theme_style", "Light")
        self.current_qr_color = settings.get("qr_color", "black")
        
        # Create screen manager
        self.screen_manager = MDScreenManager()
        
        # Create main screen
        self.main_screen = MDScreen(name="main")
        
        # Add toolbar with settings button
        toolbar = MDTopAppBar(
            title="Menu",
            right_action_items=[["cog", lambda x: self.go_settings()], ["database", lambda x: self.go_qr_storage()]]
        )
        self.main_screen.add_widget(toolbar)

        layout = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20,
            size_hint=(0.9, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.bind(minimum_height=layout.setter("height"))

        self.text_input = LinkInput()
        layout.add_widget(self.text_input)

        color_btn = ColorDropdown(update_color_callback=self.set_qr_color)
        layout.add_widget(color_btn)

        self.qr_image = Image(source="", size_hint_y=None, height=240, allow_stretch=True)
        layout.add_widget(self.qr_image)

        generate_btn = GenerateQrButton(link_input=self.text_input, qr_image=self.qr_image)
        layout.add_widget(generate_btn)
        self.generate_btn = generate_btn

        self.main_screen.add_widget(layout)
        self.screen_manager.add_widget(self.main_screen)
        
        # Create settings screen
        self.settings_screen = SettingsScreen(name="settings")
        self.screen_manager.add_widget(self.settings_screen)

        # Create qr storage screen
        self.qr_storage_screen = QrStorageScreen(name="qr_storage")
        self.screen_manager.add_widget(self.qr_storage_screen)

        return self.screen_manager

    def set_qr_color(self, color_name: str):
        self.current_qr_color = color_name
        if hasattr(self, "generate_btn") and self.generate_btn is not None:
            self.generate_btn.set_qr_color(color_name)

    def go_settings(self):
        self.screen_manager.current = "settings"

    def go_main(self):
        self.screen_manager.current = "main"

    def go_qr_storage(self):
        self.screen_manager.current = "qr_storage"


if __name__ == "__main__":
    QrCodeApp().run()
