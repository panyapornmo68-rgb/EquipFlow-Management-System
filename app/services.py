import random
from .models import ITEquipment, ToolEquipment, TransactionLog

class RentalService:
    def __init__(self, storage, history_storage):
        self.storage = storage
        self.history_storage = history_storage
        self.inventory = self._load_initial_data()
        self.history = self._load_history()

    def _load_history(self):
        raw_history = self.history_storage.load_data()
        return [TransactionLog(**item) for item in raw_history]
    
    def log_transaction(self, equipment, username, action):
        """บันทึกประวัติใหม่และเซฟลงไฟล์ทันที"""
        new_log = TransactionLog(equipment.id, equipment.name, username, action)
        self.history.append(new_log)
        
        history_data = [log.to_dict() for log in self.history]
        self.history_storage.save_data(history_data)

    
    def _load_initial_data(self):
        raw_data = self.storage.load_data()
        objects = []
        
        if not raw_data:
            return []

        for item in raw_data:
            b_date = item.get('borrow_date')
            b_user = item.get('borrower')

            if item.get('type') == 'IT':
                obj = ITEquipment(item['id'], item['name'], item.get('specs', ""), item['status'], b_date)
            else:
                obj = ToolEquipment(item['id'], item['name'], item.get('material', ""), item['status'], b_date)

            obj.borrower = b_user
            objects.append(obj)
            
        return objects
    
    def add_equipment(self, eq_type, eq_id, name, extra_info):
        if not eq_id:
            prefix = "IT" if eq_type == "IT" else "TL"
            while True:
                rand_id = f"{prefix}{random.randint(100, 999)}"
                if not any(i.id == rand_id for i in self.inventory):
                    eq_id = rand_id
                    break

        new_item = ITEquipment(eq_id, name, extra_info) if eq_type == "IT" else ToolEquipment(eq_id, name, extra_info)
        self.inventory.append(new_item)
        self._save_all()
        return new_item

    def delete_equipment(self, eq_id):
        self.inventory = [i for i in self.inventory if i.id != eq_id]
        self._save_all()

    def get_all_items(self):
        return self.inventory

    def _save_all(self):
        data_to_save = [item.to_dict() for item in self.inventory]
        self.storage.save_data(data_to_save)