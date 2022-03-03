import json


class AppGlobal:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.steps = 0

    def save(self, filename: str) -> bool:

        app_file = {}
        scene_data = {}
        scene_data["width"] = self.width
        scene_data["height"] = self.height
        scene_data["steps"] = self.steps
        app_file["SceneData"] = scene_data
        app_file["AppData"] = {}
        with open(filename, "w") as outfile:
            json.dump(app_file, indent=4, fp=outfile)

        return True

    @classmethod
    def from_file(self, filename: str):
        app = AppGlobal()
        with open(filename) as json_file:
            scene_data = json.load(json_file)
            app.width = scene_data["SceneData"]["width"]
            app.height = scene_data["SceneData"]["height"]
            app.step = scene_data["SceneData"]["steps"]
        return app
