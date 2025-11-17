import { useState } from 'react';
import { useSelector } from 'react-redux';
import {
  Card,
  CardActionArea,
  Container,
  Grid,
  Typography,
} from '@mui/material';

const RouteList = () => {
  const { routes } = useSelector((state) => state.trips);
  const [selectedRouteId, setSelectedRouteId] = useState(null);

  const handleClick = (route) => {
    console.log('Route clicked:', route);
    setSelectedRouteId(route.id);
    // Sau này có thể navigate tới /trips?origin=... ở đây luôn
  };

  return (
    <>
      <h2>Route List</h2>
      <Container maxWidth="md" sx={{ mt: 2, mb: 2 }}>
        <Grid container spacing={2}>
          {routes && routes.length > 0 ? (
            routes.map((route) => (
              <Grid item size={12} key={route.id}>
                <RouteCard
                  route={route}
                  onClick={handleClick}
                  selected={route.id === selectedRouteId}
                />
              </Grid>
            ))
          ) : (
            <Typography>No routes available</Typography>
          )}
        </Grid>
      </Container>
    </>
  );
};

const RouteCard = ({ route, onClick, selected }) => {
  return (
    <Card
      sx={{
        width: '100%',
        borderRadius: 2,
        boxShadow: selected ? 4 : 1,
        border: selected ? '2px solid #1976d2' : '1px solid #ddd',
      }}
    >
      <CardActionArea
        onClick={() => onClick(route)}
        sx={{
          p: 2,
          cursor: 'pointer',
          '&:hover': {
            backgroundColor: '#f5f5f5',
          },
        }}
      >
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Typography variant="subtitle1" fontWeight="bold">
              {route.origin} → {route.destination}
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="body2">
              Distance: {route.distance_km} km
            </Typography>
            <Typography variant="body2">
              Duration: {route.estimated_duration_hour} hours
            </Typography>
          </Grid>
        </Grid>
      </CardActionArea>
    </Card>
  );
};

export default RouteList;
