# Veyon installation scripts
## ลำดับการติดตั้ง
1. เมื่อ**เครื่องผู้สอน**ต่ออินเทอร์เน็ตได้ ให้รันสคริปต์ veyon-teacher-setup.sh ในสคริปต์จะ
- ไปดาวน์โหลด veyon_4.8.3.0-ubuntu.focal_amd64.deb (ใช้กับ Zorin 16, Ubuntu 20.04) มาวางใน Downloads 
- ติดตั้ง veyon และสร้างคีย์ 
- ติดตั้ง python package สำหรับรันเซิร์ฟเวอร์เพื่อแชร์ไฟล์ veyon, public key และข้อมูลให้สำหรับติดตั้งและคอนฟิกเครื่องผู้เรียน พร้อมทั้งรับข้อมูล IP จากเครื่องผู้เรียนมาสร้างรายการเครื่องคอมพิวเตอร์ให้โดยอัตโนมัติ
- ให้กำหนด hostname แบบ FQDN พิจารณาใช้ชื่อโรงเรียนเป็นโดเมน** สำคัญส่วนนี้จะใช้สำหรับเก็บสถิติการใช้งาน และโดเมนจะถูกนำไปใช้กำหนดให้เครื่องผู้เรียนด้วย
```
sudo apt update
git clone https://github.com/kittirak/com2kids.git
cd com2kids
./veyon-teacher-setup.sh
```
- ถ้าจะติดตั้งเครื่องเพิ่มเติมในภายหลังให้รันคำสั่งต่อไปนี้
```
cd com2kids
sudo uvicorn server:app --host 0.0.0.0 --port 8000
```

2. เมื่อ**เครื่องผู้เรียน**เชื่อมต่อเครือข่าย คุยกับเครื่องผู้สอนได้ รันสคริปต์ veyon-student-setup.sh [IP เครื่องผู้สอน] เช่น 
```
sudo apt update
wget https://raw.githubusercontent.com/kittirak/com2kids/master/veyon-student-setup.sh
chmod +x veyon-student-setup.sh
./veyon-student-setup.sh 10.0.2.251 
```
สคริปต์จะไปดาวน์โหลด veyon จากเครื่องผู้สอนตามไอพีที่กำหนด ติดตั้ง คอนฟิก พร้อมทั้งลงทะเบียนไอพีไปยังเครื่องผู้สอน เมื่อติดตั้งเสร็จ Logout แล้ว Login ใหม่สักครั้งเพื่อการทำงานที่สมบูรณ์ของ veyon 

3. ทำตามข้อ 2 จนครบทุกเครื่องและให้ทำเรียงตามลำดับเครื่อง เพราะระบบจะรันชื่อเครื่องตามลำดับในรูปแบบ student1, student2 ..

