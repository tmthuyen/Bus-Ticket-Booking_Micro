import LayoutDefault from "../components/layout/LayoutDefault/LayoutDefault";
import Login from "../components/pages/Login";
import Logout from "../components/pages/Logout";
import ErrorPage from "../components/pages/ErrorPage";
import Home from "../components/pages/Home/Home"; 
import ProtectedRoute from "./ProtectedRoute";
import PaymentSuccess from "../components/pages/Payment/PaymentSuccess";

export const routes = [
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/logout",
    element: <Logout />,
  },
  {
    path: "/",
    element: <ProtectedRoute />,   // 🔒 Bọc lại
    children: [
      {
        path: "/",
        element: <LayoutDefault />, // layout chỉ hiển thị khi có token
        children: [
          {
            path: "/",
            element: <Home />,
          },
          {
            path: "/payment-success/:payment_id",
            element: <PaymentSuccess />,
          }
        ],
      },
      {
        path: "/test",
        element: <p>Hello Test Route</p>
      }
    ],
  },
  {
    path: "*",
    element: <ErrorPage status={404} message={"Page Not Found"} />,
  },
];
