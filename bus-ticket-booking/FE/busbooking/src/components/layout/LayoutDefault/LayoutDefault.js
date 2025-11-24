import { Outlet } from 'react-router-dom';
import './LayoutDefault.css';
import CustomerHeader from '../../partials/CustomerHeader';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import { fetchRoutes } from '../../../store/actions/tripsAction';
import { fetchProfile } from '../../../store/actions/usersAction';
import { useGlobalLoading } from '../../../context/LoadingContext';
import { LoadingOutlined } from '@ant-design/icons';
import { Spin } from 'antd';

const antIconLoading = <LoadingOutlined style={{ fontSize: 48 }} spin />;
function LayoutDefault() {
  const dispatch = useDispatch();
  // spinning global loading
  const { spinning, setSpinning } = useGlobalLoading();

  useEffect(() => {
    dispatch(fetchRoutes());
  }, [dispatch]);

  const { user: userFromStore } = useSelector((state) => state.users);

  useEffect(() => {
    setSpinning(true);
    const fetchUserProfile = async () => {
      if (userFromStore == null) {
        // dispatch action to fetch user profile
        await dispatch(fetchProfile());
      }
      setSpinning(false);
    };
    fetchUserProfile();
  }, [dispatch, userFromStore, setSpinning]);

  return (
    <>
      <div className="layout-default">
        <Spin
          spinning={spinning}
          indicator={antIconLoading}
          fullscreen={true}
        />
        <header className="layout-default__header">
          <CustomerHeader user={userFromStore} />
        </header>

        <main className="layout-default__main">
          <Outlet />
        </main>

        <footer className="layout-default__footer">Tran Minh Thuyen</footer>
        {/* </Spin> */}
      </div>
    </>
  );
}

export default LayoutDefault;
