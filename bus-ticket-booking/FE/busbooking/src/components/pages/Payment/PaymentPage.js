import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  Radio,
  RadioGroup,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography,
} from '@mui/material';
import BookingSummary from '../Booking/BookingSummary';
import { PAYMENT_METHOD } from '../../../constants';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation, useSearchParams } from 'react-router-dom';
import { fetchBookingByCodeAction } from '../../../store/actions/bookingsAction';
import { fetchTripById } from '../../../store/actions/tripsAction';

const PaymentPage = () => {
  // hooks
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const dispatch = useDispatch();

  // reducer state
  const { tripById: tripChosen } = useSelector((state) => state.trips);
  const { bookingCreated: bookingFromStore, loading: bookingLoading } =
    useSelector((state) => state.bookings);

  // local state
  const [method, setMethod] = useState(PAYMENT_METHOD.MOMO);

  // query params
  const bookingCode = searchParams.get('bookingCode');
  const email = searchParams.get('email');
  const tripId = searchParams.get('tripId');

  // get trip info 

  const { booking: bookingFromState } = location.state || {};

  // 🔹 Chỉ fetch từ API nếu KHÔNG có bookingFromState & chưa có bookingFromStore
  useEffect(() => {
    if (bookingCode && !bookingFromStore) {
      dispatch(fetchBookingByCodeAction(bookingCode));
    }
  }, [bookingCode, bookingFromState, bookingFromStore, dispatch]);

  useEffect(() => {
    dispatch(fetchTripById(tripId));
  }, [tripId, dispatch]);

  const bookingInfo = bookingFromStore;
  // console.log('Booking info:', bookingInfo);
  // prepare props for BookingSummary
  const [bookingSummaryProps, setBookingSummaryProps] = useState({});

  const handleSubmitPayment = () => {
    const redirectUrl = 'http://localhost:3000/payment-success?status=success&bookingCode=' + bookingInfo?.booking_code + '&email=' + bookingInfo?.email + '&tripId=' + bookingInfo?.trip_id;
    const payloadPayment = {
      booking_id: bookingInfo?.booking_id,
      amount: bookingInfo?.total_price,
      order_info: `Payment for booking code: ${bookingInfo?.booking_code}`,
      payment_method: method,
      customer_name: bookingInfo?.full_name,
      customer_phone: bookingInfo?.phone,
      customer_email: bookingInfo?.email,
      redirect_url: redirectUrl,
      ipn_url: redirectUrl,

    }

    console.log('Payment payload:', payloadPayment);
    if (method === PAYMENT_METHOD.MOMO) {
      alert('Redirecting to MOMO payment gateway...');
      
    } else if (method === PAYMENT_METHOD.VNPAY) {
      alert('Redirecting to VNPAY payment gateway...');
    }
  }

  useEffect(() => {
    setBookingSummaryProps({
      title: 'Thông tin chuyến đi',
      routeLabel: `${tripChosen?.route.origin || '...'} - ${
        tripChosen?.route.destination || '...'
      }`,
      departureTimeLabel: tripChosen?.departure_time || '...',
      basePrice: tripChosen?.route.base_price || 0,
      seatCount: bookingInfo?.seat_quantity || 0,
      seatNumbers: bookingInfo?.seat_assignments || [],
      dropoffPoint: tripChosen?.dropoff_point || '...',
      fare: bookingInfo?.total_price || 0,
      paymentFee: 0,
    });
  }, [tripChosen, bookingInfo]);

  if (!bookingCode || !email || !tripId) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h6" color="error" align="center">
          Thiếu thông tin thanh toán. Vui lòng kiểm tra lại liên kết.
        </Typography>
      </Container>
    );
  }

  if (bookingLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h6" align="center">
          Đang tải thông tin đặt vé...
        </Typography>
      </Container>
    );
  }

  return (
    <>
      <Container maxWidth="lg" sx={{ mt: 1, mb: 4 }}>
        <Typography variant="h4" style={{ textAlign: 'center' }}>
          Payment Page
        </Typography>

        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 4 }}>
            {/* Payment method */}
            <Box
              sx={{
                width: '100%',
                background: 'var(--color-white)',
                borderRadius: '8px',
                boxShadow: 'var(--box-shadow)',
                // minHeight: '100vh',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <PaymentChooseMethod method={method} setMethod={setMethod} />

              <Button variant="contained" sx={{ mt: 2 }} fullWidth onClick={handleSubmitPayment}>
                Thanh toán ngay
              </Button>
            </Box>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
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
              {method === 'MOMO' && (
                <Typography>Payment with MOMO selected</Typography>
              )}
              {method === 'VNPAY' && (
                <Typography>Payment with VNPAY selected</Typography>
              )}
              <BookingSummary {...bookingSummaryProps} />
            </Box>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
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
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Thông tin khách hàng
              </Typography>
              <Table size="small" sx={{ mt: 1 }}>
                <TableBody>
                  <TableRow>
                    <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                      Họ và tên
                    </TableCell>
                    <TableCell
                      align="right"
                      sx={{ borderBottom: 'none', fontWeight: 500 }}
                    >
                      {bookingInfo?.full_name || 'Nguyễn Văn A'}
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell sx={{ borderBottom: 'none', fontWeight: 600 }}>
                      Email
                    </TableCell>
                    <TableCell align="right" sx={{ borderBottom: 'none' }}>
                      {bookingInfo?.email || 'example@example.com'}
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
                      {bookingInfo?.phone || '0123456789'}
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </Box>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default PaymentPage;

const PaymentChooseMethod = ({ method = PAYMENT_METHOD.MOMO, setMethod }) => {
  const handleMethodChange = (val) => {
    console.log('Selected payment method:', val);
    setMethod(val);
  };
  return (
    <FormControl>
      <FormLabel id="demo-controlled-radio-buttons-group">
        Chọn phương thức thanh toán
      </FormLabel>
      <RadioGroup
        aria-labelledby="demo-controlled-radio-buttons-group"
        name="controlled-radio-buttons-group"
        value={method}
        onChange={(e) => handleMethodChange(e.target.value)}
      >
        <FormControlLabel
          value={PAYMENT_METHOD.VNPAY}
          control={<Radio />}
          label="Thanh toán VNPAY"
        />
        <FormControlLabel
          value={PAYMENT_METHOD.MOMO}
          control={<Radio />}
          label="Thanh toán  MOMO"
        />
      </RadioGroup>
    </FormControl>
  );
};
