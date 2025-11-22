import { message } from "antd";

const { BOOKINGS_ACTION_TYPES: bookingsAction } = require("../actions/bookingsAction");

const initState = { 
  bookingCreated: null,
  seatsBookedByTrip: null,
  ticketInfo: null,
  success: false,
  loading: false,
  error: null,
  message: null,
}

const bookingsReducer = (state = initState, action) => {
  switch (action.type) {
    case bookingsAction.CREATE_BOOKINGS_REQUEST:
      return {
        ...state,
        loading: true,
        error: null,
        success: false,
        message: null,
      };
    case bookingsAction.CREATE_BOOKINGS_SUCCESS:
      return {
        ...state,
        loading: false,
        bookingCreated: action.payload.data,
        message: action.payload.message,
        error: null,
        success: true,
      };
    case bookingsAction.CREATE_BOOKINGS_FAILURE:
      return {
        ...state,
        bookingCreated: null,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
        success: false,
      };
    case bookingsAction.FETCH_BOOKING_BY_CODE_REQUEST:
      return {
        ...state,
        loading: true,
        error: null,
        success: false,
        message: null,
      };
    case bookingsAction.FETCH_BOOKING_BY_CODE_SUCCESS:
      return {
        ...state,
        loading: false,
        bookingCreated: action.payload.data,
        message: action.payload.message,
        error: null,
        success: true,
      };
    case bookingsAction.FETCH_BOOKING_BY_CODE_FAILURE:
      return {
        ...state,
        bookingCreated: null,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
        success: false,
      };
    case bookingsAction.FETCH_SEATS_BOOKED_BY_TRIP_REQUEST:
      return {
        ...state,
        loading: true,
        error: null,
        success: false,
        message: null,
      };
    case bookingsAction.FETCH_SEATS_BOOKED_BY_TRIP_SUCCESS:
      return {
        ...state,
        loading: false,
        seatsBookedByTrip: action.payload.data,
        message: action.payload.message,
        error: null,
        success: true,
      };
    case bookingsAction.FETCH_SEATS_BOOKED_BY_TRIP_FAILURE:
      return {
        ...state,
        seatsBookedByTrip: null,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
        success: false,
      };
    case bookingsAction.FETCH_TICKET_BY_CODE_AND_EMAIL_REQUEST:
      return {
        ...state,
        loading: true,
        error: null,
        success: false,
        message: null,
      };
    case bookingsAction.FETCH_TICKET_BY_CODE_AND_EMAIL_SUCCESS:
      return {
        ...state,
        loading: false,
        ticketInfo: action.payload.data,
        message: action.payload.message,
        error: null,
        success: true,
      };
    case bookingsAction.FETCH_TICKET_BY_CODE_AND_EMAIL_FAILURE:
      return {
        ...state,
        ticketInfo: null,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
        success: false,
      };
    default:
      return state;
  }
}

export default bookingsReducer;