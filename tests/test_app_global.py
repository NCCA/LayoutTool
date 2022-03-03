import unittest

from lt import app_global


class Test_App_Global(unittest.TestCase):
    def setUp(self):
        "setup dummy env and save to json"
        app = app_global.AppGlobal()
        app.width = 1000
        app.height = 800
        app.step = 0.1
        self.assertTrue(app.save("testScene.json"))

    def tearDown(self):
        print("Teardown")

    def test_ctor(self):
        app = app_global.AppGlobal()
        self.assertEqual(app.width, 0)
        self.assertEqual(app.height, 0)
        self.assertEqual(app.steps, 0)

    def test_load(self):
        app = app_global.AppGlobal().from_file("testScene.json")
        self.assertEqual(app.width, 1000)
        self.assertEqual(app.height, 800)
        self.assertEqual(app.step, 0.1)
