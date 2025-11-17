import { useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from 'react-router-dom';
import { fetchTripsByRoute } from '../../../store/actions/tripsAction';
import { Container, Grid, Skeleton, Typography } from '@mui/material'; 

const TripList = () => {
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
      <Container maxWidth="md" style={{ marginTop: '20px', marginBottom: '20px' }}>
        <Grid container spacing={2}>
          <Grid item size={12}>
            <Typography variant="h5">Trip List</Typography>
          </Grid>
          <Grid item size={12}>
            {loadingTrips ? (
              <>
                {Array.from({length: 10}).map((_, index) => (
                  <Skeleton 
                    key={index}
                    variant="rounded" 
                    height={100} 
                    width={'100%'} 
                    style={{ marginBottom: '10px' }} 
                  />
                ))} 
              </>
            ) : tripsByRoute && tripsByRoute.length > 0 ? (
              <Typography>Trips loaded. Number: {tripsByRoute.length}</Typography>
            ) : (
              <>
                <Typography>No trips found for the selected route and date.</Typography>
                {Array.from({length: 10}).map((_, index) => (
                  <Skeleton 
                    key={index}
                    variant="rounded" 
                    height={100} 
                    width={'100%'} 
                    style={{ marginBottom: '10px' }} 
                  />
                ))} 
              </>
            )}
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default TripList;
