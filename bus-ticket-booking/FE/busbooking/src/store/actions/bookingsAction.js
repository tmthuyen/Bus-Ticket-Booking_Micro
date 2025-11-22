import { parseAxiosError } from "../../api/api"; 
import { createBookingApi, getBookingByCodeApi, getSeatsBookedByTripApi, getTicketByCodeAndEmailApi } from "../../api/bookingsApi";

const BOOKINGS_ACTION_TYPES = {
  CREATE_BOOKINGS_REQUEST: "CREATE_BOOKINGS_REQUEST",
  CREATE_BOOKINGS_SUCCESS: "CREATE_BOOKINGS_SUCCESS",
  CREATE_BOOKINGS_FAILURE: "CREATE_BOOKINGS_FAILURE",
  FETCH_BOOKING_BY_CODE_REQUEST: "FETCH_BOOKING_BY_CODE_REQUEST",
  FETCH_BOOKING_BY_CODE_SUCCESS: "FETCH_BOOKING_BY_CODE_SUCCESS",
  FETCH_BOOKING_BY_CODE_FAILURE: "FETCH_BOOKING_BY_CODE_FAILURE",
  FETCH_SEATS_BOOKED_BY_TRIP_REQUEST: "FETCH_SEATS_BOOKED_BY_TRIP_REQUEST",
  FETCH_SEATS_BOOKED_BY_TRIP_SUCCESS: "FETCH_SEATS_BOOKED_BY_TRIP_SUCCESS",
  FETCH_SEATS_BOOKED_BY_TRIP_FAILURE: "FETCH_SEATS_BOOKED_BY_TRIP_FAILURE",
  FETCH_TICKET_BY_CODE_AND_EMAIL_REQUEST: "FETCH_TICKET_BY_CODE_AND_EMAIL_REQUEST",
  FETCH_TICKET_BY_CODE_AND_EMAIL_SUCCESS: "FETCH_TICKET_BY_CODE_AND_EMAIL_SUCCESS",
  FETCH_TICKET_BY_CODE_AND_EMAIL_FAILURE: "FETCH_TICKET_BY_CODE_AND_EMAIL_FAILURE", 
}

export { BOOKINGS_ACTION_TYPES };

export const createBookingAction = (bookingData) => {
  return async (dispatch) => {
    dispatch({ type: BOOKINGS_ACTION_TYPES.CREATE_BOOKINGS_REQUEST });

    try {
      const { responseApi } = await createBookingApi(bookingData);
      dispatch({ 
        type: BOOKINGS_ACTION_TYPES.CREATE_BOOKINGS_SUCCESS, 
        payload: { data: responseApi.data, message: "Tạo vé dự định thành công" } 
      });
    } catch (error) {
      console.error("fetchRoutes error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({ 
        type: BOOKINGS_ACTION_TYPES.CREATE_BOOKINGS_FAILURE, 
        payload: { 
          error: parsedError.message || "Tạo vé dự định thất bại", 
          message: parsedError.message || "Tạo vé dự định thất bại" 
        } 
      });
    }
  }
}

export const fetchBookingByCodeAction = (booking_code) => {
  return async (dispatch) => {
    dispatch({ type: BOOKINGS_ACTION_TYPES.FETCH_BOOKING_BY_CODE_REQUEST });
    try {
      const { responseApi } = await getBookingByCodeApi(booking_code);
      dispatch({
        type: BOOKINGS_ACTION_TYPES.FETCH_BOOKING_BY_CODE_SUCCESS,
        payload: { data: responseApi.data, message: "Lấy thông tin booking thành công" },
      });
    } catch (error) {
      console.error("fetchBookingByCodeAction error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({
        type: BOOKINGS_ACTION_TYPES.FETCH_BOOKING_BY_CODE_FAILURE,
        payload: { error: parsedError.message || "Lấy thông tin booking thất bại", message: parsedError.message || "Lấy thông tin booking thất bại" },
      });
    }
  }
}

export const fetchSeatsBookedByTripAction = (trip_id) => {
  return async (dispatch) => {
    dispatch({ type: BOOKINGS_ACTION_TYPES.FETCH_SEATS_BOOKED_BY_TRIP_REQUEST });
    try {
      const { responseApi } = await getSeatsBookedByTripApi(trip_id);
      dispatch({
        type: BOOKINGS_ACTION_TYPES.FETCH_SEATS_BOOKED_BY_TRIP_SUCCESS,
        payload: { data: responseApi.data, message: "Lấy thông tin ghế đã đặt thành công" },
      });
    } catch (error) {
      console.error("fetchSeatsBookedByTripAction error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({
        type: BOOKINGS_ACTION_TYPES.FETCH_SEATS_BOOKED_BY_TRIP_FAILURE,
        payload: { error: parsedError.message || "Lấy thông tin ghế đã đặt thất bại", message: parsedError.message || "Lấy thông tin ghế đã đặt thất bại" },
      });
    }
  }
}

export const fetchTicketByCodeAndEmailAction = (code, email) => {
  return async (dispatch) => {
    dispatch({ type: BOOKINGS_ACTION_TYPES.FETCH_TICKET_BY_CODE_AND_EMAIL_REQUEST }); 
    console.log("fetchTicketByCodeAndEmailAction called with code:", code, "email:", email);
    try {
      const { responseApi } = await getTicketByCodeAndEmailApi(code, email); 
      console.log("fetchTicketByCodeAndEmailAction responseApi: ", responseApi);
      dispatch({  
        type: BOOKINGS_ACTION_TYPES.FETCH_TICKET_BY_CODE_AND_EMAIL_SUCCESS, 
        payload: { data: responseApi.data, message: "Tra cứu vé thành công" }, 
      }); 
    } catch (error) {
      console.error("fetchTicketByCodeAndEmailAction error: ", error); 
      const parsedError = parseAxiosError(error);
      dispatch({
        type: BOOKINGS_ACTION_TYPES.FETCH_TICKET_BY_CODE_AND_EMAIL_FAILURE,
        payload: { error: parsedError.message || "Tra cứu vé thất bại", message: parsedError.message || "Tra cứu vé thất bại" },
      });
    }
  }
}