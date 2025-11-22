// SeatMap.jsx
import { Box, Typography, Button } from '@mui/material';
import { memo } from 'react';

const SeatMap = ({ seats = [], selectedSeatIds = [], onToggleSeat }) => {
  if (!seats.length) {
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
                    onClick={() => onToggleSeat?.(seat)}
                    sx={{
                      minWidth: 48,
                      height: 36,
                      p: 0,
                      borderRadius: 1,
                      textTransform: 'none',
                      fontSize: 12,
                      backgroundColor: selected ? 'primary.main' : 'white',
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
