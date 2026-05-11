import { useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { fetchTripsByRoute } from '../../../store/actions/tripsAction';
import { Container, Grid } from '@mui/material';
import TripList from './TripList';
import { todayVN } from '../../../utils/formatTime';

const TripPage = () => {
  const [searchParams] = useSearchParams();
  const origin_code = searchParams.get('origin');
  const destination_code = searchParams.get('destination');
  const from_date = searchParams.get('from_date');

  const dispatch = useDispatch();
  const { tripsByRoute, loading: loadingTrips } = useSelector(
    (state) => state.trips
  );

  const navigate = useNavigate();

  const handleChooseTrip = (trip) => {
    console.log('Choose trip:', trip);
    navigate(
      `/bookings/${trip.id}?origin=${origin_code}&destination=${destination_code}&from_date=${from_date}`,
      {
        state: { trip: trip, from_date: from_date },
      }
    );
  };

  const lastParamsRef = useRef(null);

  useEffect(() => {
    if (!origin_code || !destination_code || !from_date) return;

    const key = `${origin_code}-${destination_code}-${from_date}`;

    // Nếu params trùng với lần trước → không fetch nữa
    if (lastParamsRef.current === key) {
      console.log('Skip fetch, params not changed');
      return;
    }

    lastParamsRef.current = key;
    if (from_date < todayVN()) {
      console.log('From date is in the past, skip fetch trips');
      return;
    }
    dispatch(fetchTripsByRoute(origin_code, destination_code, from_date));
  }, [origin_code, destination_code, from_date, dispatch]);

  return (
    <>
      <Container
        maxWidth="lg"
        style={{ marginTop: '20px', marginBottom: '20px' }}
      >
        <Grid container spacing={2} justifyContent={'center'}>
          {from_date < todayVN() ? (
            <p style={{ color: 'red' }}>
              From date is in the past. Please select a valid date.
            </p>
          ) : (
            <TripList
              title={
                origin_code.toUpperCase() +
                ' - ' +
                destination_code.toUpperCase()
              }
              subtitleDate={from_date}
              trips={tripsByRoute}
              onBook={(t) => handleChooseTrip(t)}
              onChooseSeats={(t) => handleChooseTrip(t)}
              loading={loadingTrips}
            />
          )}
        </Grid>
      </Container>
    </>
  );
};

export default TripPage;
