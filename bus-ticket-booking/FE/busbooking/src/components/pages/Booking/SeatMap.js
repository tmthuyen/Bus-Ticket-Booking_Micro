// SeatMap.jsx
import { Box, Typography, Button } from "@mui/material";
import { memo } from "react";

const SeatMap = ({ seats = [], selectedSeatIds = [], onToggleSeat }) => {
  if (!seats.length) {
    return <Typography>Không có dữ liệu ghế.</Typography>;
  } 
  console.log("Rendering SeatMap with seats:", seats);

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
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
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
              border: "1px solid #ddd",
              p: 2,
              background: "var(--gradient-soft)",
            }}
          >
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Floor {floor}
            </Typography>

            {/* Mỗi row = 1 hàng ghế */}
            {rows.map((row) => { 
              const rowSeats = seatsOnFloor.filter(
                (s) => s.row_index === row
              );

              // A side & B side (dựa vào ký tự đầu seat_number)
              const aSeats = rowSeats.filter((s) =>
                s.seat_number.startsWith("A")
              );
              const bSeats = rowSeats.filter((s) =>
                s.seat_number.startsWith("B")
              );

              const aLeft = aSeats.find((s) => s.col_index === 1);
              const aRight = aSeats.find((s) => s.col_index === 2);
              const bLeft = bSeats.find((s) => s.col_index === 1);
              const bRight = bSeats.find((s) => s.col_index === 2);

              const renderSeat = (seat) => {
                if (!seat) return <Box sx={{ width: 48 }} />;

                const selected = isSelected(seat.seat_id);

                // console.log("Rendering seat:", seat.seat_number, "Selected:", selected);
                return (
                  <Button
                    key={seat.seat_id}
                    variant={selected ? "contained" : "outlined"}
                    size="small"
                    onClick={() => onToggleSeat?.(seat)}
                    sx={{
                      minWidth: 48,
                      height: 36,
                      p: 0,
                      borderRadius: 1,
                      textTransform: "none",
                      fontSize: 12,
                      backgroundColor: selected ? "primary.main" : "white",
                      color: selected ? "primary.contrastText" : "text.primary",
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
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: 2,
                    mb: 1,
                  }}
                >
                  {/* Bên A */}
                  <Box sx={{ display: "flex", gap: 1 }}>
                    {renderSeat(aLeft)}
                    {renderSeat(aRight)}
                  </Box>

                  {/* Lối đi */}
                  <Box sx={{ width: 32 }} />

                  {/* Bên B */}
                  <Box sx={{ display: "flex", gap: 1 }}>
                    {renderSeat(bLeft)}
                    {renderSeat(bRight)}
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
