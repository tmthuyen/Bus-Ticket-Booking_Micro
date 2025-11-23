import { Outlet } from 'react-router-dom';
import './LayoutDefault.css'; 
import CustomerHeader from '../../partials/CustomerHeader';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import { fetchRoutes } from '../../../store/actions/tripsAction';
import { fetchProfile } from '../../../store/actions/usersAction';
 
function LayoutDefault() { 
  const dispatch = useDispatch(); 

  useEffect(() => {
    dispatch(fetchRoutes());
  }, [dispatch]);
 
  
  const { user: userFromStore } = useSelector((state) => state.users);

  useEffect(() => {
    const fetchUserProfile = async () => {
      if (userFromStore == null) {
        // dispatch action to fetch user profile
        await dispatch(fetchProfile());
      }
    };
    fetchUserProfile(); 
  }, [dispatch, userFromStore]);

  return (
    <div className="layout-default">
      <header className="layout-default__header">
        <CustomerHeader user={userFromStore} />
      </header>

      <main className="layout-default__main">
        <Outlet />
      </main>

      <footer className="layout-default__footer">Tran Minh Thuyen</footer>
    </div>
  );
}

export default LayoutDefault;
