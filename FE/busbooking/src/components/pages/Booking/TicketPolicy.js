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
        khuyến mãi về sau.
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        (*) Quý khách vui lòng có mặt tại bến xuất phát của xe trước ít nhất 30
        phút giờ xe khởi hành, mang theo thông báo đã thanh toán vé thành công
        có chứa mã vé được gửi từ hệ thống BUS TICKET BOOKING. Vui lòng liên hệ
        Trung tâm tổng đài XXX để được hỗ trợ.
      </Typography>
    </>
  );
};

export default memo(TicketPolicy);