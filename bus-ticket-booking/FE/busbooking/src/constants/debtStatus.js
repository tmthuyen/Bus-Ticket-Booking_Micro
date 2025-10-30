// src/constants/paymentStatus.js
export const DEBT_STATUS = {
  PENDING: { value: 'PENDING', color: 'orange', label: 'Đang thanh toán' },
  PAID: { value: 'PAID', color: 'green', label: 'Đã thanh toán' },
  OVERDUE: { value: 'OVERDUE', color: 'red', label: 'Quá hạn' },
  OPEN: { value: 'OPEN', color: 'blue', label: 'Chưa thanh toán' },
};