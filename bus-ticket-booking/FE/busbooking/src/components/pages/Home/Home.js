import { useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchRoutes,
  fetchTripsByRoute,
} from '../../../store/actions/tripsAction';
import { Link, useNavigate } from 'react-router-dom';
import {
  Autocomplete,
  Button,
  Container,
  Grid,
  Skeleton,
  TextField,
} from '@mui/material';
import useMessage from 'antd/es/message/useMessage';
import RouteList from '../Route/RouteList';

const Home = () => {
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [fromDate, setFromDate] = useState('');
  const [errors, setErrors] = useState({
    origin: false,
    destination: false,
    fromDate: false,
  });

  const navigate = useNavigate();
  const [messageApi, contextHolder] = useMessage();
  const dispatch = useDispatch();

  const { routes, tripsByRoute, loading } = useSelector((state) => state.trips);

  const places = useMemo(() => {
    const map = new Map();
    if (routes && routes.length > 0) {
      routes.forEach((route) => {
        if (route.origin && route.origin_code && !map.has(route.origin_code)) {
          map.set(route.origin_code, {
            label: route.origin,
            code: route.origin_code,
          });
        }
        if (
          route.destination &&
          route.destination_code &&
          !map.has(route.destination_code)
        ) {
          map.set(route.destination_code, {
            label: route.destination,
            code: route.destination_code,
          });
        }
      });
    }
    return Array.from(map.values());
  }, [routes]);

  const handleSearchRoute = () => {
    const newErrors = {
      origin: !origin,
      destination: !destination,
      fromDate: !fromDate,
    };
    setErrors(newErrors);
    if (newErrors.origin || newErrors.destination || newErrors.fromDate) return;
    if (origin.code === destination.code) {
      messageApi.error('Origin and Destination cannot be the same!');
      // setOrigin(null);
      setDestination(null);
      return;
    }

    const payload = {
      origin_code: origin.code,
      destination_code: destination.code,
      from_date: fromDate,
    };
    console.log('Search payload: ', payload);

    navigate(
      `/trips?origin=${payload.origin_code}&destination=${payload.destination_code}&from_date=${payload.from_date}`
    );
  };

  return (
    <>
      <Container maxWidth="lg" sx={{}}>
        {contextHolder}
        <h1>HOME PAGE</h1>
        {/* Truyền profile + refreshProfile cho các màn con */}
        {loading ? (
          <div
            style={{
              height: '60vh',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-around',
            }}
          >
            <Skeleton variant="rounded" width={'100%'} height={100} />
            <Skeleton variant="rounded" width={'100%'} height={300} />
          </div>
        ) : (
          <div>
            <Grid container spacing={1}>
              <Grid
                container
                size={12}
                spacing={1}
                sx={{
                  border: '1px solid aqua',
                  borderRadius: '8px',
                  padding: '10px',
                  marginBottom: '10px',
                }}
              >
                <Grid size={{ xs: 12, sm: 4 }}>
                  <Autocomplete
                    disablePortal
                    options={places}
                    getOptionLabel={(option) => option.label}
                    sx={{ width: '100%' }}
                    value={origin}
                    onChange={(e, newValue) => setOrigin(newValue)}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Select origin"
                        error={errors.origin}
                        helperText={errors.origin ? 'Origin is required' : ''}
                      />
                    )}
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 4 }}>
                  <Autocomplete
                    disablePortal
                    options={places}
                    getOptionLabel={(option) => option.label}
                    sx={{ width: '100%' }}
                    value={destination}
                    onChange={(e, newValue) => setDestination(newValue)}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Select destination"
                        error={errors.destination}
                        helperText={
                          errors.destination ? 'Destination is required' : ''
                        }
                      />
                    )}
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 4 }}>
                  {/* <Date */}
                  <TextField
                    fullWidth
                    label="Select date"
                    type="date"
                    value={fromDate}
                    onChange={(e) => setFromDate(e.target.value)}
                    error={errors.fromDate}
                    helperText={errors.fromDate ? 'Date is required' : ''}
                    InputLabelProps={{ shrink: true }}
                  />
                </Grid>
                <Grid size={12} sx={{ textAlign: 'center', mt: 1 }}>
                  <Button variant="contained" onClick={handleSearchRoute}>
                    SEARCH TRIPS
                  </Button>
                </Grid>
              </Grid>
              <Grid size={12}>SHOW NEWEST TRIPS</Grid>
              <Grid size={12}>SLIDES</Grid>
            </Grid>

            <h2>Available Routes: {routes.length}</h2>
            <RouteList routes={routes} />
          </div>
        )}
      </Container>
    </>
  );
};

export default Home;
