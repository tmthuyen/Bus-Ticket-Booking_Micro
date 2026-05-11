import { UserOutlined } from '@ant-design/icons';
import { MailOutlined, PhoneOutlined } from '@mui/icons-material';
import { Typography } from '@mui/material';
import { Form, Input } from 'antd'; 
import { useEffect } from 'react';

const CustomerBookingForm = ({ 
  setFullName,
  setEmail,
  setPhone,
}) => { 
  const [formCustomer] = Form.useForm(); 

  const onFinishFormCustomer = (values) => {
    const { full_name, email, phone } = values;

    // console.log('Finish form customer booking:', values);
    setFullName(full_name);
    setEmail(email);
    setPhone(phone);

    const customer_info = {
      full_name,
      email,
      phone,
    };
    window.localStorage.setItem('customer_info', JSON.stringify(customer_info));
  };
  const onFinishFailedFormCustomer = (errorInfo) => {
    console.log('Failed to submit form customer booking:', errorInfo);
  };
  const onInputChangeFormCustomer = (changedValues, allValues) => {
    console.log(
      'Input change form customer booking:',
      changedValues,
      allValues
    );
    const { full_name, email, phone } = allValues;
    setFullName(full_name);
    setEmail(email);
    setPhone(phone);
 
  };

  const customer_info_storage = window.localStorage.getItem('customer_info');
  
  const autoFillCustomerInfo = () => {
    if (customer_info_storage) {
      try { 
        const customer_info = JSON.parse(customer_info_storage);
        formCustomer.setFieldsValue({
          full_name: customer_info.full_name || '',
          email: customer_info.email || '',
          phone: customer_info.phone || '',
        });
        setFullName(customer_info.full_name || '');
        setEmail(customer_info.email || '');
        setPhone(customer_info.phone || '');
      } catch (error) {
        console.error('Error parsing customer info from localStorage:', error);
      }
    }
  };

  useEffect(() => {
    autoFillCustomerInfo();
  }, []);

  return (
    <>
        <Typography variant="h5">Thông tin khách hàng</Typography>
        <Form
          layout="vertical"
          form={formCustomer}
          onFinish={onFinishFormCustomer}
          onFinishFailed={onFinishFailedFormCustomer}
          onValuesChange={onInputChangeFormCustomer}
          autoComplete="off"
          // initialValues={{
          //   full_name: 'fullName',
          //   email: email,
          //   phone: phone,
          // }}
        >
          <Form.Item
            label="Họ và tên" 
            name="full_name"
            rules={[{ required: true, message: 'Vui lòng nhập họ và tên' }]}
          >
            <Input 
              allowClear
              placeholder="Nhập họ và tên"
              prefix={<UserOutlined />}
            />
          </Form.Item>
          <Form.Item
            label="Địa chỉ email"
            name="email" 
            rules={[{ required: true, message: 'Vui lòng nhập email' }]}
          >
            <Input
              allowClear
              placeholder="Nhập email"
              prefix={<MailOutlined />}
            />
          </Form.Item>

          <Form.Item 
            label="Số điện thoại" 
            name="phone"
            rules={[{ required: true, message: 'Vui lòng nhập số điện thoại' }]}
          >
            <Input
              allowClear
              placeholder="Nhập số điện thoại"
              prefix={<PhoneOutlined />}
            />
          </Form.Item>
        </Form>
    </>
  );
};

export default CustomerBookingForm;
