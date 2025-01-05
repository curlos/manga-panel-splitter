import flet as ft


class AppBarButton(ft.TextButton):
    def __init__(self, text, current_view, change_view):
        super().__init__()
        self.text = text
        self.on_click = lambda e: change_view(text)
        self.set_button_style_by_view(current_view)

    def set_button_style_by_view(self, current_view):
        self.style = ft.ButtonStyle(
            bgcolor=(
                "#5e81ac" if current_view == self.text else ft.Colors.BLUE_GREY_800
            ),
            color="white",
            shape={
                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=0),
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=0),
            },
        )


class AppBar(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.current_view = "MangaDex Downloader"

        # Define the buttons
        self.mangadex_button = AppBarButton(
            text="MangaDex Downloader",
            current_view=self.current_view,
            change_view=self.change_view,
        )

        self.panel_button = AppBarButton(
            text="Panel-By-Panel",
            current_view=self.current_view,
            change_view=self.change_view,
        )

        self.bgcolor = ft.Colors.BLUE_GREY_800
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        self.mangadex_button,
                        self.panel_button,
                    ]
                ),
                ft.IconButton(ft.icons.MENU, on_click=lambda e: page.navigation.open()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )

    # Function to change the view and update the button styles
    def change_view(self, view_name):
        self.current_view = view_name

        # Update button styles dynamically
        self.mangadex_button.style = ft.ButtonStyle(
            bgcolor=(
                "#5e81ac"
                if self.current_view == "MangaDex Downloader"
                else ft.Colors.BLUE_GREY_800
            ),
            color="white",
        )

        self.panel_button.style = ft.ButtonStyle(
            bgcolor=(
                "#5e81ac"
                if self.current_view == "Panel-By-Panel"
                else ft.Colors.BLUE_GREY_800
            ),
            color="white",
        )

        self.page.update()  # Refresh the UI
