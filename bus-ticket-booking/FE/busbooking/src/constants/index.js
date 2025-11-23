const API_DOMAIN = process.env.REACT_APP_GATEWAY_URL || "http://localhost:8000";

const PAYMENT_METHOD = {
    MOMO: 'MOMO',
    VNPAY: 'VNPAY',
    CASH: 'CASH',
} 

const PREFIX_SERVICES = {
    BOOKINGS: '/bookings',
    TRIPS: '/trips',
    USERS: '/users',
    NOTIFICATIONS: '/notifications',
    PAYMENTS: '/payments',
}

export const BOOKING_STATUS = {
    PENDING: {
        label: 'Đang chờ xử lý',
        color: 'orange',
        value: 'PENDING'
    },
    PAID: {
        label: 'Đã thanh toán',
        color: 'green',
        value: 'PAID'
    }, 
    CANCELLED: {
        label: 'Đã hủy',
        color: 'red',
        value: 'CANCELLED'
    },
    REFUNDED: {
        label: 'Đã hoàn tiền',
        color: 'blue',
        value: 'REFUNDED'
    },
}
// console.log("API_DOMAIN", API_DOMAIN);
export {
    API_DOMAIN,
    PAYMENT_METHOD,
    PREFIX_SERVICES,
};