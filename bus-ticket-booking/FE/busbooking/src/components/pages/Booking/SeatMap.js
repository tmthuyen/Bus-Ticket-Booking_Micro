// SeatMap.jsx
import { Box, Typography, Button } from '@mui/material';
import { memo } from 'react';

const COLOR = {
  is_booked: '#cdccccff', // red
  available: '#52c41a', // green
  selected: '#1890ff', // blue
}

const showColor = (seat, selected) => {
  if (seat.is_booked) return COLOR.is_booked;
  if (selected) return COLOR.selected;
  return COLOR.available;
}

const SeatMap = ({ total_seats=0, total_booked=0, seats = [], selectedSeatIds = [], onToggleSeat }) => {
  if (!seats.length || total_seats === 0) {
    return <Typography>Không có dữ liệu ghế.</Typography>;
  }
  console.log('Rendering SeatMap with seats:', seats);

  // Lấy danh sách row & floor
  const floors = [...new Set(seats.map((s) => s.floor))].sort((a, b) => a - b);

  const isSelected = (seatId) => {
    let found = false;
    selectedSeatIds.forEach((s) => {
      if (s.seat_id === seatId) found = true;
    });
    return found;
  };

  // console.log("Selected Seat IDs:", selectedSeatIds);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'row', gap: 3, justifyContent: 'space-around' }}>
      {/* Màu sắc hướng dẫn */}
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        <Typography variant="subtitle1" fontWeight="bold">
          Chú thích:
      </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box
            sx={{ width: 24, height: 24, backgroundColor: COLOR.available, borderRadius: 1 }}
          />
          <Typography>Ghế trống</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box
            sx={{ width: 24, height: 24, backgroundColor: COLOR.is_booked, borderRadius: 1 }}
          />
          <Typography>Ghế đã đặt</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box
            sx={{ width: 24, height: 24, backgroundColor: COLOR.selected, borderRadius: 1 }}
          />
          <Typography>Ghế đã chọn</Typography>
        </Box>  
      </Box>
      {floors.map((floor) => {
        const seatsOnFloor = seats.filter((s) => s.floor === floor);
        const rows = [...new Set(seatsOnFloor.map((s) => s.row_index))].sort(
          (a, b) => a - b
        );

        return (
          <Box
            key={floor}
            sx={{
              borderRadius: 2,
              border: '1px solid #ddd',
              boxShadow: 'var(--box-shadow)',
              p: 3,
              background: 'var(--color-white)',
            }}
          >
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Floor {floor}
            </Typography>

            {/* Mỗi row = 1 hàng ghế */}
            {rows.map((row) => {
              const rowSeats = seatsOnFloor.filter((s) => s.row_index === row);

              const left = rowSeats.find((s) => s.col_index === 1);
              const right = rowSeats.find((s) => s.col_index === 2); 

              const renderSeat = (seat) => {
                if (!seat) return <Box sx={{ width: 48 }} />;

                const selected = isSelected(seat.seat_id);

                // console.log("Rendering seat:", seat.seat_number, "Selected:", selected);
                return (
                  <Button
                    key={seat.seat_id}
                    variant={selected ? 'contained' : 'outlined'}
                    size="small"
                    onClick={seat.is_booked ? null : () => onToggleSeat(seat)}
                    sx={{
                      minWidth: 48,
                      height: 36,
                      p: 0,
                      borderRadius: 1,
                      textTransform: 'none',
                      fontSize: 12,
                      cursor: seat.is_booked ? 'not-allowed' : 'pointer',
                      pointerEvents: seat.is_booked ? 'none' : 'auto',
                      // opacity: seat.is_booked ? 0.5 : 1,
                      backgroundColor: showColor(seat, selected),
                      color: selected ? 'primary.contrastText' : 'text.primary',
                    }}
                  >
                    {seat.seat_number}
                  </Button>
                );
              };

              return (
                <Box
                  key={`${floor}-${row}`}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: 3,
                    mb: 1,
                  }}
                > 
                  <Box sx={{ display: 'flex', gap: 3 }}>
                    {renderSeat(left)}
                    {renderSeat(right)}
                  </Box>  
                </Box>
              );
            })}
          </Box>
        );
      })}
    </Box>
  );
};

export default memo(SeatMap);
