import pathlib
import streamlit as st
import os

class ResourceManager:
    def __init__(self):
        self.base_dir = pathlib.Path(__file__).parent.parent.absolute()
        self.image_dir = self.base_dir / "images"
        #self.font_dir = self.base_dir / "fonts"
        self.paths = {
            "MauDonXin": self.image_dir / "inspection01.png",  # Kiểm tra lại tên file
            #"Font": self.font_dir / "HANDotum.ttf",  # Kiểm tra lại tên file
            #"FontDam": self.font_dir / "HANDotumB.ttf"  # Kiểm tra lại tên file
        }
        print(f"Đường dẫn MauDonXin: {self.paths['MauDonXin']}")  # Thêm dòng này
    def validate_resources(self):
        missing_files = []
        for name, path in self.paths.items():
            if not os.path.exists(path):
                missing_files.append(f"{name}: {path}")

        if missing_files:
            error_msg = "Không tìm thấy các file sau:\n" + "\n".join(missing_files)
            st.error(error_msg)
            raise FileNotFoundError(error_msg)

    def get_path(self, resource_name):
        path = self.paths.get(resource_name)
        if not path:
            raise KeyError(f"Không tìm thấy tài nguyên: {resource_name}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Không tìm thấy file: {path}")
        return path