const API_DOMAIN = process.env.REACT_APP_GATEWAY_URL || "http://localhost:8000";

const PAYMENT_METHOD = {
    MOMO: 'MOMO',
    VNPAY: 'VNPAY',
    CASH: 'CASH',
}
// console.log("API_DOMAIN", API_DOMAIN);
export {
    API_DOMAIN,
    PAYMENT_METHOD
};