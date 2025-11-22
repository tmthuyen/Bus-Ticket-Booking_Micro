const { BOOKINGS_ACTION_TYPES: bookingsAction } = require("../actions/bookingsAction");

const initState = {
  booking: null,
  seatsBookedByTrip: null,
  ticketInfo: null,
  loading: false,
  error: null,
  message: null,
}

const tripsReducer = (state = initState, action) => {
  switch (action.type) {
    case bookingsAction.FETCH_ROUTES_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case bookingsAction.FETCH_ROUTES_SUCCESS:
      return {
        ...state,
        loading: false,
        routes: action.payload.data,
        message: action.payload.message,
      };
    case bookingsAction.FETCH_ROUTES_FAILURE:
      return {
        ...state,
        routes: [],
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
      };
    case bookingsAction.FETCH_TRIPS_BY_ROUTE_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case bookingsAction.FETCH_TRIPS_BY_ROUTE_SUCCESS:
      return {
        ...state,
        loading: false,
        tripsByRoute: action.payload.data,
        message: action.payload.message,
      };
    case bookingsAction.FETCH_TRIPS_BY_ROUTE_FAILURE:
      return {
        ...state,
        loading: false,
        tripsByRoute: [],
        error: action.payload.error,
        message: action.payload.message,
      };
    case bookingsAction.FETCH_SEATS_BY_TRIP_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case bookingsAction.FETCH_SEATS_BY_TRIP_SUCCESS:
      return {
        ...state,
        loading: false,
        seatsByTrip: action.payload.data,
        message: action.payload.message,
      };
    case bookingsAction.FETCH_SEATS_BY_TRIP_FAILURE:
      return {
        ...state,
        seatsByTrip: null,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
      };
    default:
      return state;
  }
}

export default tripsReducer;