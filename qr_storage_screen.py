import os
import shutil
from datetime import datetime

from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast


QR_DIR = "qrcodes"


def _get_qr_files():
    """Return list of (filename, filepath, datetime) sorted newest first."""
    if not os.path.isdir(QR_DIR):
        return []
    files = []
    for name in os.listdir(QR_DIR):
        if name.lower().endswith(".png"):
            path = os.path.join(QR_DIR, name)
            mtime = os.path.getmtime(path)
            files.append((name, path, datetime.fromtimestamp(mtime)))
    files.sort(key=lambda x: x[2], reverse=True)
    return files


class QrListItem(MDCard):
    """A single row in the QR list."""

    def __init__(self, filename, filepath, created_at, on_download, on_rename, on_delete, **kwargs):
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("padding", [dp(12), dp(10)])
        kwargs.setdefault("spacing", dp(10))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(88))
        kwargs.setdefault("radius", [dp(14)])
        kwargs.setdefault("elevation", 1)
        kwargs.setdefault("ripple_behavior", True)
        super().__init__(**kwargs)

        self.filename = filename
        self.filepath = filepath
        self.on_download_cb = on_download
        self.on_rename_cb = on_rename
        self.on_delete_cb = on_delete

        # ── QR thumbnail ──────────────────────────────────────────────
        thumb = Image(
            source=filepath,
            size_hint=(None, None),
            size=(dp(62), dp(62)),
            allow_stretch=True,
            keep_ratio=True,
        )
        self.add_widget(thumb)

        # ── Title + date block ────────────────────────────────────────
        info = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2),
            size_hint_y=None,
            height=dp(62),
            padding=[dp(4), 0],
        )

        # Display name = filename without extension
        display_name = os.path.splitext(filename)[0]
        self.title_label = MDLabel(
            text=display_name,
            font_style="Subtitle1",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(28),
            shorten=True,
            shorten_from="right",
        )

        date_str = created_at.strftime("%b %d, %Y")
        time_str = created_at.strftime("%I:%M %p")
        date_label = MDLabel(
            text=f"📅 {date_str}    🕐 {time_str}",
            font_style="Caption",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(22),
            theme_text_color="Secondary",
        )

        info.add_widget(self.title_label)
        info.add_widget(date_label)
        self.add_widget(info)

        # ── Spacer ────────────────────────────────────────────────────
        self.add_widget(MDBoxLayout())  # flexible spacer

        # ── Action buttons ────────────────────────────────────────────
        actions = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(0),
            size_hint=(None, None),
            size=(dp(132), dp(48)),
            pos_hint={"center_y": 0.5},
        )

        btn_download = MDIconButton(
            icon="download",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().theme_cls.primary_color,
            icon_size="22sp",
        )
        btn_download.bind(on_release=lambda *a: self.on_download_cb(self.filepath))

        btn_rename = MDIconButton(
            icon="pencil",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().theme_cls.primary_color,
            icon_size="22sp",
        )
        btn_rename.bind(on_release=lambda *a: self.on_rename_cb(self))

        btn_delete = MDIconButton(
            icon="delete",
            theme_text_color="Custom",
            text_color=[0.85, 0.2, 0.2, 1],
            icon_size="22sp",
        )
        btn_delete.bind(on_release=lambda *a: self.on_delete_cb(self))

        actions.add_widget(btn_download)
        actions.add_widget(btn_rename)
        actions.add_widget(btn_delete)
        self.add_widget(actions)


class QrStorageScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self._rename_dialog = None
        self._delete_dialog = None
        self._pending_item = None  # item being renamed / deleted

        root = MDBoxLayout(orientation="vertical")

        root.add_widget(
            MDTopAppBar(
                title="Storage",
                left_action_items=[["arrow-left", lambda x: self.app.go_main()]],
            )
        )

        # Scroll container
        self._list_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(12), dp(14), dp(12), dp(14)],
            size_hint_y=None,
        )
        self._list_layout.bind(minimum_height=self._list_layout.setter("height"))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self._list_layout)
        root.add_widget(scroll)

        self.add_widget(root)

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def on_enter(self, *args):
        """Refresh list every time screen becomes visible."""
        self._refresh_list()

    # ── List building ─────────────────────────────────────────────────────

    def _refresh_list(self):
        self._list_layout.clear_widgets()
        files = _get_qr_files()

        if not files:
            placeholder = MDLabel(
                text="No QR codes yet.\nGenerate one on the main screen!",
                halign="center",
                valign="middle",
                theme_text_color="Secondary",
                font_style="Body1",
            )
            self._list_layout.add_widget(placeholder)
            return

        for filename, filepath, created_at in files:
            item = QrListItem(
                filename=filename,
                filepath=filepath,
                created_at=created_at,
                on_download=self._on_download,
                on_rename=self._on_rename_request,
                on_delete=self._on_delete_request,
            )
            self._list_layout.add_widget(item)

    # ── Download ──────────────────────────────────────────────────────────

    def _on_download(self, filepath):
        dest_dir = os.path.expanduser("~/Desktop")
        dest = os.path.join(dest_dir, os.path.basename(filepath))
        try:
            shutil.copy2(filepath, dest)
            toast(f"Saved to Desktop: {os.path.basename(filepath)}")
        except Exception as e:
            toast(f"Error: {e}")

    # ── Rename ────────────────────────────────────────────────────────────

    def _on_rename_request(self, item: QrListItem):
        self._pending_item = item
        self._rename_field = MDTextField(
            hint_text="New name",
            text=os.path.splitext(item.filename)[0],
            size_hint_x=1,
        )
        self._rename_dialog = MDDialog(
            title="Rename QR code",
            type="custom",
            content_cls=self._rename_field,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda *a: self._rename_dialog.dismiss()),
                MDRaisedButton(text="SAVE", on_release=self._on_rename_confirm),
            ],
        )
        self._rename_dialog.open()

    def _on_rename_confirm(self, *args):
        if not self._pending_item:
            return
        new_name = self._rename_field.text.strip()
        if not new_name:
            toast("Name cannot be empty")
            return

        old_path = self._pending_item.filepath
        ext = os.path.splitext(old_path)[1]
        new_path = os.path.join(QR_DIR, new_name + ext)

        if os.path.exists(new_path) and new_path != old_path:
            toast("A file with that name already exists")
            return

        try:
            os.rename(old_path, new_path)
            toast("Renamed successfully")
        except Exception as e:
            toast(f"Error: {e}")

        self._rename_dialog.dismiss()
        self._pending_item = None
        self._refresh_list()

    # ── Delete ────────────────────────────────────────────────────────────

    def _on_delete_request(self, item: QrListItem):
        self._pending_item = item
        self._delete_dialog = MDDialog(
            title="Delete QR code",
            text=f'Are you sure you want to delete "{os.path.splitext(item.filename)[0]}"?',
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda *a: self._delete_dialog.dismiss()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=[0.85, 0.2, 0.2, 1],
                    on_release=self._on_delete_confirm,
                ),
            ],
        )
        self._delete_dialog.open()

    def _on_delete_confirm(self, *args):
        if not self._pending_item:
            return
        try:
            os.remove(self._pending_item.filepath)
            toast("Deleted")
        except Exception as e:
            toast(f"Error: {e}")

        self._delete_dialog.dismiss()
        self._pending_item = None
        self._refresh_list()
