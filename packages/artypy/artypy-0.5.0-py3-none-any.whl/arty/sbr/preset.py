import os

# TODO: Add loading and saving functions
# TODO: Handle paths appropriately

class Preset:
    def __init__(self, img_path="../_demo/images/img.png", palette_size=10, stroke_scale=0, length_scale=1 / 3,
                 gradient_smoothing_radius=0, brush_type="circle", length="base", length_first_flag=True,
                 gradient_type="sharr", gradient_smoothing_type="gaussian", smoothing_iterations=1, grid_scale=3, grayscale=False, has_cardboard=False):
        self.img_path = img_path
        self.palette_size = palette_size
        self.stroke_scale = stroke_scale
        self.gradient_smoothing_radius = gradient_smoothing_radius
        self.brush_type = brush_type
        self.length = length
        self.length_first_flag = length_first_flag
        file_names = [int(file_name.split(".")[0]) for file_name in os.listdir(f"sbr/{str(self.brush_type)}")]

        if len(file_names) == 0:
            file_names = [-1]

        self.img_save_path = os.path.join(f"sbr/{str(self.brush_type)}/{str(max(file_names) + 1)}.jpg")
        self.preset_save_path = f"../configs/presets/sbr/{str(self.brush_type)}/{str(max(file_names) + 1)}.yaml"
        self.length_scale = length_scale
        self.gradient_type = gradient_type
        self.gradient_smoothing_type = gradient_smoothing_type
        self.smoothing_iterations = smoothing_iterations
        self.grid_scale = grid_scale
        self.grayscale = grayscale
        self.has_cardboard = has_cardboard