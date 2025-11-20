import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Stack, 
  Skeleton,
} from '@mui/material'; 
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import SyncAltIcon from '@mui/icons-material/SyncAlt';
import { formatVNDate } from '../../../utils/formatTime';
import TripCard from './TripCard';

// ========= Status → MUI Chip color =========
export const statusChip = {
  SCHEDULED: { label: 'SCHEDULED', color: 'success' },
  BOARDING: { label: 'BOARDING', color: 'info' },
  DEPARTED: { label: 'DEPARTED', color: 'warning' },
  CANCELLED: { label: 'CANCELLED', color: 'error' },
  COMPLETED: { label: 'COMPLETED', color: 'default' },
};

export default function TripList({
  title,
  subtitleDate,
  trips,
  onBook,
  onChooseSeats,
  loading,
}) {
  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: 1200,
        mx: 'auto',
        px: { xs: 1.5, sm: 3 },
        py: 3,
      }}
    >
      {/* Header */}
      {(title || subtitleDate) && (
        <Box sx={{ mb: { xs: 2, sm: 3 } }}>
          {title && (
            <Stack direction="row" spacing={1} alignItems="center">
              <SyncAltIcon fontSize="small" />
              <Typography variant="h5" fontWeight={700}>
                {title} ({trips?.length || 0})
              </Typography>
            </Stack>
          )}
          {subtitleDate && (
            <Stack
              direction="row"
              spacing={1}
              alignItems="center"
              sx={{ mt: 0.5 }}
            >
              <CalendarMonthIcon fontSize="small" color="action" />
              <Typography variant="body2" color="text.secondary">
                {formatVNDate(subtitleDate, {
                  withWeekday: true,
                  withTime: false,
                })}
              </Typography>
            </Stack>
          )}
        </Box>
      )}

      {/* Loading skeleton */}
      {loading && (
        <Grid container spacing={2}>
          {Array.from({ length: 4 }).map((_, i) => (
            <Grid item size={12} md={6} key={i}>
              <Card elevation={0} variant="outlined">
                <Skeleton variant="rectangular" height={120} />
                <Box sx={{ p: 2 }}>
                  <Skeleton width="70%" height={24} />
                  <Skeleton width="40%" height={20} sx={{ mt: 1 }} />
                  <Skeleton variant="rounded" height={36} sx={{ mt: 2 }} />
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {!loading && trips?.length === 0 && (
        <Card elevation={0} variant="outlined">
          <CardContent>
            <Typography align="center" color="text.secondary">
              Không tìm thấy chuyến phù hợp.
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Trip cards */}
      {!loading && trips?.length > 0 && (
        <Grid container spacing={2}>
          {trips.map((t, idx) => (
            <TripCard
              key={t.id}
              t={t}
              idx={idx}
              onChooseSeats={onChooseSeats}
              onBook={onBook}
            />
          ))}
        </Grid>
      )}
    </Box>
  );
}


