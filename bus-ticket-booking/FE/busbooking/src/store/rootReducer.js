import { combineReducers } from "redux";
import tripsReducer from "./reducers/tripsReducer"; 
import usersReducer from "./reducers/usersReducer";

const rootReducer = combineReducers({
  trips: tripsReducer,
  users: usersReducer,
});

export default rootReducer;