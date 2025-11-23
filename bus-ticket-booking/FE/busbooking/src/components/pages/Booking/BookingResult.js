import { Box, Container, Grid } from '@mui/material';
import { TicketCard } from '../Ticket/LookupTicketPage';
import { parseAxiosError } from '../../../api/api';
import { getTicketByBookingId } from '../../../api/bookingsApi';
import { useEffect, useState } from 'react';
import { Button, message, Result, Space } from 'antd';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { parseTicketInfo } from '../../../utils/ticketUtils';
import { CheckCircleTwoTone, HomeOutlined } from '@ant-design/icons';
import { Loop } from '@mui/icons-material';

// status="success"
// icon={<CheckCircleTwoTone twoToneColor="#52c41a" />}
// title="Thanh toán thành công!"
// subTitle="Cảm ơn bạn đã đặt vé xe của TTT BUS."
const resultExtra = (bookingInfo) => {
  if (!bookingInfo) return null;

  if (bookingInfo.status === 'PAID') {
    return {
      status: 'success',
      icon: <CheckCircleTwoTone twoToneColor={'#52c41a'} />,
      title: 'Đặt vé thành công!',
      subTitle: 'Cảm ơn bạn đã đặt vé xe của TTT BUS.',
    };
  } else if (bookingInfo.status === 'PENDING') {
    return {
      status: 'info',
      icon: <Loop style={{ width: '50px', height: '50px', color: 'orange'}} />,
      title: 'Đang chờ thanh toán',
    };
  } else {
    return {
      status: 'error',
      title: 'Đặt vé thất bại',
      subTitle: 'Vui lòng liên hệ bộ phận hỗ trợ để được giúp đỡ.',
    };
  }
};
const BookingResult = () => {
  const [searchParams] = useSearchParams();
  const [loadingPaymentInfo, setLoadingPaymentInfo] = useState(false);
  const [paymentInfo, setPaymentInfo] = useState(null);
  const [messageAnt, contextHolder] = message.useMessage();
  const navigate = useNavigate();

  const bookingId = searchParams.get('bookingId');
  const paymentId = searchParams.get('paymentId');

  useEffect(() => {
    const fetchPaymentById = async (bookingId, paymentId) => {
      setLoadingPaymentInfo(true);
      try {
        // Gọi API để lấy thông tin thanh toán theo bookingId và paymentId
        const { responseApi } = await getTicketByBookingId(bookingId);
        console.log('Payment info:', responseApi);
        setPaymentInfo(responseApi.data);
        // Xử lý dữ liệu thanh toán ở đây (hiển thị, lưu trữ, v.v.)
      } catch (error) {
        console.error('Error fetching payment info:', parseAxiosError(error));
        messageAnt.error(
          'Lỗi khi lấy thông tin thanh toán. ' +
            (parseAxiosError(error).message || error.message)
        );
      } finally {
        // Có thể thêm logic dọn dẹp hoặc cập nhật trạng thái ở đây nếu cần
        setLoadingPaymentInfo(false);
      }
    };

    fetchPaymentById(bookingId, paymentId);
  }, [bookingId, paymentId, messageAnt]);

  return (
    <>
      {contextHolder}
      {loadingPaymentInfo && <div>Loading payment information...</div>}

      {!loadingPaymentInfo && !paymentInfo && (
        <div
          style={{
            minHeight: '75vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 16,
          }}
        >
          <Result
            status="404"
            title="Không tìm thấy thông tin vé"
            subTitle="Vui lòng kiểm tra lại mã vé hoặc quay về trang chủ."
            extra={
              <Button type="primary" onClick={() => navigate('/')}>
                Về trang chủ
              </Button>
            }
          />
        </div>
      )}

      {!loadingPaymentInfo && paymentInfo && (
        <>
          <Container maxWidth="lg" sx={{ mt: 1, mb: 4 }}>
            <Box mb={1}>
              <Result
                // status="success"
                // icon={<CheckCircleTwoTone twoToneColor="#52c41a" />}
                // title="Thanh toán thành công!"
                // subTitle="Cảm ơn bạn đã đặt vé xe của TTT BUS."
                {...resultExtra(paymentInfo)}
                extra={
                  <Space wrap>
                    <Button
                      icon={<HomeOutlined />}
                      onClick={() => navigate('/')}
                    >
                      Về trang chủ
                    </Button>
                  </Space>
                }
              />
            </Box>
            <Grid container spacing={1} justifyContent={'center'}>
              <Grid size={{ xs: 12, md: 6 }} item>
                <TicketCard ticketData={parseTicketInfo(paymentInfo)} />
              </Grid>
            </Grid>
          </Container>
        </>
      )}
    </>
  );
};
export default BookingResult;
