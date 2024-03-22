from gradio import Column, Row, Slider, Checkbox
from PIL.Image import Image as pil_image
from gradio import on
from PIL.ImageEnhance import Brightness, Contrast
from PIL.Image import Transpose


class ImageEditBlock:
    def __init__(self) -> None:
        self.enhancement_column = Column()

        self.brightness_slider = Slider(
            minimum=0.0,
            maximum=10.0,
            value=1.0,
            step=0.5,
            label="Image Brightness",
            interactive=True,
        )
        self.enhancement_column.add(self.brightness_slider)

        self.contrast_slider = Slider(
            minimum=0.0,
            maximum=10.0,
            value=1.0,
            step=0.5,
            label="Image Contrast",
            interactive=True,
        )
        self.enhancement_column.add(self.contrast_slider)

        self.image_transformation_row = Row()

        self.flip_horizontal_checkbox = Checkbox(
            value=False, label="Flip Horizontal", interactive=True
        )
        self.image_transformation_row.add(self.flip_horizontal_checkbox)

        self.to_vertical_checkbox = Checkbox(
            value=False, label="To Vertical", interactive=True
        )
        self.image_transformation_row.add(self.to_vertical_checkbox)

        self.flip_vertical_checkbox = Checkbox(
            value=False, label="Flip Vertical", interactive=True
        )
        self.image_transformation_row.add(self.to_vertical_checkbox)

    def render(self) -> None:
        self.brightness_slider.render()
        self.contrast_slider.render()
        self.flip_horizontal_checkbox.render()
        self.to_vertical_checkbox.render()
        self.flip_vertical_checkbox.render()

    def attach_event(self, input_image, output_image) -> None:
        @on(
            triggers=[
                self.brightness_slider.release,
                self.contrast_slider.release,
            ],
            inputs=[
                input_image,
                self.brightness_slider,
                self.contrast_slider,
            ],
            outputs=output_image,
            show_progress="hidden",
        )
        def image_enhancement_change(
            image: pil_image, brightness: float, contrast: float
        ) -> pil_image:
            image = Brightness(image).enhance(brightness)
            image = Contrast(image).enhance(contrast)

            return image

        @on(
            triggers=[
                self.flip_horizontal_checkbox.select,
                self.to_vertical_checkbox.select,
                self.flip_vertical_checkbox.select,
            ],
            inputs=[
                input_image,
                self.flip_horizontal_checkbox,
                self.to_vertical_checkbox,
                self.flip_vertical_checkbox,
            ],
            outputs=output_image,
            show_progress="hidden",
        )
        def image_transform_change(
            image: pil_image,
            is_flip_horizontal: bool,
            is_to_vertical: bool,
            is_flip_vertical: bool,
        ) -> pil_image:
            is_vertical_operation = not is_flip_horizontal

            if is_vertical_operation:
                if is_to_vertical:
                    image = image.transpose(Transpose.ROTATE_90)

                if is_flip_vertical:
                    image = image.transpose(Transpose.FLIP_TOP_BOTTOM)
            else:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT)

            return image
