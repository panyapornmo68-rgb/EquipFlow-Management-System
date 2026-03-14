import json
import os

class JSONStorage:
    def __init__(self, filename="data/inventory.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save_data(self, data):
        """บันทึกข้อมูลลงไฟล์ JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def load_data(self):
        """โหลดข้อมูลจากไฟล์ JSON"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading: {e}")
            return []