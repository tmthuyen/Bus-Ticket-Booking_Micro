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

// lay thong tin ghe da dat cua 1 chuyen di
export const getSeatsBookedByTripApi = async (trip_id) => {
  const res = await api.get(
    `${PREFIX_SERVICE}/seats-booked-by-trip/${trip_id}`
  );
  // console.log("getSeatsByTrip: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};

// tra cuu ve
export const getTicketByCodeAndEmailApi = async (code, email) => {
  const res = await api.get(
    `${PREFIX_SERVICE}/ticket-by-code-and-email`, { params: { code, email } }
  );
  // console.log("getTicketByCodeAndEmail: ", res.data);
  return {
    responseApi: res.data,
  }; // tuỳ backend trả data gì
};