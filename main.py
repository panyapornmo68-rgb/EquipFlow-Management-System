import sys
from PySide6.QtWidgets import QApplication
from app.storage import JSONStorage
from app.services import RentalService
from app.ui import MainWindow, LoginWindow

def main():
    app = QApplication(sys.argv)
    
    storage = JSONStorage("data/inventory.json")
    history_storage = JSONStorage("data/history.json")
    service = RentalService(storage, history_storage) 

    while True:
        login = LoginWindow()
        if login.exec() == LoginWindow.Accepted:
            window = MainWindow(service, login.get_role(), login.user_input.text())
            window.show()
            app.exec() 
            if not getattr(window, 'is_logout', False): break 
        else: break
    
if __name__ == "__main__":
    main()