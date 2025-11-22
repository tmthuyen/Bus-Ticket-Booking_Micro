import { useState } from 'react';
import { 
  Typography,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Collapse,
  IconButton,
  Box,
  Divider,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { formatVN, formatVNDate } from '../../../utils/formatTime';

// Helper format số tiền
const formatCurrency = (value) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(
    value || 0
  );

const BookingSummary = ({
  title = 'Thông tin lượt đi',
  routeLabel, // "Bạc Liêu - Miền Tây"
  departureTimeLabel, // "06:00 26/11/2025"
  seatCount = 0, // số lượng ghế
  seatNumbers = [], // array ["A01", "A02"]
  fare = 0, // giá vé lượt đi
  paymentFee = 0, // phí thanh toán
}) => {
  const [openPriceDetail, setOpenPriceDetail] = useState(true);

  const total = (fare || 0) + (paymentFee || 0);

  return (
    <>
      <Box mb={2}>
        <Typography variant="h6" fontWeight={600} gutterBottom>
          {title}
        </Typography>

        {/* Bảng thông tin chính */}
        <Table size="small" aria-label="booking summary">
          <TableBody>
            <TableRow>
              <TableCell
                sx={{ fontWeight: 600 }}
              >
                Tuyến xe
              </TableCell>
              <TableCell align="right">
                {routeLabel}
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Thời gian xuất bến</TableCell>
              <TableCell align="right">{formatVNDate(departureTimeLabel, { withTime: true })}</TableCell>
            </TableRow>

            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Số lượng ghế</TableCell>
              <TableCell align="right">{seatCount} ghế</TableCell>
            </TableRow>

            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Số ghế</TableCell>
              <TableCell align="right">
                {seatNumbers.length ? seatNumbers.map((item) => item.seat_number).join(', ') : 'Chưa chọn ghế'}
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Tổng tiền lượt đi</TableCell>
              <TableCell align="right" sx={{ fontWeight: 600, color: 'primary.main' }}>
                {formatCurrency(total)}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Hàng "Chi tiết giá" + toggle */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Typography variant="subtitle1" fontWeight={600}>
          Chi tiết giá
        </Typography>
        <IconButton
          size="small"
          onClick={() => setOpenPriceDetail((prev) => !prev)}
        >
          <ExpandMoreIcon
            sx={{
              transform: openPriceDetail ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.2s ease',
            }}
          />
        </IconButton>
      </Box>

      <Collapse in={openPriceDetail} timeout="auto" unmountOnExit>
        <Table size="small" sx={{ mt: 1 }}>
          <TableBody>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none' }}>
                Giá vé lượt đi
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {formatCurrency(fare)}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ borderBottom: 'none' }}>
                Phí thanh toán
              </TableCell>
              <TableCell
                align="right"
                sx={{ borderBottom: 'none', fontWeight: 500 }}
              >
                {formatCurrency(paymentFee)}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Tổng tiền</TableCell>
              <TableCell
                align="right"
                sx={{ fontWeight: 700, color: 'primary.main' }}
              >
                {formatCurrency(total)}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Collapse>
    </>
  );
};

export default BookingSummary;
