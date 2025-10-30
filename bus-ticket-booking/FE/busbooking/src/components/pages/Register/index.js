import { Card, Form, Input, Row, Button, Typography, Col, Progress, Space, Divider } from "antd";
import { useMemo, useState } from "react";
import { LockOutlined, MailOutlined, PhoneOutlined, UserOutlined } from "@ant-design/icons";
import "./Register.css";
import { register } from "../../../auth/auth";
import { parseAxiosError, setPydanticErrorsToForm } from "../../../api/api";
import { Link } from "react-router-dom";

function strength(pw) {
  let s = 0;
  if (!pw) return 0;
  if (pw.length >= 6) s += 20;
  if (pw.length >= 10) s += 20;
  if (/[A-Z]/.test(pw)) s += 20;
  if (/[0-9]/.test(pw)) s += 20;
  if (/[^A-Za-z0-9]/.test(pw)) s += 20;
  return Math.min(s, 100);
}

const Register = () => {
  const [formRegister] = Form.useForm();
  const [errMessage, setErrMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const password = Form.useWatch('password', formRegister);
  const score = useMemo(() => strength(password), [password]);
  

  const onFinish = async (values) => {
    console.log("Success:", values);
    // Call API to register user
    const { full_name, email, phone, password, confirm_password } = values;
    // Validate email format
    if (!isValidInput(email, full_name, phone, password, confirm_password)) {
      return;
    }

    // call API register
    setSubmitting(true);
    try {
      const res = await register(full_name, email, phone, password, confirm_password);
      console.log("Register user:", res.data);

      // backend kiểu successResponse => kiểm tra success/message
      if (res?.success === false) {
        // lỗi dạng { success:false, message, data? }
        // message.error(res?.message || "Đăng ký thất bại");
        setErrMessage(res?.message || "Đăng ký thất bại");
        return;
      }

      // message.success("Đăng ký thành công!");
      setErrMessage('Đăng ký thành công! Vui lòng đăng nhập.');
      formRegister.resetFields();
    } catch (error) {
      console.error("Failed to register user:", error.response.data);
      const { status, data, message: msg } = parseAxiosError(error);

      if (status === 422 && Array.isArray(data?.detail)) {
        // pydantic validation error
        setPydanticErrorsToForm(formRegister, data.detail);
        setErrMessage('Vui lòng kiểm tra lại thông tin đã nhập.');
        return;
      }

      // Nếu backend trả {success:false,message:"..."} với 400/409...
      if (data?.message) {
        setErrMessage(data.message); 
        return;
      }

      setErrMessage(msg);
    } finally{
      setSubmitting(false);
    }
  }

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  const onInputChange = (val) => {
    // setErr('');
  };

  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const isValidPassword = (password) => {
    // Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
  }

  const isValidInput = (email, full_name, phone, password, confirm_password) => {
    if (!full_name || full_name.trim() === '') {
      formRegister.setFields([{ name: 'full_name', errors: ['Họ và tên không được để trống. Vui lòng nhập lại.'] }]);
      formRegister.getFieldInstance('full_name').focus();
      return false;
    }
    
    if (!isValidEmail(email)) { 
      formRegister.setFields([{ name: 'email', errors: ['Email không hợp lệ. Vui lòng nhập lại.'] }]);
      formRegister.getFieldInstance('email').focus();
      return false;
    }

    if (phone && isNaN(phone)) { 
      formRegister.setFields([{ name: 'phone', errors: ['Số điện thoại không hợp lệ. Vui lòng nhập lại.'] }]);
      formRegister.getFieldInstance('phone').focus();
      return false;
    }

    // Validate password strength
    if (!isValidPassword(password)) { 
      setErrMessage('Mật khẩu bao gồm ít nhất 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.');
      formRegister.setFields([{ name: 'password', errors: ['Mật khẩu không đủ mạnh. Vui lòng nhập lại.'] }]);
      formRegister.getFieldInstance('password').focus();
      return false;
    }

    if (password !== confirm_password) {
      console.log("Mật khẩu xác nhận không khớp");
      // setErrMessage('Mật khẩu xác nhận không khớp');
      formRegister.setFields([{ name: 'confirm_password', errors: ['Mật khẩu xác nhận không khớp. Vui lòng nhập lại.'] }]);
      formRegister.getFieldInstance('confirm_password').focus();
      return false;
    } 
    return true;
  }

  return (
    <>
      <Row justify="center" align="center" style={{marginTop: '20px' }}>
        <Col span={24} style={{ display: 'flex', justifyContent: 'center' }}>
          <Card  
          className="cardRegister"
          >
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
                Tạo tài khoản
              </Typography.Title>
              <Typography.Text >
                Điền thông tin bên dưới để bắt đầu.
              </Typography.Text>
            </Space>

            <Divider style={{ margin: "16px 0 24px", border: "1px solid " }} />

            <Form
              layout={'vertical'}
              form={formRegister}
              initialValues={{ remember: true }}
              style={{ maxWidth: 360 }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              onValuesChange={onInputChange}
              autoComplete="off"
            >
              <Form.Item label="Họ và tên" name="full_name" rules={[{ required: true, message: 'Vui lòng nhập họ và tên' }]}>
                <Input 
                  placeholder="Nhập  họ và tên" 
                  prefix={<UserOutlined />}             
                />
              </Form.Item>
              <Form.Item label="Địa chỉ email" name="email" rules={[{ required: true, message: 'Vui lòng nhập email' }]}>
                <Input placeholder="Nhập email" prefix={<MailOutlined />} />
              </Form.Item>

              <Form.Item label="Số điện thoại" name="phone" >
                <Input placeholder="Nhập số điện thoại" prefix={<PhoneOutlined />} />
              </Form.Item>

              <Form.Item label="Mật khẩu" name="password" rules={[{ required: true, message: 'Vui lòng nhập mật khẩu' }]}>
                <Input.Password placeholder="********" prefix={<LockOutlined />} />
              </Form.Item>

              <div style={{ marginTop: -8, marginBottom: 16 }}>
                <Progress
                  percent={score}
                  showInfo={false}
                  strokeColor={score < 40 ? "#f43f5e" : score < 80 ? "#f59e0b" : "#22c55e"}
                  trailColor="#e5e7eb"
                />
                <Typography.Text style={{ color: "black", fontSize: 12 }}>
                  Độ mạnh mật khẩu: {score < 40 ? "Yếu" : score < 80 ? "Khá" : "Mạnh"}
                </Typography.Text>
              </div>

              <Form.Item label="Mật khẩu xác nhận" name="confirm_password" rules={[{ required: true, message: 'Vui lòng xác nhận mật khẩu' }]}>
                <Input.Password placeholder="********" prefix={<LockOutlined />} />
              </Form.Item>

              {/* Error message */}
              <Typography.Text type="danger">
                {errMessage}
              </Typography.Text>
              

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={ submitting } style={{ width: '100%' }}>
                  Đăng ký
                </Button>
              </Form.Item>
 
            </Form>
            <Typography.Text>
              Đã có tài khoản? <Link to="/login">Đăng nhập</Link>
            </Typography.Text>
          </Card>
        </Col>
      </Row>
    </>
  )
};

export default Register;