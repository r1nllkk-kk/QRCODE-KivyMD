from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from color_dropdown import ColorDropdown

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

        root = MDBoxLayout(orientation="vertical")

        root.add_widget(MDTopAppBar(title="Settings", left_action_items=[["arrow-left", lambda x: self.app.go_main()]]))

        content = MDBoxLayout(orientation="vertical", padding=20, spacing=16)

        # Налаштування теми застосунку
        theme_card = MDCard(
            padding=16,
            radius=[16],
            elevation=2,
            size_hint_y=None,
            height=80
        )
        theme_layout = MDBoxLayout(orientation="horizontal", spacing=16)
        
        theme_label = MDLabel(
            text="Theme",
            font_style="Subtitle1",
            halign="left"
        )
        theme_btn = MDRaisedButton(
            text="Toggle Theme",
            size_hint_x=None,
            width=140,
            pos_hint={"center_y": 0.5}
        )
        theme_btn.bind(on_release=lambda *args: self.toggle_theme())
        
        theme_layout.add_widget(theme_label)
        theme_layout.add_widget(theme_btn)
        theme_card.add_widget(theme_layout)
        content.add_widget(theme_card)

        # Налаштування кольору QR-коду
        color_card = MDCard(
            padding=16,
            radius=[16],
            elevation=2,
            size_hint_y=None,
            height=80
        )
        color_layout = MDBoxLayout(orientation="horizontal", spacing=16)
        
        color_label = MDLabel(
            text="QR Color",
            font_style="Subtitle1",
            halign="left"
        )
        color_btn = ColorDropdown(
            update_color_callback=self.app.set_qr_color,
            size_hint_x=None,
            width=120,
            pos_hint={"center_y": 0.5}
        )
        
        color_layout.add_widget(color_label)
        color_layout.add_widget(color_btn)
        color_card.add_widget(color_layout)
        content.add_widget(color_card)

        # Збереження налаштувань
        save_btn = MDRaisedButton(
            text="Save Settings",
            size_hint_y=None,
            height=48,
            pos_hint={"center_x": 0.5}
        )

        save_btn.bind(on_release=self.on_save)

        content.add_widget(save_btn)

        root.add_widget(content)

        self.add_widget(root)

    def on_save(self, *args):
        self.app.settings_store.save(
            theme_style=self.app.theme_cls.theme_style,
            qr_color=self.app.current_qr_color
        )

    def toggle_theme(self):
        self.app.theme_cls.theme_style = "Dark" if self.app.theme_cls.theme_style == "Light" else "Light"
        self.app.settings_store.save(
            theme_style=self.app.theme_cls.theme_style,
            qr_color=self.app.current_qr_color
        )
