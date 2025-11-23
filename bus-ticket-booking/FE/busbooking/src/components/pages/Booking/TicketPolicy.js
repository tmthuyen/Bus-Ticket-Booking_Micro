import { Typography } from '@mui/material';
import { memo } from 'react';

const TicketPolicy = () => {
  return (
    <>
      <Typography variant="h6" sx={{}}>
        Chính sách đặt vé
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        Quý khách vui lòng Đăng ký/Đăng nhập tài khoản để nhận chương trình
        khuyến mãi.
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        (*) Quý khách vui lòng có mặt tại bến xuất phát của xe trước ít nhất 30
        phút giờ xe khởi hành, mang theo thông báo đã thanh toán vé thành công
        có chứa mã vé được gửi từ hệ thống FUTA BUS LINES. Vui lòng liên hệ
        Trung tâm tổng đài 1900 6067 để được hỗ trợ.
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        (*) Nếu quý khách có nhu cầu trung chuyển, vui lòng liên hệ Tổng đài
        trung chuyển 1900 6918 trước khi đặt vé. Chúng tôi không đón/trung
        chuyển tại những điểm xe trung chuyển không thể tới được.
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        (*) Nếu quý khách có nhu cầu di chuyển chặng đường ngắn hơn so với hành
        trình, vui lòng gọi Tổng đài 1900 6067 để được hưởng chính sách giá vé
        tốt nhất.
      </Typography>
    </>
  );
};

export default memo(TicketPolicy);