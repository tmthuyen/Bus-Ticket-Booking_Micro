import {
  Button,
  Divider,
  Flex,
  Form,
  Input,
  notification,
  Space,
  Spin,
  Typography,
} from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import './Login.scss';
import { useState } from 'react'; 
import { useDispatch, useSelector } from 'react-redux';
import { fetchProfile, loginUser } from '../../../store/actions/usersAction';

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
function Login() {
  const [api, contextHolder] = notification.useNotification();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const {
    user,
    token,
    loading: loadingUser, 
    message: messageUser,
  } = useSelector((state) => state.users);

  const [form] = Form.useForm();
  const [err, setErr] = useState('');
  const [loading, setLoading] = useState(false);

  const onInputChange = (val) => {
    setErr('');
  };
  const onFinish = async (values) => {
    const { username, password } = values;
    // 0373436164 - Admin25@
    setLoading(loadingUser);

    try {
      //   const { responseApi: loginResponse } = await login(username, password);
      dispatch(loginUser(username, password));

      console.log('Login successful:', token);

      await dispatch(fetchProfile());
      console.log('Fetched profile:', user);

      api.success({
        message: messageUser || 'Đăng nhập thành công' ,
        description: `Chào mừng ${user?.full_name} đến với hệ thống đặt vé xe buýt!`,
      });

      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (error) {
      console.error('Login failed:', error);
      setErr('Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.');
    } finally {
      setLoading(loadingUser);
    }
  };

  return (
    <Flex align="center" justify="center" vertical>
      {contextHolder}
      <div className="login">
        <Space
          direction="vertical"
          style={{ width: '100%' }}
          size={8}
          align="center"
        >
          <div
            style={{
              width: 'auto',
              height: 56,
              borderRadius: 16,
              padding: '0 24px',
              background: 'linear-gradient(135deg,#22d3ee,#6366f1)',
              display: 'grid',
              placeItems: 'center',
              color: '#fff',
              fontWeight: 700,
              fontSize: 20,
              boxShadow: '0 6px 18px rgba(99,102,241,.35)',
            }}
          >
            Bus Booking System
          </div>
          <Typography.Title level={5}>Đăng nhập tài khoản</Typography.Title>
        </Space>

        <Divider style={{ margin: '8px 0' }} />
        <Form
          layout={'vertical'}
          form={form}
          initialValues={{ remember: true }}
          style={{ maxWidth: 360 }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          onValuesChange={onInputChange}
          autoComplete="off"
        >
          <Form.Item
            label="Tên đăng nhập"
            name="username"
            rules={[
              {
                required: true,
                message: 'Please input your username!',
              },
            ]}
          >
            <Input placeholder="Nhập tên đăng nhập" prefix={<UserOutlined />} />
          </Form.Item>

          <Form.Item
            label="Mật khẩu"
            name="password"
            rules={[
              {
                required: true,
                message: 'Please input your password!',
              },
            ]}
          >
            <Input.Password
              placeholder="Nhập mật khẩu"
              prefix={<LockOutlined />}
            />
          </Form.Item>

          <Typography.Text type="danger">{err}</Typography.Text>
          <Form.Item label={null}>
            <Button
              type="primary"
              className="login__submit"
              htmlType="submit"
              loading={loading}
              block
            >
              Đăng nhập
            </Button>
          </Form.Item>
        </Form>
        <Typography.Text>
          Chưa có tài khoản? <Link to="/register">Đăng ký</Link>
        </Typography.Text>
      </div>
      <Spin
        size="large"
        fullscreen
        delay={100}
        spinning={loading}
        tip={'Dang xac thuc'}
      />
    </Flex>
  );
}
export default Login;
