import { useState } from 'react';
import { useSelector } from 'react-redux';
import { Box, Card, CardActionArea, Grid, Typography } from '@mui/material';
import { MultipleStop } from '@mui/icons-material';

const RouteList = ({ onRouteClick }) => {
  const { routes } = useSelector((state) => state.trips);
  const [selectedRouteId, setSelectedRouteId] = useState(null);

  const handleClick = (route) => {
    console.log('Route clicked:', route);
    setSelectedRouteId(route.id);
    // Sau này có thể navigate tới /trips?origin=... ở đây luôn
  };

  return (
    <>
      <Grid
        container
        spacing={2}
        sx={{ my: 2, maxWidth: '100%', overflowX: 'auto' }}
      >
        {routes && routes.length > 0 ? (
          routes.map((route) => (
            <Grid size={12} key={route.id}>
              <RouteCard
                route={route}
                onClick={onRouteClick || handleClick}
                selected={route.id === selectedRouteId}
              />
            </Grid>
          ))
        ) : (
          <Typography>No routes available</Typography>
        )}
      </Grid>
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
        border: selected ? '1px solid var(--color-primary)' : '1px solid #ddd',
      }}
    >
      <CardActionArea
        onClick={() => onClick(route)}
        sx={{
          p: 1,
          cursor: 'pointer',
          '&:hover': {
            background: 'var(--gradient-soft)',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.4)',
          },
        }}
      >
        <Grid container spacing={1}>
          <Grid 
            size={{ xs: 12, sm: 6 }}
            sx={{
              display: 'flex',
              justifyContent: 'start',
              alignItems: 'center',
            }}
          >
            <Typography variant="subtitle1" fontWeight="bold">
              {route.origin}
            </Typography>
            <MultipleStop sx={{ mx: 1 }} />
            <Typography variant="subtitle1" fontWeight="bold">
              {route.destination}
            </Typography>
          </Grid>

          <Grid 
            size={{ xs: 12, sm: 6 }}
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <Typography variant="body2">
              Distance: {route.distance_km} km
            </Typography>
            <Typography variant="body2">
              Duration: {route.estimated_duration_hour} hours
            </Typography>

            <Box sx={{
              border: "1px solid var(--color-primary)",
              borderRadius: "8px",
              padding: "4px 12px",
              cursor: "pointer",
              backgroundColor: selected ? 'var(--color-primary)' : 'transparent', 
            }}>
              <Typography 
                variant="button"
                color="primary"
                sx={{ color: selected ? '#fff' : 'var(--color-primary)' }}
              >
                Select
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardActionArea>
    </Card>
  );
};

export default RouteList;
