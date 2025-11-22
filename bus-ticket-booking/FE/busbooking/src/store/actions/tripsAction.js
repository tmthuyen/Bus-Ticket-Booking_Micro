import { parseAxiosError } from "../../api/api";
import { getRoutes, getTripsByOriginAndDestinationAndFromDate
  , getSeatsByTripId,
  getTripById
 } from "../../api/tripsApi";

const TRIPS_ACTION_TYPES = {
  FETCH_ROUTES_REQUEST: "FETCH_ROUTES_REQUEST",
  FETCH_ROUTES_SUCCESS: "FETCH_ROUTES_SUCCESS",
  FETCH_ROUTES_FAILURE: "FETCH_ROUTES_FAILURE",
  FETCH_TRIP_BY_ID_REQUEST: "FETCH_TRIP_BY_ID_REQUEST",
  FETCH_TRIP_BY_ID_SUCCESS: "FETCH_TRIP_BY_ID_SUCCESS",
  FETCH_TRIP_BY_ID_FAILURE: "FETCH_TRIP_BY_ID_FAILURE",
  FETCH_TRIPS_BY_ROUTE_REQUEST: "FETCH_TRIPS_BY_ROUTE_REQUEST",
  FETCH_TRIPS_BY_ROUTE_SUCCESS: "FETCH_TRIPS_BY_ROUTE_SUCCESS",
  FETCH_TRIPS_BY_ROUTE_FAILURE: "FETCH_TRIPS_BY_ROUTE_FAILURE",
  FETCH_SEATS_BY_TRIP_REQUEST: "FETCH_SEATS_BY_TRIP_REQUEST",
  FETCH_SEATS_BY_TRIP_SUCCESS: "FETCH_SEATS_BY_TRIP_SUCCESS",
  FETCH_SEATS_BY_TRIP_FAILURE: "FETCH_SEATS_BY_TRIP_FAILURE",
}

export { TRIPS_ACTION_TYPES };

const fetchRoutes = () => {
  return async (dispatch) => {
    dispatch({ type: TRIPS_ACTION_TYPES.FETCH_ROUTES_REQUEST });
    try {
      const { responseApi } = await getRoutes(); 
      console.log("Fetch Routes responseApi: ", responseApi);
      dispatch({ 
        type: TRIPS_ACTION_TYPES.FETCH_ROUTES_SUCCESS, 
        payload: { data: responseApi.data, message: "Lấy danh sách tuyến xe thành công" } 
      });
    } catch (error) {
      console.error("fetchRoutes error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({ 
        type: TRIPS_ACTION_TYPES.FETCH_ROUTES_FAILURE, 
        payload: { 
          error: parsedError.message || "Lấy danh sách tuyến xe thất bại", 
          message: parsedError.message || "Lấy danh sách tuyến xe thất bại" 
        } 
      });
    }
  }
};

const fetchTripById = (trip_id) => {
  return async (dispatch) => {
    dispatch({ type: TRIPS_ACTION_TYPES.FETCH_TRIP_BY_ID_REQUEST });
    try {
      const { responseApi } = await getTripById(trip_id);
      console.log("Fetch Trip By ID responseApi: ", responseApi);
      dispatch({
        type: TRIPS_ACTION_TYPES.FETCH_TRIP_BY_ID_SUCCESS,
        payload: { data: responseApi.data, message: "Lấy thông tin chuyến xe thành công" }
      });
    } catch (error) {
      console.error("fetchTripById error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({
        type: TRIPS_ACTION_TYPES.FETCH_TRIP_BY_ID_FAILURE,
        payload: {
          error: parsedError.message || "Lấy thông tin chuyến xe thất bại",
          message: parsedError.message || "Lấy thông tin chuyến xe thất bại"
        }
      });
    }
  };
}

const fetchTripsByRoute = (origin_code, destination_code, from_date) => {
  return async (dispatch) => {
    dispatch({ type: TRIPS_ACTION_TYPES.FETCH_TRIPS_BY_ROUTE_REQUEST });
    try {
      const { responseApi } = await getTripsByOriginAndDestinationAndFromDate(origin_code, destination_code, from_date);
      // console.log("Fetch Trips By Route responseApi: ", responseApi);
      dispatch({ 
        type: TRIPS_ACTION_TYPES.FETCH_TRIPS_BY_ROUTE_SUCCESS, 
        payload: { data: responseApi.data, message: "Lấy danh sách chuyến xe thành công" } 
      });
    } catch (error) {
      console.error("fetchTripsByRoute error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({ 
        type: TRIPS_ACTION_TYPES.FETCH_TRIPS_BY_ROUTE_FAILURE, 
        payload: { 
          error: parsedError.message || "Lấy danh sách chuyến xe thất bại", 
          message: parsedError.message || "Lấy danh sách chuyến xe thất bại" 
        } 
      });
    }
  }
};

const fetchSeatsByTrip = (trip_id) => {
  return async (dispatch) => {
    dispatch({ type: TRIPS_ACTION_TYPES.FETCH_SEATS_BY_TRIP_REQUEST });
    try {
      const { responseApi } = await getSeatsByTripId(trip_id);
      console.log("Fetch Seats By Trip responseApi: ", responseApi);
      dispatch({ 
        type: TRIPS_ACTION_TYPES.FETCH_SEATS_BY_TRIP_SUCCESS, 
        payload: { data: responseApi.data, message: "Lấy danh sách ghế thành công" } 
      });
    } catch (error) {
      console.error("fetchSeatsByTrip error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({ 
        type: TRIPS_ACTION_TYPES.FETCH_SEATS_BY_TRIP_FAILURE, 
        payload: { 
          error: parsedError.message || "Lấy danh sách ghế thất bại", 
          message: parsedError.message || "Lấy danh sách ghế thất bại" 
        } 
      });
    }
  };
};

export {
  fetchRoutes,
  fetchTripById,
  fetchTripsByRoute,
  fetchSeatsByTrip,
};