# 🚀 EquipFlow - ระบบบริหารจัดการยืม-คืนอุปกรณ์ (EquipFlow-Management-System)

EquipFlow เป็นแอปพลิเคชันสำหรับจัดการการยืมและคืนอุปกรณ์ภายในองค์กร พัฒนาด้วยภาษา Python โดยเน้นการออกแบบตามหลักการ **Object-Oriented Programming (OOP)** และ **SOLID Principles** เพื่อให้โค้ดมีความยืดหยุ่นและง่ายต่อการขยายผลในอนาคต

---

## 👥 ข้อมูลทีมและสมาชิก (Team Information)

**ชื่อทีม:** Yakporlaew
**โปรเจกต์:** EquipFlow-Management-System

| รหัสนักศึกษา | ชื่อ-นามสกุล | หน้าที่รับผิดชอบ (Responsibility) |
|:------------|:-----------|:-------------------------------|
| 68114540399 | นางสาวปัญญาพร มูลดับ | **Project Manager & Backend & UI/UX**<br>- ออกแบบโครงสร้าง Class (OOP/SOLID)<br>- จัดการ Logic การยืม-คืน และค่าปรับ<br>- พัฒนา GUI ด้วย PySide6 และ Stylesheet |
| 68114540045 | นางสาวกฤติมา ทองมวล | **Transaction Logging**<br>- ออกแบบระบบบันทึกประวัติ (History Log)<br>- จัดการโครงสร้างไฟล์ข้อมูล JSON |

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
EquipFlow/
├── app/                  # ส่วน Business Logic และ UI
│   ├── __init__.py       # ทำให้โฟลเดอร์ app กลายเป็น Python Package
│   ├── models.py         # เก็บ Class ต่างๆ
│   ├── services.py       # เก็บฟังก์ชันจัดการข้อมูล
│   ├── storage.py        # จัดการไฟล์ JSON
│   └── ui.py             # โค้ดหน้าจอและระบบ Role-Based
├── data/                 # ส่วนฐานข้อมูล (Database)
│   ├── inventory.json    # เก็บข้อมูลอุปกรณ์
│   ├── history.json      # เก็บประวัติการยืม-คืน
│   └── users.json        # เก็บข้อมูลผู้ใช้งาน
├── main.py               # ไฟล์หลักที่ใช้รันโปรแกรม
├── README.md             # คู่มือการใช้งาน
└── requirements.txt      # รายชื่อ Library (PySide6)
```
---

## ✨ คุณสมบัติของระบบ (Key Features)

- **Role-based Access Control:** แบ่งสิทธิ์ชัดเจนระหว่าง Admin (จัดการอุปกรณ์) และ User (ยืม-คืนอุปกรณ์)
- **Rental System:** User สามารถค้นหาอุปกรณ์และทำรายการยืม-คืนได้ด้วยตนเอง
- **Inventory Management:** ระบบจัดการอุปกรณ์ เพิ่ม/ลบ ข้อมูลได้แบบ Real-time
- **Automated Fine System:** คำนวณค่าปรับอัตโนมัติหากคืนเกินกำหนด 7 วัน โดยคำนวณจากวันที่ยืมจริง (วันละ 50 บาท)
- **Transaction Logging:** บันทึกประวัติการยืม-คืนอย่างละเอียดลงไฟล์ JSON เพื่อการตรวจสอบย้อนหลัง
- **Modern GUI:** อินเตอร์เฟซที่ทันสมัย ใช้งานง่าย พร้อมระบบตอบโต้ผ่าน Dialog และ Message Box

---

## 🔑 บัญชีเข้าใช้งานสำหรับทดสอบ (Test Accounts)

เพื่อให้สามารถทดสอบระบบได้ทันที สามารถใช้บัญชีต่อไปนี้ในการเข้าสู่ระบบ:

| สิทธิ์การใช้งาน (Role) | ชื่อผู้ใช้ (Username) | รหัสผ่าน (Password) |
|:---|:---|:---|
| 👑 **ผู้ดูแลระบบ (Admin 1)** | `admin1` | `123` |
| 👑 **ผู้ดูแลระบบ (Admin 2)** | `admin2` | `456` |
| 👤 **ผู้ใช้งาน (User 1)** | `user1` | `111` |
| 👤 **ผู้ใช้งาน (User 2)** | `user2` | `222` |

> **หมายเหตุ:** บัญชีเหล่านี้ถูกจัดเก็บอยู่ในไฟล์ `data/users.json` ท่านสามารถเพิ่มหรือแก้ไขบัญชีผู้ใช้ได้จากไฟล์ดังกล่าว

---
### Clone ลงเครื่อง

เปิด Command Prompt แล้วทำตามนี้

เลือกที่อยู่: พิมพ์ cd desktop (เพื่อไปที่หน้าจอ Desktop เก็บงานที่นี่จะได้หาง่าย)

ใช้คำสั่ง Clone: พิมพ์คำสั่งด้านล่างนี้แล้วกด Enter

**Clone Repository**
   ```bash
   git clone [https://github.com/ช](https://github.com/ช)ื่อUserของคุณ/EquipFlow.git
   cd EquipFlow
```

### การเปิดโปรเจกต์
1. เปิดโปรแกรม **VS Code**
2. ไปที่เมนู `File` > `Open Folder...` แล้วเลือกโฟลเดอร์ **EquipFlow-Management-System**
ทำตามขั้นตอนด้านล่างนี้เพื่อติดตั้งและรันโปรเจกต์ในเครื่องของคุณ :


วิธีเปิด Terminal ใน VS Code

ใช้เมนูด้านบน: คลิกที่เมนูคำว่า Terminal แล้วเลือก New Terminal

### 🛠 1. สิ่งที่ต้องเตรียม (Prerequisites)
- ก่อนจะเริ่มติดตั้งโปรแกรม ตรวจสอบให้แน่ใจว่าเครื่องของคุณมีสิ่งเหล่านี้: **Python 3.9 หรือสูงกว่า** หากยังไม่มีให้ดาวน์โหลดที่ [python.org](https://www.python.org/)
- ตรวจสอบเวอร์ชันโดยพิมพ์: 
```bash
python --version
```
- สำคัญ: ในขั้นตอนการติดตั้งบน Windows ต้องติ๊กถูกที่ช่อง "Add Python to PATH" เสมอ

### 2. การติดตั้ง Library (Dependencies)
ติดตั้ง Library ทั้งหมดที่จำเป็นผ่านคำสั่ง:
```bash
pip install -r requirements.txt
```
🚀 วิธีการเข้าใช้งาน (How to Run)
หลังจากติดตั้ง Library เรียบร้อยแล้ว ให้รันโปรแกรมด้วยคำสั่ง:
```bash
python main.py
```


