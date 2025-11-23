# Khơi động backend, tại root: 
- docker compose -p bus-ticket-booking up --build (--build khi lần đầu hoặc thêm libs, đổi env)
- docker compose -p bus-ticker-booking up (thêm -d nếu muốn chạy nền)
# Khởi động frontend, vào thư mục FE/busbooking: 
  - npm i
  - npm start
# Database:
 - dữ liệu ở thư mục database_script/
 - lấy dữ liệu test ở design-db
 - backup cuối cùng ở database_script/backup

# Link Swagger:
 - http://localhost:8001/users/docs
 - http://localhost:8002/trips/docs
 - http://localhost:8003/bookings/docs
 - http://localhost:8004/payments/docs
 - http://localhost:8005/notifications/docs

# Link Github: 
  - https://github.com/tmthuyen/SOA_Final_BusTicketBooking.git

# Link slide: 
  - canva-xyz

# Task
 + Thuyên: 
 + Tuấn: 
 + Tâm:  
 + Báo cáo + thuyết trình: All

# Deadline:
+ Ngày bắt đầu: 23/10/2025
+ Hạn cung cấp API_URL và mô tả của các services: 12:00 5/11/2025
+ Ngày hoàn thành code:  
+ Ngày submit: 12:00 AM 25/11/2025

# Cài đặt docker, mysql workbench, postman

# Tại thư mục gốc:
gõ lệnh (Cần bật docker app trước)
- Lần đầu: docker compose -p bus-ticket-booking up --build (sau khi pull từ git vẫn phải --build)
- Lần sau sửa code (không cập nhật thư viện): docker-compose -p bus-ticket-booking up 

# Hiện tại có gateway với cổng 8000
# Mỗi API sẽ có port riêng với user_service là 8001
- API gateway http://localhost:8000 + service + path
  + vi du: http://localhost:8000/user/login

- API User service: http://localhost:8000/users/{path}
- API Trip service: http://localhost:8000/trips/{path}
- API Booking service: http://localhost:8000/bookings/{path}
- API Notification service: http://localhost:8000/notifications/{path}
- API Payment service: http://localhost:8000/payments/{path}

# port db trong docker-compose.yml sẽ là port để kết nối với mysql workbench cho từng service
- Vi du: 
  ports:
      - "3308:3306"
  3308 la port de ket noi
# mỗi service có database riêng nha
- Vô mysql workbench tạo kết nối tương ứng với các port db trong file docker-compose.yml

# Thay đổi cập nhật thuộc tính database thì nhớ back up dữ liệu cũ trước hoặc thay đổi column trong db
docker compose down user_db
docker volume rm bus-ticket-booking_user_db_data
docker compose up -d user_db



http://localhost:3000/payment-success?status=success
&bookingCode=BK2311256191
&email=tranthuyen2222@gmail.com
&tripId=1
&partnerCode=MOMO
&orderId=BOOK209015b7202511230425236B53ADFB
&requestId=b230dc58-4892-4ffa-b747-d8b3e5861eb5
&amount=850000
&orderInfo=Thanh+to%C3%A1n+v%C3%A9+xe
&orderType=momo_wallet
&transId=4614096933
&resultCode=1002
&message=Successful.
&payType=napas
&responseTime=1763872191084
&extraData=
&signature=31549feb0d74c73d730284e5311edb26a78b7a0974eee3e6ed15e5a3df58d834

Lấy result từ link
- Thành công: booking ? payment?
- Thất bại: 