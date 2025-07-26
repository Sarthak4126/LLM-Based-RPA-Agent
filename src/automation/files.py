# src/automation/files.py
import os
import shutil
from pathlib import Path

class FileManager:
    @staticmethod
    def create_folder(path: str) -> bool:
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            raise Exception(f"Create folder failed: {str(e)}")

    @staticmethod
    def move_files(source_pattern: str, dest_folder: str) -> int:
        try:
            moved_count = 0
            for file in Path().glob(source_pattern):
                if file.is_file():
                    shutil.move(str(file), dest_folder)
                    moved_count += 1
            return moved_count
        except Exception as e:
            raise Exception(f"Move files failed: {str(e)}")

    @staticmethod
    def save_text(content: str, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            raise Exception(f"Save text failed: {str(e)}")