import flet as ft
from classes.SettingsBase import SettingsBase
from TextToSpeech import TextToSpeech


class SettingsImagesToVideo(
    SettingsBase,
):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.tts = TextToSpeech(self.page.client_storage)
        self.locale_voice_mapping = self.tts.get_locale_voice_mapping()

        self.azure_voice_pitch_options = ["x-low", "low", "medium", "high", "x-high"]
        self.azure_voice_rate_options = ["x-slow", "slow", "medium", "fast", "x-fast"]
        self.azure_voice_volume_options = [
            "silent",
            "x-soft",
            "soft",
            "medium",
            "loud",
            "x-loud",
        ]

        self.video_height_textfield = self.get_number_textfield(
            "Video Height (px)", "video_height"
        )

        # Reading Speed
        self.reading_speed_wpm_textfield = self.get_number_textfield(
            "Reading Speed (WPM)", "reading_speed_wpm"
        )

        self.reading_speed_wpm_col = ft.Column(
            controls=[
                self.reading_speed_wpm_textfield,
            ],
            visible=bool(self.page.client_storage.get("use_reading_speed_wpm")),
        )

        self.radio_use_reading_speed_wpm = ft.Radio(
            label="Use Reading Speed (WPM)",
            value="use_reading_speed_wpm",
        )

        # Image Displayed Duration
        self.image_displayed_duration_textfield = self.get_number_textfield(
            "Image Displayed Duration (sec.)", "image_displayed_duration"
        )

        self.image_displayed_duration_col = ft.Column(
            controls=[
                self.image_displayed_duration_textfield,
            ],
            visible=bool(self.page.client_storage.get("use_image_displayed_duration")),
        )

        self.radio_use_image_displayed_duration = ft.Radio(
            label="Use Image Displayed Duration (sec.)",
            value="use_image_displayed_duration",
        )

        # Text-To-Speech (Azure)
        self.image_pre_tts_audio_delay_textfield = self.get_number_textfield(
            "Image Pre-TTS Audio Delay (seconds)",
            "image_pre_tts_audio_delay",
        )

        self.image_post_tts_audio_delay_textfield = self.get_number_textfield(
            "Image Post-TTS Audio Delay (seconds)",
            "image_post_tts_audio_delay",
        )

        self.azure_subscription_key_textfield = ft.TextField(
            label="Azure Subscription Key",
            border_color="#5e81ac",
            password=True,
            can_reveal_password=True,
            value=self.page.client_storage.get("azure_subscription_key"),
            on_change=lambda e: self.change_setting("azure_subscription_key", e.data),
        )

        self.azure_region_textfield = ft.TextField(
            label="Azure Region",
            border_color="#5e81ac",
            value=self.page.client_storage.get("azure_region"),
            on_change=lambda e: self.change_setting("azure_region", e.data),
        )

        default_locale = self.get_setting_value("azure_voice_locale", "en-US")

        default_voice_dict = self.locale_voice_mapping[default_locale]
        default_voice_short_names = default_voice_dict.keys()
        default_voice_short_names_list = list(default_voice_dict.keys())
        default_voice_name = (
            self.page.client_storage.get("azure_voice_name")
            or default_voice_short_names_list[0]
        )

        default_azure_voice_volume = self.get_setting_value(
            "azure_voice_volume", "x-loud"
        )
        default_azure_voice_rate = self.get_setting_value("azure_voice_rate", "medium")
        default_azure_voice_pitch = self.get_setting_value(
            "azure_voice_pitch", "medium"
        )

        self.voice_locale_dropdown = ft.Dropdown(
            label="Voice Locale",
            options=[
                ft.dropdown.Option(locale)
                for locale in sorted(self.locale_voice_mapping.keys())
            ],
            value=default_locale,
            text_style=ft.TextStyle(
                color="white",  # Text color of the selected item
                size=14,  # Font size
            ),
            fill_color="#3b4252",  # Background color of the dropdown
            border_color="#5e81ac",
            max_menu_height=300,
            on_change=self.handle_voice_locale_change,
        )

        self.voice_names_dropdown = ft.Dropdown(
            label="Voice Names",
            options=[
                ft.dropdown.Option(voice_short_name)
                for voice_short_name in default_voice_short_names
            ],
            value=default_voice_name,
            text_style=ft.TextStyle(
                color="white",  # Text color of the selected item
                size=14,  # Font size
            ),
            fill_color="#3b4252",  # Background color of the dropdown
            border_color="#5e81ac",
            max_menu_height=300,
            on_change=lambda e: self.change_setting("azure_voice_name", e.data),
        )

        self.voice_volume_options_dropdown = ft.Dropdown(
            label="Voice Volume",
            options=[
                ft.dropdown.Option(volume) for volume in self.azure_voice_volume_options
            ],
            value=default_azure_voice_volume,
            text_style=ft.TextStyle(
                color="white",  # Text color of the selected item
                size=14,  # Font size
            ),
            fill_color="#3b4252",  # Background color of the dropdown
            border_color="#5e81ac",
            max_menu_height=300,
            on_change=lambda e: self.change_setting("azure_voice_volume", e.data),
        )

        self.voice_rate_options_dropdown = ft.Dropdown(
            label="Voice Rate",
            options=[
                ft.dropdown.Option(rate) for rate in self.azure_voice_rate_options
            ],
            value=default_azure_voice_rate,
            text_style=ft.TextStyle(
                color="white",  # Text color of the selected item
                size=14,  # Font size
            ),
            fill_color="#3b4252",  # Background color of the dropdown
            border_color="#5e81ac",
            max_menu_height=300,
            on_change=lambda e: self.change_setting("azure_voice_rate", e.data),
        )

        self.voice_pitch_options_dropdown = ft.Dropdown(
            label="Voice Pitch",
            options=[
                ft.dropdown.Option(pitch) for pitch in self.azure_voice_pitch_options
            ],
            value=default_azure_voice_pitch,
            text_style=ft.TextStyle(
                color="white",  # Text color of the selected item
                size=14,  # Font size
            ),
            fill_color="#3b4252",  # Background color of the dropdown
            border_color="#5e81ac",
            max_menu_height=300,
            on_change=lambda e: self.change_setting("azure_voice_pitch", e.data),
        )

        self.text_to_speech_azure_col = ft.Column(
            controls=[
                self.azure_subscription_key_textfield,
                self.azure_region_textfield,
                self.voice_locale_dropdown,
                self.voice_names_dropdown,
                self.voice_volume_options_dropdown,
                self.voice_rate_options_dropdown,
                self.voice_pitch_options_dropdown,
                self.image_pre_tts_audio_delay_textfield,
                self.image_post_tts_audio_delay_textfield,
            ],
            visible=bool(self.page.client_storage.get("use_text_to_speech_azure")),
        )

        self.radio_use_text_to_speech_azure = ft.Radio(
            label="Use Text-To-Speech (Azure)",
            value="use_text_to_speech_azure",
        )

        self.radio_group_dict = {
            "use_reading_speed_wpm": {
                "elem": self.radio_use_reading_speed_wpm,
                "toggle_elem": self.reading_speed_wpm_col,
                "setting_key": "use_reading_speed_wpm",
            },
            "use_image_displayed_duration": {
                "elem": self.radio_use_image_displayed_duration,
                "toggle_elem": self.image_displayed_duration_col,
                "setting_key": "use_image_displayed_duration",
            },
            "use_text_to_speech_azure": {
                "elem": self.radio_use_text_to_speech_azure,
                "toggle_elem": self.text_to_speech_azure_col,
                "setting_key": "use_text_to_speech_azure",
            },
        }

        self.minimum_image_duration_textfield = self.get_number_textfield(
            "Minimum Image Duration (seconds)", "minimum_image_duration"
        )

        self.minimum_image_duration_col = ft.Column(
            controls=[
                self.minimum_image_duration_textfield,
            ],
            visible=bool(self.page.client_storage.get("use_minimum_image_duration")),
        )

        self.page_num_textfield_dict = {
            "video_height": self.video_height_textfield,
            "reading_speed_wpm": self.reading_speed_wpm_textfield,
            "image_displayed_duration": self.image_displayed_duration_textfield,
            "minimum_image_duration": self.minimum_image_duration_textfield,
            "image_pre_tts_audio_delay": self.image_pre_tts_audio_delay_textfield,
            "image_post_tts_audio_delay": self.image_post_tts_audio_delay_textfield,
        }

        self.inner_content = [
            self.video_height_textfield,
            ft.Checkbox(
                label="Use Minimum Image Duration (sec.)",
                value=self.page.client_storage.get("use_minimum_image_duration"),
                on_change=lambda e: self.toggle_setting_element_visibility(
                    e,
                    self.minimum_image_duration_col,
                    "use_minimum_image_duration",
                ),
            ),
            self.minimum_image_duration_col,
            ft.RadioGroup(
                content=ft.Column(
                    controls=[val["elem"] for val in self.radio_group_dict.values()]
                ),
                on_change=lambda e: self.handle_radio_group_change(
                    e, self.radio_group_dict
                ),
                value=self.get_radio_group_init_value(
                    radio_group_dict=self.radio_group_dict
                ),
            ),
            self.reading_speed_wpm_col,
            self.image_displayed_duration_col,
            self.text_to_speech_azure_col,
        ]

        self.content = self.get_full_content()

    def handle_voice_locale_change(self, e):
        self.change_setting("azure_voice_locale", e.data)

        current_locale = self.get_setting_value("azure_voice_locale", "en-US")

        current_voice_dict = self.locale_voice_mapping[current_locale]
        current_voice_short_names = current_voice_dict.keys()
        current_voice_short_names_list = list(current_voice_dict.keys())
        current_voice_name = current_voice_short_names_list[0]

        self.voice_names_dropdown.options = [
            ft.dropdown.Option(voice_short_name)
            for voice_short_name in current_voice_short_names
        ]
        self.voice_names_dropdown.value = current_voice_name
        self.voice_names_dropdown.update()
