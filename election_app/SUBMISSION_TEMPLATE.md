# SUBMISSION - Exit Exam MVC 1/2569 (อาทิตย์เช้า)

## 1. วิธีเปิดโปรแกรม
ภาษา/เฟรมเวิร์กใช้ Python / Flask
คำสั่งเปิดโปรแกรม รันไฟล์ app.py ผ่าน Terminal ด้วยคำสั่ข:python app.py
จะไ้ดเป็น MVC169_66005164\MVC169_660550164\election_app> python app.py
ถ้าจารย์ไม่มี flask มาก่อน ให้รัยน pip install Flask==3.0.0 ก่อนรัน app.py ด้านบนค่ะ

## 2. ตารางเชื่อมโยง Requirements

| Requirement | Model / Domain | Controller / Action | View / Screen |
|---|---|---|---|
| R1 |db_manager |main_ctrl (ใช้index, voter_login) |indexhtml, voter_login.html, layout.html
| R2|CandidateModel, VoterModel, BallotModel|main_ctrl (candidate_list) voter_ctrl (vote_page, submit_vote)|candidate_list.html, voter_vote.html
| R3| ElectionModel|staff_ctrl (close_voting) |staff_dashboard.html
| R4|PatternGroupModel, ElectionModel |staff_ctrl (review_group) |staff_dashboard.html
| R5|ElectionModel, PatternGroupModel, BallotModel |staff_ctrl (dashboard)main_ctrl (public_status)voter_ctrl (ดัก Error) |staff_dashboard.html, public_status.html

## 3. ผลการทดสอบ

| กรณี | ผ่าน/ไม่ผ่าน | หมายเหตุ (เฉพาะที่จำเป็น) |
|---|---|---|
| T1 |ผ่าน |
| T2 |ผ่าน |ปฎิเสธที่หมายถึงคือไม่สามารถกดโหวตได้เลยเพราะเคยลงคะแนนแล้ว |
| T3 | ผ่าน|
| T4 |ผ่าน |
| T5 | ผ่าน|
| T6 | ผ่าน|

## 4. ความแตกต่างระหว่างแบบที่ออกกับโปรแกรมจริง (ถ้ามี)
1. ตอนแรกอยากให้คนที่เลือกแล้วกดโหวดอีกครั้งถึงจะมี popupว่าไม่มีสิทธิ์โหวต เต่เพื่อความรวดเร็วจึงเปลี่ยนเป็นแบบไม่สามารถเลือกเข้าโหวตได้ 
2. 
3. 

## 5. บันทึกการใช้ Generative AI
หากไม่ได้ใช้ ให้ระบุ **ไม่ได้ใช้ Generative AI**

| เวลาโดยประมาณ | เครื่องมือ | ใช้เพื่ออะไร | นำคำแนะนำไปใช้อย่างไร |
|---|---|---|---|
|9:45|Ghat gpt|ให้แปลReq เป็นภาษาไทยที่อ่านและเข้าใจง่ายพร้อมทั้ง | เข้าใจrequirement และ เข้าใจกระบวนการที่ต้องทำเพื่อนำไปคัดเลือกภาษา เครืื่องมือที่จะใช้
|9:55|Ghat gpt| รัน pip install แล้วขึ้น Error No such file หรือรัน python app.py แล้วขึ้น can't open fileแล้วerror AI อธิบายว่าอาจเกิดจากการรันคำสั่งผิดโฟลเดอร์|กลับไปเช็ค Directory ปัจจุบันด้วยตัวเอง และใช้คำสั่ง cd election_app เพื่อเข้าไปยังโฟลเดอร์ที่ถูกต้องก่อนรัน
10:00|Gemimi| ให้ Ai ทวนการเรียกmethod Python HTML flaks | นำวิธีการใช้ การเรียกที่ได้ไปใช้
|10:20|Gemini|ต้องการเพิ่มรูปลงบน Git ไม่ได้เลยให้ Aiสอนวิธีเอาไฟล์รูขึ่น|ทำวิธีUpload รูปตามวิธีต่างๆที่ได้เสนอมา
|10:45 |Gemini|ต้องการให้ข้อมูลถูกรีเซ็ตใหม่ทุกครั้งที่เปิดโปรแกรมแต่ตอนแรกรันแล้วได้ข้อมูลเก่าที่ยังค้างอยู่ |แนะนำแนวคิดการใช้ In-memory databaseแทนการใช้ไฟล์แคช และแนะนำคอนเซปต์การล้างตาราง (DROP TABLE) ก่อนสร้างใหม่ถ้ารันใหม่
|11:20|Gemini|ตอนนี้เจ้าหน้าที่ไม่มีปุ่มหยุดรับบัตร มีแค่สถานะ ต้องส่งค่าจาก Controller ไป View ถามว่าต้องทำยังไงให้ถูกตามหลัก MVC|ได้กลับมาแก้ไขฟังก์ชัน dashboard() ในหน้า HTML ให้แสดงปุ่มได้อย่างถูกต้อง
|11:30|Gemini|เขียนฟังก์ชันรับค่าจากฟอร์มโหวตแล้ว พอพอกด Submit เว็บพังขึ้น 405 Method Not Allowed เกิดจากอะไร ต้องไปเช็คที่ไฟล์ไหน|เจอว่าvoter_ctrl.py ส่วนsubmit_vote() ขาดพารามิเตอร์ดังกล่าวจริง หลังจากใช้ Ai ใน Vs แก้ ทำให้ระบบสามารถรับค่าจากฟอร์มและทำงานต่อได้สำเร็จโดยไม่พัง
