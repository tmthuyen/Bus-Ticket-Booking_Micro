import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = () => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    // ❌ Không có token → quay về login
    return <Navigate to="/login" replace />;
  }

  // ✅ Có token → cho vào các route con
  return <Outlet />;
};

export default ProtectedRoute;