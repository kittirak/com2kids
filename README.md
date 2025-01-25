# Veyon installation scripts
## ลำดับการติดตั้ง
1. เมื่อ**เครื่องผู้สอน**ต่ออินเทอร์เน็ตได้ ให้รันสคริปต์ veyon-teacher-setup.sh ในสคริปต์จะ
- กำหนดให้ไปดาวน์โหลด veyon_4.8.3.0-ubuntu.focal_amd64.deb (ใช้กับ Zorin 16, Ubuntu 20.04) 
- ติดตั้ง veyon สร้างคีย์ 
- ติดตั้ง python package สำหรับรันเซิร์ฟเวอร์เืพื่อให้บริการสำหรับติดตั้งและคอนฟิกเครื่องผู้เรียน
- ให้กำหนด hostname แบบ FQDN พิจารณาใช้ชื่อโรงเรียนเป็นโดเมน** สำคัญส่วนนี้จะใช้สำหรับเก็บสถิติการใช้งาน และโดเมนจะถูกนำไปใช้กำหนดให้เครื่องผู้เรียนด้วย
```
git clone https://github.com/kittirak/com2kids.git
./com2kids/veyon-teacher-setup.sh
```

2. เมื่อ**เครื่องผู้เรียน**เชื่อมต่อเครือข่าย คุยกับเครื่องผู้สอนได้ รันสคริปต์ veyon-student-setup.sh [IP เครื่องผู้สอน] เช่น 
```
wget https://raw.githubusercontent.com/kittirak/com2kids/master/veyon-student-setup.sh
./veyon-student-setup.sh 10.0.2.251 
```
สคริปต์จะไปดาวน์โหลด veyon จากเครื่องผู้สอนตามไอพีที่กำหนด ติดตั้ง คอนฟิก พร้อมทั้งลงทะเบียนไอพีไปยังเครื่องผู้สอน

3. ทำตามข้อ 2 จนครบทุกเครื่องและให้ทำเรียงตามลำดับเครื่อง เพราะระบบจะรันชื่อเครื่องตามลำดับในรูปแบบ student1, student2 ..

