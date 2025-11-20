import { useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from 'react-router-dom';
import { fetchTripsByRoute } from '../../../store/actions/tripsAction';
import { Container, Grid, Skeleton, Typography } from '@mui/material';
import { formatVNDate } from '../../../utils/formatTime';
import TripList, { DemoTripList } from './TripList';

const TripPage = () => {
  const [searchParams] = useSearchParams();
  const origin_code = searchParams.get('origin');
  const destination_code = searchParams.get('destination');
  const from_date = searchParams.get('from_date');

  const dispatch = useDispatch();
  const { tripsByRoute, loading: loadingTrips } = useSelector(
    (state) => state.trips
  );

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
    dispatch(fetchTripsByRoute(origin_code, destination_code, from_date));
  }, [origin_code, destination_code, from_date, dispatch]);

  return (
    <>
      <Container
        maxWidth="lg"
        style={{ marginTop: '20px', marginBottom: '20px' }}
      >
        <Grid container spacing={2}>
          <TripList
            title={origin_code.toUpperCase() + ' - ' + destination_code.toUpperCase()}
            subtitleDate={from_date}
            trips={tripsByRoute}
            onBook={(t) => alert(`Đặt vé cho trip #${t.id}`)}
            onChooseSeats={(t) => alert(`Xem sơ đồ ghế trip #${t.id}`)}
            loading={loadingTrips}
          />
        </Grid>
      </Container>
    </>
  );
};

export default TripPage;
