import { message } from "antd";
import { USERS_ACTION_TYPES } from "../actions/usersAction";

const initialState = {
  user: null,
  token: null,
  loading: false,
  error: null,
  message: null,
};

const usersReducer = (state = initialState, action) => {
  switch (action.type) {
    case USERS_ACTION_TYPES.FETCH_LOGIN_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case USERS_ACTION_TYPES.FETCH_LOGIN_SUCCESS:
      return {  
        ...state,
        loading: false,
        token: action.payload.data
      };
    case USERS_ACTION_TYPES.FETCH_LOGIN_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
      };
    case USERS_ACTION_TYPES.FETCH_ME_REQUEST:
      return {
        ...state,
        loading: true,
      };
    case USERS_ACTION_TYPES.FETCH_ME_SUCCESS:
      return {
        ...state,
        loading: false,
        user: action.payload.data,
        message: action.payload.message,
      };
    case USERS_ACTION_TYPES.FETCH_ME_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload.error,
        message: action.payload.message,
      };
    case USERS_ACTION_TYPES.FETCH_LOGOUT:
      return {
        ...initialState,
      };
    default:
      return state
  }
};

export default usersReducer;
