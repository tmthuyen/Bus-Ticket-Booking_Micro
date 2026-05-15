import api from './api';

const PREFIX_SERVICE = '/bookings';
// GET /trips/routes
// {
//   "trip_id": 1,
//   "seat_numbers": ["string"],
//   "full_name": "string",
//   "phone": "stringstri",
//   "email": "user@example.com",
//   "total_price": 1
// }
export const createBookingApi = async (body) => {
  const res = await api.post(`${PREFIX_SERVICE}/`, {
    // data booking
    ...body,
  });
  // console.log("getRoutes: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

export const cancelBookingApi = async (bookingId) => {
  const res = await api.put(`${PREFIX_SERVICE}/${bookingId}/cancel`, { 
  });
  // console.log("getRoutes: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

// lay thong tin ghe da dat cua 1 chuyen di
export const getSeatsBookedByTripApi = async (trip_id) => {
  const res = await api.get(
    `${PREFIX_SERVICE}/trip/${trip_id}/booked-seats`
  );
  // console.log("getSeatsByTrip: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

// tra cuu ve bang booking_code va email
export const getTicketByCodeAndEmailApi = async (code, email) => {
  const res = await api.get(
    `${PREFIX_SERVICE}/search/${email}/${code}`
  );
  // console.log("getTicketByCodeAndEmail: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

// tra cuu ve bang booking_code va email
export const getTicketByBookingId = async (bookingId) => {
  const res = await api.get(
    `${PREFIX_SERVICE}/${bookingId}`
  );
  
  console.log("getTicketByBookingId: ", res);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

// lay thong tin booking theo booking_code
export const getBookingByCodeApi = async (booking_code) => {
  const res = await api.get(
    `${PREFIX_SERVICE}/code/${booking_code}`
  );
  console.log("getBookingByCode: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
}