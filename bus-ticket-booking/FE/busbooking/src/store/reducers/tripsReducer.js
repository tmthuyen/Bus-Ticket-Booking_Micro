const { TRIPS_ACTION_TYPES: tripsAction } = require("../actions/tripsAction");

const intitState = {
  routes: [],
  tripById: null,
  tripsByRoute: [], // trips and route info 
  seatsByTrip: [], // seats and trip info
  loading: false,
  error: null,
  message: null,
}

const tripsReducer = (state = intitState, action) => {
  switch (action.type) {
    case tripsAction.FETCH_ROUTES_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case tripsAction.FETCH_ROUTES_SUCCESS:
      return {
        ...state,
        loading: false,
        routes: action.payload.data,
        message: action.payload.message,
      };
    case tripsAction.FETCH_ROUTES_FAILURE:
      return {
        ...state,
        routes: [],
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
      };
    case tripsAction.FETCH_TRIP_BY_ID_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case tripsAction.FETCH_TRIP_BY_ID_SUCCESS:
      return {
        ...state,
        loading: false, 
        tripById: action.payload.data,
        message: action.payload.message,
      };
    case tripsAction.FETCH_TRIP_BY_ID_FAILURE:
      return {
        ...state,
        loading: false,
        tripById: null,
        error: action.payload.error,
        message: action.payload.message,
      };
    case tripsAction.FETCH_TRIPS_BY_ROUTE_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case tripsAction.FETCH_TRIPS_BY_ROUTE_SUCCESS:
      return {
        ...state,
        loading: false,
        tripsByRoute: action.payload.data,
        message: action.payload.message,
      };
    case tripsAction.FETCH_TRIPS_BY_ROUTE_FAILURE:
      return {
        ...state,
        loading: false,
        tripsByRoute: [],
        error: action.payload.error,
        message: action.payload.message,
      };
    case tripsAction.FETCH_SEATS_BY_TRIP_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case tripsAction.FETCH_SEATS_BY_TRIP_SUCCESS:
      return {
        ...state,
        loading: false,
        seatsByTrip: action.payload.data,
        message: action.payload.message,
      };
    case tripsAction.FETCH_SEATS_BY_TRIP_FAILURE:
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