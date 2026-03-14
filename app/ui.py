from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QComboBox, QLabel, QMessageBox, QDialog, QFrame, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QIcon, QAction
from datetime import datetime, timedelta
import json
import os

STYLE_SHEET = """
    QMainWindow { background-color: #F8FAFC; }
    QLabel { color: #1E293B; font-family: 'Segoe UI', sans-serif; }
    QTableWidget {
        background-color: white; border-radius: 12px; border: 1px solid #E2E8F0;
        gridline-color: #F1F5F9; font-size: 13px;
    }
    QHeaderView::section {
        background-color: #F8FAFC; padding: 12px; border: none;
        border-bottom: 2px solid #E2E8F0; font-weight: bold; color: #64748B;
    }
    QLineEdit { border: 2px solid #E2E8F0; border-radius: 8px; padding: 10px; background: white; }
    QPushButton#AddBtn { background-color: #3B82F6; color: white; border-radius: 8px; font-weight: bold; padding: 10px 20px; }
    QPushButton#AddBtn:hover { background-color: #2563EB; }
"""

class LoginWindow(QDialog):
    Accepted = 1
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login System")
        self.setFixedSize(350, 350)
        self.role = None
        layout = QVBoxLayout(self)
        
        title = QLabel("EquipFlow System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        subtitle = QLabel("กรุณากรอกข้อมูลเพื่อเข้าใช้งาน")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet("background-color: #1E293B; color: white; border-radius: 5px;")
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn)

    def check_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
            
            found_user = next((u for u in users if u['username'] == username and u['password'] == password), None)
            
            if found_user:
                self.role = found_user['role']
                self.accept()
            else:
                QMessageBox.warning(self, "ล้มเหลว", "Username หรือ Password ไม่ถูกต้อง!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"ไม่สามารถโหลดข้อมูลผู้ใช้ได้: {str(e)}")

    def get_role(self): return self.role


class HistoryDialog(QDialog):
    def __init__(self, history_data, role, current_user):
        super().__init__()
        self.setWindowTitle("ประวัติการทำรายการ")
        self.resize(800, 500)
        layout = QVBoxLayout(self)

        title_text = "ประวัติการ ยืม-คืน ของคุณ" if role == "User" else "Log ประวัติการทำรายการทั้งหมด (Admin)"
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #1E293B;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["เวลา", "ID อุปกรณ์", "ชื่ออุปกรณ์", "ผู้ใช้งาน", "กิจกรรม"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        

        if role == "Admin":
            filtered_data = history_data
        else:
            filtered_data = [log for log in history_data if log.username == current_user]

        self.table.setRowCount(len(filtered_data))
        for row, log in enumerate(reversed(filtered_data)):
            self.table.setItem(row, 0, QTableWidgetItem(log.timestamp))
            self.table.setItem(row, 1, QTableWidgetItem(log.eq_id))
            self.table.setItem(row, 2, QTableWidgetItem(log.eq_name))
            self.table.setItem(row, 3, QTableWidgetItem(log.username))
            
            action_item = QTableWidgetItem()
            if log.action == "Borrow":
                action_item.setText("ยืมอุปกรณ์")
                action_item.setForeground(QColor("#3B82F6"))
            else:
                action_item.setText("รับอุปกรณ์คืน")
                action_item.setForeground(QColor("#10B981"))
            
            self.table.setItem(row, 4, action_item)

        layout.addWidget(self.table)
        
        close_btn = QPushButton("ปิดหน้าต่าง")
        close_btn.setMinimumHeight(40)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

class MainWindow(QMainWindow):
    def __init__(self, service, role, username):
        super().__init__()
        self.is_logout = False
        self.service = service
        self.role = role
        self.current_user = username
        self.setWindowTitle(f"Equipment Management - ({self.role})")
        self.resize(1100, 800)
        self.setStyleSheet(STYLE_SHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        self.setup_header()
        self.setup_filters()
        self.setup_table()

        if self.role == "Admin":
            self.setup_admin_panel()

        self.refresh_table()

    def show_history(self):
        history_data = self.service.history 
        dialog = HistoryDialog(history_data, self.role, self.current_user)
        dialog.exec()

    def setup_header(self):
        top_bar = QHBoxLayout()
        title_label = QLabel("รายการอุปกรณ์ทั้งหมด")
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #0F172A;")
        top_bar.addWidget(title_label)
        top_bar.addStretch()
        
        history_btn = QPushButton("ดูประวัติการใช้งาน")
        history_btn.setStyleSheet("background-color: #F1F5F9; border: 1px solid #E2E8F0; padding: 5px 15px;")
        history_btn.clicked.connect(self.show_history)
        top_bar.addWidget(history_btn)

        logout_btn = QPushButton("ออกจากระบบ")
        logout_btn.clicked.connect(self.handle_logout)
        top_bar.addWidget(logout_btn)
        self.main_layout.addLayout(top_bar)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        self.cards_layout.setContentsMargins(0, 10, 0, 10)
        
        self.card_total = self.create_card("อุปกรณ์ทั้งหมด", "#2563EB")
        self.card_available = self.create_card("ว่างพร้อมใช้งาน", "#10B981")
        self.card_rented = self.create_card("ถูกยืมอยู่", "#F59E0B")

        self.card_fine = None
        if self.role == "Admin":
            self.card_fine = self.create_card("เกินกำหนด (ค้างค่าปรับ)", "#EF4444")
        
        self.main_layout.addLayout(self.cards_layout)


    def update_dashboard_stats(self):
        items = self.service.get_all_items()
        total = len(items)
        available = sum(1 for i in items if i.status == "Available")
        rented = total - available
        
        self.card_total.setText(str(total))
        self.card_available.setText(str(available))
        self.card_rented.setText(str(rented))
        
        if self.card_fine is not None:
            fine_count = 0
            for item in items:
                if item.status == "Rented" and item.borrow_date:
                    try:
                        b_date = datetime.strptime(item.borrow_date, "%Y-%m-%d %H:%M")

                        if (datetime.now() - b_date).days > 7:
                            fine_count += 1
                    except: pass
            self.card_fine.setText(str(fine_count))

    def create_card(self, title, color):
        card = QFrame()
        card.setStyleSheet(f"""QFrame {{background-color: white; border-radius: 12px; border: 1px solid #E2E8F0; /* ใส่เส้นขอบบางๆ รอบๆ */s padding: 18px 22px; /* เพิ่ม padding ให้ดูโปร่ง */}}""")
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 500;")
        lbl_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        lbl_value = QLabel("0")
        lbl_value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 700;")
        lbl_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        
        self.cards_layout.addWidget(card)
        return lbl_value

    def handle_logout(self):
        self.is_logout = True
        self.close()

    def setup_admin_panel(self):
        panel = QFrame()
        panel.setStyleSheet
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)

        self.name_in = QLineEdit()
        self.name_in.setPlaceholderText("ระบุชื่ออุปกรณ์ที่ต้องการเพิ่ม...")
        
        self.type_in = QComboBox()
        self.type_in.addItems(["IT Device", "Tool"])
        self.type_in.setFixedWidth(150)
        
        add_btn = QPushButton("เพิ่มอุปกรณ์ใหม่")
        add_btn.setObjectName("AddBtn")
        add_btn.setFixedWidth(150)
        add_btn.clicked.connect(self.add_item)

        layout.addWidget(self.name_in)
        layout.addWidget(QLabel("ประเภท:"))
        layout.addWidget(self.type_in)
        layout.addWidget(add_btn)
        
        self.main_layout.addWidget(panel)

    def setup_filters(self):
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ค้นหาชื่ออุปกรณ์...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.search_input)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["ทั้งหมด", "IT Device", "Tool"])
        self.category_combo.setMinimumWidth(150)
        self.category_combo.currentTextChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.category_combo)
        
        filter_layout.addStretch()
        self.main_layout.addLayout(filter_layout)

    def setup_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "ชื่ออุปกรณ์", "ประเภท", "วันที่ยืม", "สถานะ", "ค่าปรับ", "จัดการ"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.main_layout.addWidget(self.table)

    def refresh_table(self):
        self.update_dashboard_stats()
        items = self.service.get_all_items()
        self.table.setRowCount(0)
        all_items = self.service.get_all_items()
        search_text = self.search_input.text().strip().lower()
        selected_category = self.category_combo.currentText()

        filtered_items = []
        for item in all_items:
            name_match = search_text in item.name.lower() or search_text in item.id.lower()
            category_match = True
            if selected_category == "IT Device":
                category_match = (item.get_category() == "IT Device")
            elif selected_category == "Tool":
                category_match = (item.get_category() == "Tool")
            
            if name_match and category_match:
                filtered_items.append(item)

        self.table.setRowCount(len(filtered_items))
        for row, item in enumerate(filtered_items):
            self.table.setItem(row, 0, QTableWidgetItem(item.id))
            self.table.setItem(row, 1, QTableWidgetItem(item.name))
            self.table.setItem(row, 2, QTableWidgetItem(item.get_category()))
            
            status_item = QTableWidgetItem(item.status)
            if item.status == "Available":
                status_item.setForeground(QColor("#10B981"))
            else:
                status_item.setForeground(QColor("#EF4444"))
            self.table.setItem(row, 3, status_item)
            
            self.table.setItem(row, 4, QTableWidgetItem(item.borrower if item.borrower else "-"))
            self.table.setItem(row, 5, QTableWidgetItem(item.borrow_date if item.borrow_date else "-"))
            
            borrow_date_str = item.borrow_date if item.borrow_date else "-"
            self.table.setItem(row, 3, QTableWidgetItem(borrow_date_str))

            status_text = "ว่าง"
            color = "#10B981"
            
            if item.status == "Rented":
                if getattr(item, 'borrower', None) == self.current_user:
                    status_text = "ยืมแล้ว (โดยคุณ)"
                    color = "#3B82F6"
                else:
                    if self.role == "Admin":
                        borrower_name = getattr(item, 'borrower', 'ไม่ทราบชื่อ')
                        status_text = f"ถูกยืม โดย ({borrower_name})"
                        color = "#F59E0B"
                    else:
                        status_text = "ไม่ว่าง"
                        color = "#EF4444"
            
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(QColor(color))
            status_item.setTextAlignment(Qt.AlignCenter) 
            self.table.setItem(row, 4, status_item)

            fine_text = "-"
            if item.status == "Rented" and item.borrow_date:
                try:
                    b_date = datetime.strptime(item.borrow_date, "%Y-%m-%d %H:%M")
                    days_passed = (datetime.now() - b_date).days
                    if days_passed > 7:
                        fine_text = f"{(days_passed - 7) * 50} ฿"
                except: pass
            self.table.setItem(row, 5, QTableWidgetItem(fine_text))

            actions = QWidget()
            act_lay = QHBoxLayout(actions)
            act_lay.setContentsMargins(5, 2, 5, 2)
            
            if self.role == "User" and item.status == "Available":
                btn = QPushButton("ยืม")
                btn.clicked.connect(lambda chk=False, i=item: self.toggle(i))
                act_lay.addWidget(btn)
                
            if self.role == "Admin":
                if item.status == "Rented":
                    btn = QPushButton("รับของคืน")
                    btn.setStyleSheet("background-color: #c5f0cc; color: #279c3c; border-radius: 4px;")
                    btn.clicked.connect(lambda chk=False, i=item: self.toggle(i))
                    act_lay.addWidget(btn)
                else:
                    del_btn = QPushButton("ลบอุปกรณ์")
                    del_btn.setStyleSheet("background-color: #FEE2E2; color: #EF4444; border: none;")
                    del_btn.clicked.connect(lambda chk=False, id=item.id: self.delete_item(id))
                    act_lay.addWidget(del_btn)

            self.table.setCellWidget(row, 6, actions)

    def add_item(self):
        name = self.name_in.text().strip()
        if name:
            raw_type = self.type_in.currentText()
            final_type = "IT" if "IT" in raw_type else "Tool"
            self.service.add_equipment(final_type, "", name, "")
            self.name_in.clear()
            self.refresh_table()
            QMessageBox.information(self, "สำเร็จ", f"เพิ่ม {name} เข้าสู่ระบบแล้ว (ระบบสุ่ม ID ให้เรียบร้อย)")
        else:
            QMessageBox.warning(self, "แจ้งเตือน", "กรุณากรอกชื่ออุปกรณ์ก่อนกดเพิ่ม!")

    def toggle(self, item):
        if item.status == "Available":
            item.check_out(self.current_user)
            self.service.log_transaction(item, self.current_user, "Borrow")
            QMessageBox.information(self, "สำเร็จ", f"ยืม {item.name} เรียบร้อย")
        else:
            fine = item.calculate_fine()
            
            if fine > 0:
                msg = f"คืนอุปกรณ์ล่าช้า!\nมีค่าปรับที่ต้องชำระ: {fine} บาท\n\nยืนยันการชำระเงินและคืนอุปกรณ์หรือไม่?"
                reply = QMessageBox.warning(self, "ชำระค่าปรับ", msg, 
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            
            item.return_item()
            self.service.log_transaction(item, self.current_user, "Return")
            QMessageBox.information(self, "สำเร็จ", f"คืน {item.name} เรียบร้อยแล้ว")

        self.service._save_all()
        self.refresh_table()

    def delete_item(self, eq_id):
        reply = QMessageBox.question(self, 'ยืนยัน', f'ต้องการลบ {eq_id}?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.service.delete_equipment(eq_id)
            self.refresh_table()