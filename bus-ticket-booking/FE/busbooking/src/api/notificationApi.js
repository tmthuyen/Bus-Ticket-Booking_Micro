import api from './api';

const PREFIX_SERVICE = '/notifications'; 

// {
// email, code
export const verifyOtp = async (body) => {
  const res = await api.post(`${PREFIX_SERVICE}/otp/verify`, {
    // data booking
    ...body,
  });
  // console.log("getRoutes: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};