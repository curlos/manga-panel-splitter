import flet as ft
import pdb
from utils import construct_directory_structure, get_last_directory, is_image_file
import os
from pprint import pprint


class MagiPanelByPanelView(ft.Container):
    def __init__(self, parent_gui):
        super().__init__()
        self.bgcolor = "#3b4252"

        self.parent_gui = parent_gui
        self.page = self.parent_gui.page
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)
        self.expand = True

        self.pick_directory_container = ft.Container(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.UPLOAD,
                            color="white",
                        ),
                        ft.Text("Pick Directory", color="white", size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor="#3b4252",
                border=ft.border.all(1, "#5e81ac"),
                border_radius=ft.border_radius.all(10),
                alignment=ft.alignment.center,
            ),
            bgcolor="#444c5e",
            on_click=self.open_file_picker_dialog,
            padding=5,
            border_radius=ft.border_radius.all(10),
            height=150,
            alignment=ft.alignment.center,
        )

        self.files_directory_panel_list = self.get_default_files_directory_panel_list()

        self.files_list_container = ft.Container(
            content=ft.Container(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Files List", color="white", size=14),
                                    ft.IconButton(
                                        ft.Icons.CLOSE,
                                        icon_color="white",
                                        icon_size=16,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.ListView(
                                controls=[
                                    self.files_directory_panel_list,
                                ],
                                expand=True,
                            ),
                        ]
                    ),
                    alignment=ft.alignment.top_left,
                ),
                bgcolor="#3b4252",
                border=ft.border.all(1, "#5e81ac"),
                border_radius=ft.border_radius.all(10),
                alignment=ft.alignment.center,
                padding=10,
            ),
            bgcolor="#444c5e",
            padding=5,
            border_radius=ft.border_radius.all(10),
            expand=True,
            alignment=ft.alignment.top_left,
        )

        self.content = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(controls=[self.pick_directory_container], expand=True),
                    ft.Column(controls=[self.files_list_container], expand=True),
                ],
                expand=True,
                spacing=5,
            ),
            margin=ft.margin.symmetric(horizontal=10),
        )

    def get_default_files_directory_panel_list(self):
        return ft.Column(
            controls=[
                ft.ExpansionTile(
                    title=ft.Text("Dragon Ball (Official Colored)"),
                    maintain_state=True,
                    text_color="white",
                    tile_padding=ft.padding.only(left=0, top=0, right=0, bottom=0),
                    controls_padding=ft.padding.only(left=0, top=0, right=0, bottom=0),
                    controls=[
                        ft.ExpansionTile(
                            title=ft.Text("Vol. 19 Ch. 220 - A Faint Light"),
                            maintain_state=True,
                            text_color="white",
                            controls=[
                                ft.ListTile(
                                    title=ft.Text(f"{i}.jpg", size=14),
                                    dense=True,
                                    content_padding=ft.padding.only(
                                        left=20, top=0, right=0, bottom=0
                                    ),
                                    bgcolor="#444c5e",
                                )
                                for i in range(4)
                            ],
                            tile_padding=ft.padding.only(
                                left=20, top=0, right=0, bottom=0
                            ),
                        )
                        for _ in range(5)
                    ],
                )
            ]
        )

    def get_file_row(self, name, size):
        return ft.Container(
            content=ft.Row(
                controls=[ft.Text(name), ft.Text(size)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#444c5e",
            padding=ft.padding.only(left=15, top=7, right=7, bottom=7),
        )

    def open_file_picker_dialog(self, e):
        self.pick_files_dialog.get_directory_path()

    def pick_files_result(self, e):
        absolute_path = e.path
        relative_path = get_last_directory(e.path)

        directory_structure = construct_directory_structure(absolute_path)

        pprint(directory_structure)
        # pdb.set_trace()

        expansion_tiles = self.build_expansion_tiles(directory_structure)

        self.files_directory_panel_list.controls = expansion_tiles
        self.files_directory_panel_list.update()

    def build_expansion_tiles(self, structure):
        def create_tiles(level, i):
            tiles = []
            for key, value in level.items():
                if key == "__images__":
                    # Create ListTiles for images
                    tiles.extend(
                        [
                            ft.ListTile(
                                title=ft.Text(img, size=14),
                                dense=True,
                                content_padding=ft.padding.only(
                                    left=i * 10, top=0, right=0, bottom=0
                                ),
                                bgcolor="#444c5e",
                            )
                            for img in value
                        ]
                    )
                else:
                    # Recursively create nested tiles for directories
                    nested_tiles = create_tiles(value, i + 1)
                    tiles.append(
                        ft.ExpansionTile(
                            title=ft.Text(key),
                            maintain_state=True,
                            text_color="white",
                            controls=nested_tiles,  # Add children here
                            tile_padding=ft.padding.only(
                                left=i * 10, top=0, right=0, bottom=0
                            ),
                        )
                    )
            return tiles

        return create_tiles(structure, 1)