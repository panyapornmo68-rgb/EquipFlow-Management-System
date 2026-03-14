from abc import ABC, abstractmethod
from datetime import datetime

class Equipment(ABC):
    def __init__(self, eq_id, name, status="Available", borrow_date=None, borrower=None):
        self.id = eq_id
        self.name = name
        self.__status = status
        self.borrow_date = borrow_date 
        self.borrower = borrower
        self.DAILY_RATE = 50
        self.MAX_BORROW_DAYS = 7

    def calculate_fine(self):
        """คำนวณค่าปรับตามระยะเวลาที่ผ่านไป"""
        if not self.borrow_date:
            return 0
        
        start_date = datetime.strptime(self.borrow_date, "%Y-%m-%d %H:%M")
        now = datetime.now()
        
        duration = now - start_date
        
        if duration.days > self.MAX_BORROW_DAYS:
            overdue_days = duration.days - self.MAX_BORROW_DAYS
            return overdue_days * self.DAILY_RATE
        
        return 0

    @property
    def status(self):
        return self.__status

    def check_out(self, borrower_name):
        self.__status = "Rented"
        self.borrower = borrower_name
        self.borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def return_item(self):
        self.__status = "Available"
        self.borrower = None
        self.borrow_date = None

    @abstractmethod
    def to_dict(self):
        """Method สำหรับแปลง Object เป็น Dictionary เพื่อเซฟลง JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "borrow_date": self.borrow_date,
            "borrower": self.borrower
        }

class ITEquipment(Equipment):
    def __init__(self, eq_id, name, specs, status="Available", borrow_date=None):
        super().__init__(eq_id, name, status, borrow_date)
        self.specs = specs
    def get_category(self): return "IT Device"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "borrow_date": self.borrow_date,
            "borrower": self.borrower,
            "type": "IT",
            "specs": self.specs
        }

class ToolEquipment(Equipment):
    def __init__(self, eq_id, name, material, status="Available", borrow_date=None):
        super().__init__(eq_id, name, status, borrow_date)
        self.material = material
    def get_category(self): return "Tool"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "borrow_date": self.borrow_date,
            "borrower": self.borrower,
            "type": "Tool",
            "material": self.material
        }

class TransactionLog:
    def __init__(self, eq_id, eq_name, username, action, timestamp=None):
        self.eq_id = eq_id
        self.eq_name = eq_name
        self.username = username
        self.action = action
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "eq_id": self.eq_id,
            "eq_name": self.eq_name,
            "username": self.username,
            "action": self.action,
            "timestamp": self.timestamp
        }