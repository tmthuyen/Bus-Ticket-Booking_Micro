import { Button, Divider, Flex, Form, Input, notification, Space, Spin, Typography } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import './Login.scss';
import { API_DOMAIN } from '../../../constants';
import { useState } from 'react';
import { getMe, login } from '../../../auth/auth';

const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};
function Login() {
    const [api, contextHolder] = notification.useNotification();
    
    const [form] = Form.useForm();
    const [err, setErr] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

    const onInputChange = (val) => {
        setErr('');
    };
    const onFinish = async (values) => {
        
        const { username, password } = values;
        const body = new URLSearchParams();

        const token = await login(username, password);
        console.log('Access Token:', token);
        const me = await getMe();
        console.log('Logged in user:', me);
        // mo code comment khi chay
        body.append('username', username);
        body.append('password', password);
        // body.append('device_id', 'web');
        // backdoor
        // body.append("username", "52300070");
        // body.append("password", "123456");
        setLoading(true);
 
        try {
            const res = await fetch(API_DOMAIN + '/users/auth/login', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body,
            });

            await sleep(500);
            // setLoading(false)

            setTimeout(() => setLoading(false), 1000);

            const rs = await res.json();
            console.log('rs', rs);

            if (res.status === 200) {
                // const rs = await res.json();
                // console.log(rs);
                if (localStorage.getItem('access_token'))
                    localStorage.removeItem('access_token');
                localStorage.setItem('access_token', rs.data.access_token);
                // chuyển hướng sau khi login thành công
                // console.log(rs);
                
                api.success({
                    message: 'Đăng nhập thành công',
                    description: `Chào mừng ${username} đã quay trở lại!`,
                    duration: 5,
                });

                const me = await fetch(API_DOMAIN + '/users/auth/me', {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        // 'Content-Type': 'application/x-www-form-urlencoded',
                        Authorization: `Bearer ${rs.data.access_token}`,
                    },
                });
                const meRs = await me.json();
                api.info({
                    message: 'Thông tin người dùng',
                    description: `Bạn đang đăng nhập với vai trò: ${meRs.data.full_name} - ${meRs.data.role}`,
                    duration: 5,
                });

                // navigate('/');
            } else if (res.status === 401) {
                
                setErr(rs.message ? rs.message : rs.detail);
                // console.log(rs);
            } else {
                setErr(rs.message ? rs.message : 'Đã có lỗi xảy ra, vui lòng thử lại.');
            }
        } catch (error) {
            setErr(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Flex align="center" justify="center" vertical>
         {contextHolder}
            <div className="login"> 
                <Space direction="vertical" style={{ width: "100%" }} size={8} align="center">
                    <div style={{
                        width: 'auto', height: 56, borderRadius: 16, padding: '0 24px',
                        background: "linear-gradient(135deg,#22d3ee,#6366f1)",
                        display: "grid", placeItems: "center", color: "#fff",
                        fontWeight: 700, fontSize: 20, boxShadow: "0 6px 18px rgba(99,102,241,.35)"
                    }}>
                        Bus Booking System
                    </div>
                    <Typography.Title level={5}>
                        Đăng nhập tài khoản
                    </Typography.Title> 
                </Space>

                <Divider style={{ margin: "8px 0" }} />
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
                        <Input
                            placeholder="Nhập tên đăng nhập"
                            prefix={
                                <UserOutlined />
                            }
                        />
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
                            prefix={
                                <LockOutlined />
                            }
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
