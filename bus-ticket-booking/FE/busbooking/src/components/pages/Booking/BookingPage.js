import { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { fetchSeatsByTrip } from '../../../store/actions/tripsAction';
import { Box, Button, Container, Divider, Grid, Typography } from '@mui/material';
import CustomerBookingForm from './CustomerBookingForm';
import TicketPolicy from './TicketPolicy';
import BookingSummary from './BookingSummary';
import SeatMap from './SeatMap';
import { notification } from 'antd';
import { WarningOutlined } from '@ant-design/icons';
import { createBookingAction } from '../../../store/actions/bookingsAction';

const BookingPage = () => {
  // hooks
  const { tripId } = useParams();
  const location = useLocation();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [apiNotification, contextHolder] = notification.useNotification();
  const openErrorNotification = useCallback(
    (message, description) => {
      apiNotification.error({
        message,
        description,
        icon: <WarningOutlined style={{ color: '#fa0707ff' }} />,
        duration: 2,
      });
    },
    [apiNotification]
  );

  // local state
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [isReadPolicy, setIsReadPolicy] = useState(false);
  const [totalPrice, setTotalPrice] = useState(0);

  // reducer state
  const { trip: tripFromState } = location.state || {};
  const { seatsByTrip, tripsByRoute } = useSelector((state) => state.trips);
  const {
    bookingCreated,
    success: bookingSuccess,
    message: bookingMessage,
  } = useSelector((state) => state.bookings);
  const trip =
    tripFromState || tripsByRoute?.find((t) => t.id === parseInt(tripId));
  // console.log('Trip from state:', tripFromState);
  // console.log('Trip:', trip);

  const [selectedSeatIds, setSelectedSeatIds] = useState([]);
  const handleToggleSeat = useCallback(
    (seat) => {
      setSelectedSeatIds((prev) => {
        // console.log('Toggling seat:', prev, seat);
        let isSelected = false;
        prev.forEach((s) => {
          if (s.seat_id === seat.seat_id) {
            isSelected = true;
          }
        });
        // console.log('Is seat selected:', isSelected);
        if (isSelected) {
          return prev.filter((s) => s.seat_id !== seat.seat_id);
        }

        if (prev.length >= 5) {
          openErrorNotification(
            'Chọn ghế thất bại',
            'Bạn chỉ được chọn tối đa 5 ghế cho mỗi lần đặt vé.'
          );
          return prev;
        }
        return [
          ...prev,
          { seat_id: seat.seat_id, seat_number: seat.seat_number },
        ];
      });
    },
    [setSelectedSeatIds, openErrorNotification]
  );

  useEffect(() => {
    if (tripId && seatsByTrip.length === 0) {
      dispatch(fetchSeatsByTrip(parseInt(tripId)));
    }
  }, [tripId, seatsByTrip, dispatch]);

  // tinh tong tien
  useEffect(() => {
    setTotalPrice(selectedSeatIds?.length * trip.base_price || 0);
  }, [selectedSeatIds, trip]);

  const handleBookingInfo = async () => {
    if (selectedSeatIds.length === 0) {
      openErrorNotification(
        'Chưa chọn ghế',
        'Vui lòng chọn ghế trước khi đặt vé.'
      );
      return;
    }
    if (!fullName || !email || !phone) {
      openErrorNotification(
        'Thiếu thông tin khách hàng',
        'Vui lòng điền đầy đủ thông tin khách hàng trước khi đặt vé.'
      );
      return;
    }

    // luu lai thong tin trong local storage
    const customer_info = {
      full_name: fullName,
      email,
      phone,
    };
    window.localStorage.setItem('customer_info', JSON.stringify(customer_info));

    if (!isReadPolicy) {
      openErrorNotification(
        'Chưa đồng ý chính sách',
        'Vui lòng đồng ý với các điều khoản và chính sách đặt vé trước khi đặt vé.'
      );
      return;
    }

    const bookingInfo = {
      trip_id: parseInt(trip.id),
      full_name: fullName,
      email,
      phone,
      seats_selected: selectedSeatIds,
      seat_numbers: selectedSeatIds.map((s) => s.seat_number),
      seat_count: selectedSeatIds.length,
      total_price: parseInt(totalPrice),
    };
    console.log('Booking info:', bookingInfo);
    const bookingResult = await dispatch(createBookingAction(bookingInfo));
    console.log('Booking result:', bookingResult);

    if (!bookingResult || bookingResult.success === false) {
      openErrorNotification(
        'Đặt vé thất bại',
        bookingResult.message ||
          'Có lỗi xảy ra khi đặt vé. Vui lòng thử lại sau.'
      );
      console.error('Booking failed:', bookingResult);

      return;
    }

    apiNotification.success({
      message: 'Đặt vé thành công',
      description: `Giữ vé thành công. Mã vé của bạn là: ${
        bookingResult.data.booking_code
      }.\n ${JSON.stringify(bookingResult.data, null, 2)}`,
      duration: 5,
    });

    apiNotification.info({
      message: 'Chuyển đến trang thanh toán',
      description: 'Bạn sẽ được chuyển đến trang thanh toán trong giây lát.',
      duration: 3,
    });

    setTimeout(() => {
      navigate(
        `/payments?bookingCode=${bookingResult.data.booking_code}&email=${email}&tripId=${trip.id}`,
        { state: { booking: bookingResult.data, trip } }
      );
    }, 3000);

    // alert('Thong tin dat ve: ' + JSON.stringify(bookingInfo, null, 2));
  };

  if (!trip) {
    return (
      <Container sx={{ mt: 3 }}>
        <Typography>Đang tải thông tin chuyến đi...</Typography>
      </Container>
    );
  }

  // console.log('Seats by trip:', seatsByTrip);
  // console.log('Selected seat IDs:', selectedSeatIds);
  // console.log('Selected trip:', trip);

  return (
    <>
      {contextHolder}
      <Container maxWidth="lg" style={{ marginBottom: '20px' }}>
        <h2>Booking Page for Trip ID: {tripId}</h2>

        <Grid container spacing={2}>
          <Grid
            container
            spacing={1}
            size={{ xs: 12, md: 8 }}
            sx={{
              background: 'var(--color-white)',
              borderRadius: '8px',
              boxShadow: 'var(--box-shadow)',
              // minHeight: '100vh',
              padding: '16px',
            }}
          >
            <Grid item size={12}>
              <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
                Sơ đồ ghế
              </Typography>
              <SeatMap
                total_seats={seatsByTrip.total_seats || 0}
                total_booked={seatsByTrip.total_booked || 0}
                seats={seatsByTrip.seat_layout || []}
                selectedSeatIds={selectedSeatIds}
                onToggleSeat={handleToggleSeat}
              />
            </Grid>

            <Divider sx={{ width: '100%', my: 2 }} />

            <Grid container spacing={1} size={12}>
              <Grid item size={{ xs: 12, md: 6 }}>
                <CustomerBookingForm
                  setFullName={(name) => setFullName(name)}
                  setEmail={(e) => setEmail(e)}
                  setPhone={(p) => setPhone(p)}
                />
              </Grid>
              <Grid item size={{ xs: 12, md: 6 }}>
                <TicketPolicy />
              </Grid>
              <Grid item size={12} sx={{ mb: 2 }}>
                {/* check box dong y chinh sach */}
                <input
                  type="checkbox"
                  checked={isReadPolicy}
                  onChange={(e) => setIsReadPolicy(e.target.checked)}
                />
                <label htmlFor="agreePolicy" style={{ marginLeft: '8px' }}>
                  Tôi đồng ý với các điều khoản và chính sách đặt vé.
                </label>
              </Grid>
            </Grid>
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
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <BookingSummary
                title="Thông tin lượt đi"
                routeLabel={`${trip?.origin || '...'} - ${
                  trip?.destination || '...'
                }`}
                departureTimeLabel={trip?.departure_time || '...'}
                seatCount={selectedSeatIds?.length || 0}
                seatNumbers={selectedSeatIds}
                dropoffPoint={trip?.dropoff_point || '...'}
                basePrice={trip?.base_price || 0}
                fare={totalPrice || 0}
                paymentFee={trip?.payment_fee || 0}
              />
            </Box>
          </Grid>
          {/* nut thanh toan va huy booking */}
          <Grid item size={12} sx={{ textAlign: 'right', marginTop: '16px' }}>
            <Button
              variant="outlined"
              color="primary"
              onClick={() => alert('Huy dat ve')}
            >
              Hủy đặt vé
            </Button>
            <Button
              variant="contained"
              color="primary"
              sx={{ marginLeft: '8px' }}
              onClick={handleBookingInfo}
            >
              Đặt vé
            </Button>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default BookingPage;
