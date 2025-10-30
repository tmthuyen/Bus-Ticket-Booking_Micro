import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    // Xóa thông tin đăng nhập
    localStorage.removeItem("access_token");
    // sessionStorage.removeItem("user");

    // Nếu backend có API logout, gọi thêm:
    // await fetch("/api/logout", { method: "POST", credentials: "include" });

    // Chuyển hướng
    navigate("/login");
  }, [navigate]);

  return null;  
}


export default Logout;
