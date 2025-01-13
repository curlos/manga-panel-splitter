import flet as ft
from classes.PickInputAndOutputDirectories import PickInputAndOutputDirectories
import os
from utils import get_last_two_directories, remove_last_directory
from waifu2x import upscale_with_waifu2x


class UpscaleImagesView(ft.Container):
    def __init__(self, parent_gui):
        super().__init__()
        self.bgcolor = "#3b4252"
        self.expand = True

        self.pick_input_output_directories_container = PickInputAndOutputDirectories(
            on_submit=self.handle_upscale_images, parent_gui=parent_gui
        )

        self.content = self.pick_input_output_directories_container

    def handle_upscale_images(self, e):
        input_directory = self.pick_input_output_directories_container.input_directory
        output_directory = self.pick_input_output_directories_container.output_directory

        if not input_directory and not output_directory:
            self.parent_gui.terminal_output.update_terminal_with_error_message(
                "ERROR: Please enter valid input and output directories."
            )
            return
        elif not input_directory:
            self.parent_gui.terminal_output.update_terminal_with_error_message(
                "ERROR: Please enter a valid input directory."
            )
            return
        elif not output_directory:
            self.parent_gui.terminal_output.update_terminal_with_error_message(
                "ERROR: Please enter a valid output directory."
            )
            return

        files_directory_structure = (
            self.pick_input_output_directories_container.files_directory_structure
        )

        self.process_images_in_structure(
            files_directory_structure, remove_last_directory(input_directory)
        )

    def process_images_in_structure(self, structure, base_path=""):
        output_directory = self.pick_input_output_directories_container.output_directory

        def traverse_and_process(level, current_path):
            for key, value in level.items():
                if key == "__images__":
                    img_obj_list = value
                    self.process_list_of_images_waifu_2x(
                        base_path, current_path, output_directory, img_obj_list
                    )
                else:
                    # Traverse nested directories
                    next_path = os.path.join(current_path, key) if current_path else key
                    traverse_and_process(value, next_path)

        # Start the traversal from the root of the structure
        traverse_and_process(structure, base_path)

    def process_list_of_images_waifu_2x(
        self, base_path, current_path, output_directory, img_obj_list
    ):
        # Current path is a directory containing images
        input_directory = os.path.join(base_path, current_path)
        series_and_chapter_name_directory = get_last_two_directories(input_directory)
        replace_existing_image = False
        upscale_ratio = self.page.client_storage.get("upscale_ratio")

        for img_obj in img_obj_list:
            file_name = img_obj["name"]

            input_image = f"{input_directory}/{file_name}"
            output_image = input_image

            if not replace_existing_image:
                full_image_output_directory = (
                    f"{output_directory}/{series_and_chapter_name_directory}"
                )
                os.makedirs(full_image_output_directory, exist_ok=True)
                output_image = f"{full_image_output_directory}/{file_name}"

            upscale_with_waifu2x(
                input_image=input_image,
                output_image=output_image,
                upscale_ratio=upscale_ratio,
            )