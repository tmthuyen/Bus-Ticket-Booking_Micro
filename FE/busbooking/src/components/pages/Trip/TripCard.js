import { motion } from 'framer-motion';
import {
  Card,
  CardHeader,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Button,
  Grid,
  Stack,
  Divider,
} from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import DirectionsBusIcon from '@mui/icons-material/DirectionsBus';
import SyncAltIcon from '@mui/icons-material/SyncAlt';
import EventSeatIcon from '@mui/icons-material/EventSeat';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ConfirmationNumberIcon from '@mui/icons-material/ConfirmationNumber';
import { diffMinutes, formatHM, formatVNDate } from '../../../utils/formatTime';
import { statusChip } from './TripList';

const TripCard = ({ t, idx, onChooseSeats, onBook }) => {
  return (
    <>
      <Grid item size={12} key={t.id}>
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.05 }}
        >
          <Card
            elevation={0}
            variant="outlined"
            sx={{ width: '100%', borderRadius: 3, '&:hover': { boxShadow: 4 } }}
          >
            <CardHeader
              sx={{ pb: 0.5 }}
              title={
                <Stack
                  direction="row"
                  alignItems="center"
                  justifyContent="space-between"
                  spacing={1}
                >
                  <Stack
                    direction="row"
                    spacing={1.5}
                    alignItems="center"
                    sx={{ minWidth: 0 }}
                  >
                    <LocationOnIcon color="action" fontSize="small" />
                    <Typography variant="subtitle1" fontWeight={600} noWrap>
                      {t.origin} → {t.destination}
                    </Typography>
                  </Stack>
                  {(() => {
                    const meta = statusChip[t.status] || statusChip.SCHEDULED;
                    return (
                      <Chip
                        size="small"
                        label={meta.label}
                        color={meta.color}
                        variant="outlined"
                      />
                    );
                  })()}
                </Stack>
              }
            />

            <CardContent sx={{ pt: 1.5, width: '100%' }}>
              {/* Times & duration */}
              <Grid container spacing={1.5} justifyContent={'space-between'} alignItems="flex-start">
                <Grid item size={{ xs: 12, md: 4 }}>
                  <Stack spacing={0.5}>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <AccessTimeIcon color="action" fontSize="small" />
                      <Typography variant="body2" fontWeight={600}>
                        Khởi hành
                      </Typography>
                    </Stack>
                    <Typography variant="body1">
                      {formatVNDate(t.departure_time, {
                        withWeekday: true,
                        withTime: true,
                      })}
                    </Typography>
                  </Stack>
                </Grid>
                <Grid item size={{ xs: 12, md: 4 }}>
                  <Stack spacing={0.5}>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <AccessTimeIcon color="action" fontSize="small" />
                      <Typography variant="body2" fontWeight={600}>
                        Kết thúc
                      </Typography>
                    </Stack>
                    <Typography variant="body1">
                      {formatVNDate(t.arrival_time, {
                        withWeekday: true,
                        withTime: true,
                      })}
                    </Typography>
                  </Stack>
                </Grid>
                <Grid item size={{ xs: 12, md: 4 }}>
                  <Stack alignItems="flex-start" spacing={0.5}>
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ textTransform: 'uppercase' }}
                    >
                      Thời lượng
                    </Typography>
                    <Typography variant="subtitle1" fontWeight={700}>
                      {formatHM(
                        t.estimated_duration ??
                          (t.arrival_time
                            ? diffMinutes(t.departure_time, t.arrival_time)
                            : undefined)
                      )}
                    </Typography>
                  </Stack>
                </Grid>
              </Grid>

              <Divider sx={{ my: 1.5 }} />

              {/* Bus & meta */}
              <Grid container spacing={1.2} sx={{ width: '100%', justifyContent: 'space-between' }}>
                <Grid item size={{ xs: 6, md: 3 }}>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <DirectionsBusIcon fontSize="small" />
                    <Typography variant="body2" color="text.primary">
                      {t.bus?.bus_model?.name || 'Xe giường/ghế'}
                    </Typography>
                  </Stack>
                </Grid>
                <Grid item size={{ xs: 6, md: 3 }}>
                  <Stack
                    direction="row"
                    spacing={1}
                    alignItems="center"
                    justifyContent={{ xs: 'flex-end', md: 'center' }}
                  >
                    <EventSeatIcon fontSize="small" />
                    <Typography variant="body2">{t.total_seats} ghế</Typography>
                  </Stack>
                </Grid>
                <Grid item size={{ xs: 6, md: 3 }}>
                  <Stack direction="row" spacing={1} alignItems="flex-end">
                    <ConfirmationNumberIcon fontSize="small" />
                    <Typography variant="body2">
                      Biển số: {t.plate_number || t.bus?.plate_number || '--'}
                    </Typography>
                  </Stack>
                </Grid>
                <Grid item size={{ xs: 6, md: 3 }}>
                  <Stack
                    direction="row"
                    spacing={1}
                    alignItems="center"
                    justifyContent="flex-end"
                  >
                    <SyncAltIcon fontSize="small" />
                    <Typography variant="body2">
                      {(t.distance_km ?? 0).toLocaleString('vi-VN')} km
                    </Typography>
                  </Stack>
                </Grid>
              </Grid>
            </CardContent>

            <CardActions
              sx={{ px: 2, pb: 2, pt: 0, justifyContent: 'space-between' }}
            >
              <Stack
                direction="row"
                spacing={1}
                alignItems="center"
                color="text.secondary"
              >
                <Typography variant="caption">Mã chuyến:</Typography>
                <Typography variant="caption" fontWeight={600}>
                  #{t.id}
                </Typography>
              </Stack>
              <Stack direction="row" spacing={1}>
                <Button
                  variant="outlined"
                  onClick={() => onChooseSeats?.(t)}
                  endIcon={<ChevronRightIcon fontSize="small" />}
                >
                  Chọn ghế
                </Button>
                <Button variant="contained" onClick={() => onBook?.(t)}>
                  Đặt vé
                </Button>
              </Stack>
            </CardActions>
          </Card>
        </motion.div>
      </Grid>
    </>
  );
};

export default TripCard;