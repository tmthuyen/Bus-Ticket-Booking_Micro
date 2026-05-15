import { parseAxiosError, TOKEN_KEYS } from "../../api/api";
import { getMe, login } from "../../api/usersApi";

const USERS_ACTION_TYPES = {
  FETCH_LOGIN_REQUEST: "FETCH_LOGIN_REQUEST",
  FETCH_LOGIN_SUCCESS: "FETCH_LOGIN_SUCCESS",
  FETCH_LOGIN_FAILURE: "FETCH_LOGIN_FAILURE", 
  FETCH_ME_REQUEST: "FETCH_ME_REQUEST",
  FETCH_ME_SUCCESS: "FETCH_ME_SUCCESS",
  FETCH_ME_FAILURE: "FETCH_ME_FAILURE",
  FETCH_CHANGE_PASSWORD_REQUEST: "FETCH_CHANGE_PASSWORD_REQUEST",
  FETCH_CHANGE_PASSWORD_SUCCESS: "FETCH_CHANGE_PASSWORD_SUCCESS",
  FETCH_CHANGE_PASSWORD_FAILURE: "FETCH_CHANGE_PASSWORD_FAILURE",
  FETCH_UPDATE_PROFILE_REQUEST: "FETCH_UPDATE_PROFILE_REQUEST",
  FETCH_UPDATE_PROFILE_SUCCESS: "FETCH_UPDATE_PROFILE_SUCCESS",
  FETCH_UPDATE_PROFILE_FAILURE: "FETCH_UPDATE_PROFILE_FAILURE",
  FETCH_LOGOUT: "FETCH_LOGOUT",
}

export { USERS_ACTION_TYPES };

const loginUser = (username, password) => {
  return async (dispatch) => {
    dispatch({ type: USERS_ACTION_TYPES.FETCH_LOGIN_REQUEST });
    try {
      const { responseApi } = await login(username, password);
      // console.log("Login responseApi: ", responseApi);  
      localStorage.setItem(TOKEN_KEYS.BUS_ACCESS_TOKEN, responseApi.data.access_token);
      dispatch({ 
        type: USERS_ACTION_TYPES.FETCH_LOGIN_SUCCESS, 
        payload: { data: responseApi.data.access_token, message: "Đăng nhập thành công" } 
      });
    } catch (error) {
      console.error("loginUser error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({ 
        type: USERS_ACTION_TYPES.FETCH_LOGIN_FAILURE, 
        payload: { 
          error: parsedError.error || "Đăng nhập thất bại", 
          message: parsedError.message || "Đăng nhập thất bại" 
        } 
      });
    }
  };
};

const logoutUser = () => {
  return (dispatch) => {
    dispatch({ type: USERS_ACTION_TYPES.FETCH_LOGOUT });
  };
};

const fetchProfile = () => {
  return async (dispatch) => {
    dispatch({ type: USERS_ACTION_TYPES.FETCH_ME_REQUEST });
    try {
      const { responseApi } = await getMe();
      console.log("Fetch Profile responseApi: ", responseApi);  
      dispatch({ 
        type: USERS_ACTION_TYPES.FETCH_ME_SUCCESS, 
        payload: { data: responseApi.data, message: "Lấy thông tin người dùng thành công" } 
      });
    } catch (error) {
      console.error("fetchProfile error: ", error);
      const parsedError = parseAxiosError(error);
      dispatch({ 
        type: USERS_ACTION_TYPES.FETCH_ME_FAILURE, 
        payload: {
          error: parsedError.error || "Lấy thông tin người dùng thất bại", 
          message: parsedError.message || "Lấy thông tin người dùng thất bại" 
        } 
      });
    }
  };
};

export {
  loginUser,
  logoutUser,
  fetchProfile,
}