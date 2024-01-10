import os
import sys


class RelativePath:
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        final_path = os.path.join(base_path, relative_path)
        return final_path.replace("/", os.path.sep)
