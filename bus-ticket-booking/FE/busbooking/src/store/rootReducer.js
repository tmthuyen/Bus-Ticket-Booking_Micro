import { combineReducers } from "redux";
import tripsReducer from "./reducers/tripsReducer"; 
import usersReducer from "./reducers/usersReducer";
import bookingsReducer from "./reducers/bookingsReducer";

const rootReducer = combineReducers({
  trips: tripsReducer,
  users: usersReducer,
  bookings: bookingsReducer,
});

export default rootReducer;