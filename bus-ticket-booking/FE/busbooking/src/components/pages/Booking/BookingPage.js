import { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation, useParams } from 'react-router-dom';
import { fetchSeatsByTrip } from '../../../store/actions/tripsAction';
import {
  Button,
  Container,
  Divider,
  Grid,
  Table,
  Typography,
} from '@mui/material';
import CustomerBookingForm from './CustomerBookingForm';
import TicketPolicy from './TicketPolicy';
import BookingSummary from './BookingSummary';
import SeatMap from './SeatMap'; 
import { notification } from 'antd'; 
import { WarningOutlined } from '@ant-design/icons';

const BookingPage = () => {
  // hooks
  const { tripId } = useParams();
  const location = useLocation();
  const dispatch = useDispatch();
  const [apiNotification, contextHolder] = notification.useNotification();
  const openErrorNotification = (message, desc) => {
    apiNotification.error({
      message: message,
      description: desc,
      icon: <WarningOutlined style={{ color: '#fa0707ff' }} />,
      duration: 2,
    });
  };

  // local state
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [isReadPolicy, setIsReadPolicy] = useState(false);
  const [totalPrice, setTotalPrice] = useState(0);

  // reducer state
  const { trip: tripFromState } = location.state || {};
  const { seatsByTrip, tripsByRoute } = useSelector((state) => state.trips);

  const trip =
    tripFromState || tripsByRoute?.find((t) => t.id === parseInt(tripId));
  console.log('Trip from state:', tripFromState);
  console.log('Trip:', trip);
  
  const [selectedSeatIds, setSelectedSeatIds] = useState([]);
  const handleToggleSeat = useCallback((seat) => { 
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
  }, [setSelectedSeatIds, openErrorNotification]);

  useEffect(() => {
    if (tripId && seatsByTrip.length === 0) {
      dispatch(fetchSeatsByTrip(parseInt(tripId)));
    }
  }, [tripId, seatsByTrip, dispatch]);

  // tinh tong tien
  useEffect(() => {
    setTotalPrice(selectedSeatIds?.length * trip.base_price || 0);
  }, [selectedSeatIds, trip]);

  const handleBookingInfo = () => {
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
    alert('Thong tin dat ve: ' + JSON.stringify(bookingInfo, null, 2));
  };

  if (!trip) {
    return (
      <Container sx={{ mt: 3 }}>
        <Typography>Đang tải thông tin chuyến đi...</Typography>
      </Container>
    );
  }

  console.log('Seats by trip:', seatsByTrip);
  console.log('Selected seat IDs:', selectedSeatIds);
  console.log('Selected trip:', trip);

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
              So do xe cho trip {tripId} (Tong so ghe:{' '}
              {trip?.bus?.total_seats || '...'})
              <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
                Sơ đồ ghế
              </Typography>
              <SeatMap
                seats={seatsByTrip}
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
          <Grid
            container
            size={{ xs: 12, md: 4 }}
            sx={{
              background: 'var(--color-white)',
              borderRadius: '8px',
              boxShadow: 'var(--box-shadow)',
              // minHeight: '100vh',
              padding: '16px',
            }}
          >
            <Grid item size={12}>
              <BookingSummary
                title="Thông tin lượt đi"
                routeLabel={`${trip?.origin || '...'} - ${
                  trip?.destination || '...'
                }`}
                departureTimeLabel={trip?.departure_time || '...'}
                seatCount={selectedSeatIds?.length || 0}
                seatNumbers={selectedSeatIds}
                dropoffPoint={trip?.dropoff_point || '...'}
                fare={totalPrice || 0}
                paymentFee={trip?.payment_fee || 0}
              />
            </Grid>
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
              Thanh toán
            </Button>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default BookingPage;
