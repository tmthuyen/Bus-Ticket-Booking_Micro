import api from './api';

const PREFIX_SERVICE = '/notifications'; 

// email, booking_code, otp
export const verifyOtp = async (body) => {
  const res = await api.post(`${PREFIX_SERVICE}/otp/verify`, {
    // data verify booking
    ...body,
  });
  // console.log("getRoutes: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

// email, booking_code
export const resendOtp = async (body) => {
  const res = await api.post(`${PREFIX_SERVICE}/otp/send`, {
    // data verify booking
    ...body,
  });
  // console.log("getRoutes: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};