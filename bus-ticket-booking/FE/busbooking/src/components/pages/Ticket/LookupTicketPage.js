import { MailOutlined, SearchOutlined } from '@ant-design/icons';
import {
  Box,
  Chip,
  Container,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography,
} from '@mui/material';
import { Button, Form, Input, message } from 'antd';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTicketByCodeAndEmailAction } from '../../../store/actions/bookingsAction';
import { BOOKING_STATUS } from '../../../constants';
import { formatVNDate } from '../../../utils/formatTime';
import currencyUtils from '../../../utils/currencyUtils';

const parseTicketInfo = (ticketInfo) => {
  if (!ticketInfo) return null;
 
  const info = {
    id: ticketInfo.id,
    bookingCode: ticketInfo.booking_code,
    fullName: ticketInfo.full_name,
    phone: ticketInfo.phone,
    email: ticketInfo.email,
    status: ticketInfo.status,
    seatQuantity: ticketInfo.seat_quantity,
    totalPrice: ticketInfo.total_price,
    createdAt: ticketInfo.created_at,
    seatAssignments: ticketInfo.seat_assignments
      .map((seat) => seat.seat_number)
      .join(', '),
    origin: ticketInfo.trip?.route?.origin,
    destination: ticketInfo.trip?.route?.destination,
    departureTime: ticketInfo.trip?.departure_time,
    arrivalTime: ticketInfo.trip?.arrival_time,
    busPlateNumber: ticketInfo.trip?.bus?.plate_number,
  };

  return info;
};

const LookupTicketPage = () => {
  const [formLookupTicket] = Form.useForm();
  const dispatch = useDispatch();
  const [messageAnt, contextHolder] = message.useMessage();

  // store state
  const {
    ticketInfo,
    loading: loadingLookup,
    success,
    message: messageLookup,
  } = useSelector((state) => state.bookings);

  const [bookingCode, setBookingCode] = useState('');
  const [email, setEmail] = useState('');
  const [ticketFetched, setTicketFetched] = useState(null);

  const [submitLookup, setSubmitLookup] = useState(false);

  const onFinish = async (values) => {
    const { booking_code, email } = values;
    console.log('Finish form lookup ticket:', values);
    setBookingCode(booking_code);
    setEmail(email);
    setSubmitLookup(true);
    // dispatch action to lookup ticket
    await dispatch(fetchTicketByCodeAndEmailAction(booking_code, email));
  };

  useEffect(() => {
    if (!submitLookup) return;

    if (success && !loadingLookup && ticketInfo) {
      messageAnt.success(messageLookup);
      console.log('Ticket info fetched:', parseTicketInfo(ticketInfo));
      setTicketFetched(ticketInfo);
    }

    if (!success && !loadingLookup) {
      messageAnt.error(messageLookup);
    }
  }, [
    success,
    loadingLookup,
    messageLookup,
    ticketInfo,
    messageAnt,
    submitLookup,
  ]);

  useEffect(() => {
    setTicketFetched(null);
  }, [email, bookingCode]);

  const onFinishFailed = (errorInfo) => {
    console.log('Failed to submit form customer booking:', errorInfo);
  };
  const onInputChange = (changedValues, allValues) => {
    setBookingCode(allValues.booking_code);
    setEmail(allValues.email);
    console.log('Input change form lookup ticket:', changedValues, allValues);
  };

  return (
    <>
      {contextHolder}
      <Container maxWidth="lg" sx={{ minHeight: '80vh', paddingY: 4 }}>
        <Typography
          variant="h5"
          fontWeight={600}
          style={{ textAlign: 'center' }}
        >
          Tra cứu vé
        </Typography>
        <Grid
          container
          spacing={2}
          sx={{ marginTop: 2, justifyContent: 'center' }}
        >
          <Grid size={{ xs: 12, md: 6 }}>
            <Form
              layout="vertical"
              form={formLookupTicket}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              onValuesChange={onInputChange}
              autoComplete="off"
              // initialValues={{
              //   full_name: 'fullName',
              //   email: email,
              //   phone: phone,
              // }}
            >
              <Form.Item
                label="Mã đặt vé"
                name="booking_code"
                rules={[{ required: true, message: 'Vui lòng nhập mã đặt vé' }]}
              >
                <Input
                  allowClear
                  placeholder="Nhập mã đặt vé"
                  value={bookingCode}
                  // prefix={< />}
                />
              </Form.Item>
              <Form.Item
                label="Địa chỉ email"
                name="email"
                rules={[{ required: true, message: 'Vui lòng nhập email' }]}
              >
                <Input
                  allowClear
                  placeholder="Nhập email"
                  prefix={<MailOutlined />}
                  value={email}
                />
              </Form.Item>

              <Form.Item label={null}>
                <Button
                  htmlType="submit"
                  loading={loadingLookup}
                  block
                  style={{
                    background: 'var(--color-primary)',
                    color: 'black',
                    '&:hover': { background: 'var(--color-primary-dark)' },
                  }}
                  icon={<SearchOutlined />}
                >
                  Tìm vé
                </Button>
              </Form.Item>
            </Form>
          </Grid>

          {success && ticketFetched && (
            <Grid size={{ xs: 12, md: 6 }} sx={{ marginTop: 4 }}>
              <TicketCard ticketData={parseTicketInfo(ticketFetched)} />
            </Grid>
          )}
        </Grid>
      </Container>
    </>
  );
};
export default LookupTicketPage;

export const TicketCard = ({ ticketData }) => {
  if (!ticketData)
    return (
      <>
        <Typography variant="body1">
          Không có thông tin vé để hiển thị.
        </Typography>
      </>
    );

  const departimeVN =
    formatVNDate(ticketData.departureTime, { withTime: true }) || '—';
  const arrivaltimeVN =
    formatVNDate(ticketData.arrivalTime, {
      withTime: true,
    }) || '—';
  const statusLabel =
    BOOKING_STATUS[ticketData.status]?.label || ticketData.status;
  let statusChip = null;
  if (ticketData.status === BOOKING_STATUS.PENDING.value) {
    statusChip = <Chip label={statusLabel} color="warning" />;
  } else if (ticketData.status === BOOKING_STATUS.PAID.value) {
    statusChip = <Chip label={statusLabel} color="success" />;
  } else if (ticketData.status === BOOKING_STATUS.CANCELLED.value) {
    statusChip = <Chip label={statusLabel} color="error" />;
  } else if (ticketData.status === BOOKING_STATUS.REFUNDED.value) {
    statusChip = <Chip label={statusLabel} color="info" />;
  } else {
    statusChip = <Chip label={statusLabel} />;
  }
  return (
    <>
      <Box
        sx={{
          width: '100%',
          background: 'var(--color-white)',
          borderRadius: '8px',
          boxShadow: 'var(--box-shadow)',
          // minHeight: '100vh',
          padding: '16px',
        }}
      >
        <Typography
          variant="h6"
          fontWeight={600}
          style={{ textAlign: 'center' }}
        >
          Thông tin vé
        </Typography>
        <Table size="small" sx={{ mt: 1 }}>
          <TableBody>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Mã đặt vé
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {ticketData?.bookingCode}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Khách hàng
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {ticketData?.fullName}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Email
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {ticketData?.email}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Số điện thoại
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {ticketData?.phone}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Chuyến xe
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {ticketData?.origin} - {ticketData?.destination}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Thời gian khởi hành
              </TableCell>
              <TableCell align="right" sx={{ borderBottom: 'none' }}>
                {departimeVN}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Dự kiến đến
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {arrivaltimeVN}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Xe
              </TableCell>
              <TableCell align="right" sx={{ borderBottom: 'none' }}>
                {ticketData?.busPlateNumber}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Số ghế đã đặt
              </TableCell>
              <TableCell align="right" sx={{ borderBottom: 'none' }}>
                {ticketData?.seatQuantity}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Ghế đã đặt
              </TableCell>
              <TableCell align="right" sx={{ borderBottom: 'none' }}>
                {ticketData?.seatAssignments}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Trạng thái vé
              </TableCell>
              <TableCell align="right" sx={{ borderBottom: 'none' }}>
                {statusChip}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                Tổng tiền
              </TableCell>
              <TableCell align="right" sx={{ borderBottom: 'none' }}>
                {currencyUtils.formatCurrency(ticketData?.totalPrice)}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Box>
    </>
  );
};
