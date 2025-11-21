import { parseAxiosError } from "../../api/api"; 
import { createBookingApi, getSeatsBookedByTripApi, getTicketByCodeAndEmailApi } from "../../api/bookingsApi";

const BOOKINGS_ACTION_TYPES = {
  CREATE_BOOKINGS_REQUEST: "CREATE_BOOKINGS_REQUEST",
  CREATE_BOOKINGS_SUCCESS: "CREATE_BOOKINGS_SUCCESS",
  CREATE_BOOKINGS_FAILURE: "CREATE_BOOKINGS_FAILURE",
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
    try {
      const { responseApi } = await getTicketByCodeAndEmailApi(code, email); 
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