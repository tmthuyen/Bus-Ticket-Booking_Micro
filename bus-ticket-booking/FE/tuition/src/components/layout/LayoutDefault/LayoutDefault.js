import { Link, Outlet, useNavigate } from "react-router-dom";
import "./LayoutDefault.scss";
import { useCallback, useEffect, useMemo, useState } from "react";
import { get } from "../../../utils/request";
import Profile from "../../pages/Profile/index";
import { Dropdown, Flex, Space, Typography, Spin } from "antd";
import { DownOutlined, LogoutOutlined, UserOutlined } from "@ant-design/icons";

const { Text } = Typography;

function LayoutDefault() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [openProfile, setOpenProfile] = useState(false);
  const navigate = useNavigate();

  // Hàm fetch/memo để truyền xuống con
  const refreshProfile = useCallback(
    async (signal) => {
      try {
        const res = await get("/auth/users/me/", { signal });
        // tuỳ cấu trúc backend; giả định { status: 'ok', data: {...} }
        if (res?.status === "ok" && res?.data) {
          setProfile(res.data);
        } else {
          navigate("/login", { replace: true });
        }
      } catch (err) {
        if (err?.name !== "AbortError") {
          navigate("/login", { replace: true });
        }
      }
    },
    [navigate]
  );

  useEffect(() => {
    const ac = new AbortController();
    (async () => {
      setLoading(true);
      await refreshProfile(ac.signal);
      setLoading(false);
    })();
    return () => ac.abort();
  }, [refreshProfile]);

  const items = useMemo(
    () => [
      {
        key: "1",
        icon: <UserOutlined />,
        label: "Hồ sơ",
        onClick: () => setOpenProfile(true),
      },
      {
        key: "2",
        icon: <LogoutOutlined />,
        label: <Link to="logout">Đăng xuất</Link>,
      },
    ],
    []
  );

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", padding: 24 }}>
        <Spin tip="Đang tải thông tin tài khoản..." />
      </div>
    );
  }

  if (!profile) return null; // đã navigate sang /login ở trên

  return (
    <div className="layout-default">
      <header className="layout-default__header">
        <div className="layout-default__logo">
          <Link to="/">
            <Flex align="center" justify="center">
              <img
                src={"/tdtu_logo_rmbg.png"}
                style={{ height: 60, width: 60, objectFit: "cover" }}
                alt="Logo"
              />
              <Text style={{ marginLeft: 8 }}>Cổng thanh toán học phí TDTU</Text>
            </Flex>
          </Link>
        </div>

        <div className="layout-default__account">
          <Dropdown menu={{ items }} placement="bottomRight" arrow>
            <Space style={{ cursor: "pointer" }}>
              <Text strong>Hello {profile.full_name}</Text>
              <DownOutlined />
            </Space>
          </Dropdown>
        </div>
      </header>

      <main className="layout-default__main">
        {/* Truyền profile + refreshProfile cho các màn con */}
        <Outlet context={{ profile, refreshProfile }} />

        {/* Nếu bạn có modal Profile, mở ở đây */}
        <Profile open={openProfile} onClose={() => setOpenProfile(false)} profile={profile} />
      </main>

      <footer className="layout-default__footer">Tran Minh Thuyen</footer>
    </div>
  );
}

export default LayoutDefault;
