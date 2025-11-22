import { MailOutlined, SearchOutlined } from '@ant-design/icons';
import { Container, Grid, Typography } from '@mui/material';
import { Button, Form, Input, message } from 'antd';
import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {  fetchTicketByCodeAndEmailAction } from '../../../store/actions/bookingsAction';

const LookupTicketPage = () => {
  const [formLookupTicket] = Form.useForm();
  const dispatch = useDispatch();
  const [messageAnt, contextHolder] = message.useMessage();
  
  // store state
  const { ticketInfo, loading: loadingLookup, success, message: messageLookup } = useSelector((state) => state.bookings);

  const [bookingCode, setBookingCode] = useState('');
  const [email, setEmail] = useState('');

  const onFinish = async (values) => {
    const { booking_code, email } = values;
    console.log('Finish form lookup ticket:', values);
    setBookingCode(booking_code);
    setEmail(email);

    // dispatch action to lookup ticket
    // dispatch(fetchBookingByCodeAction(booking_code));
    const searchTicket = async () => {
      await dispatch(fetchTicketByCodeAndEmailAction(booking_code, email));
    };
    await searchTicket();

    if (!ticketInfo){ 
      messageAnt.error(messageLookup);
      return;
    }

    messageAnt.success('Tra cứu vé thành công!');
    console.log('Lookup ticket message:', messageLookup);
    console.log('Lookup ticket:', ticketInfo);
    
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed to submit form customer booking:', errorInfo);
  };
  const onInputChange = (changedValues, allValues) => {
    setBookingCode(allValues.booking_code);
    setEmail(allValues.email);
    console.log('Input change form lookup ticket:', changedValues, allValues);
  };

  return (
    <>
      {contextHolder}
      <Container maxWidth="lg" sx={{ minHeight: '80vh', paddingY: 4 }}>
        <Typography variant="h5" fontWeight={600} style={{ textAlign: 'center' }}>Tra cứu vé</Typography>
        <Grid
          container
          spacing={2}
          sx={{ marginTop: 2, justifyContent: 'center' }}
        >
          <Grid size={{ xs: 12, md: 6 }}>
            <Form
              layout="vertical"
              form={formLookupTicket}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              onValuesChange={onInputChange}
              autoComplete="off"
              // initialValues={{
              //   full_name: 'fullName',
              //   email: email,
              //   phone: phone,
              // }}
            >
              <Form.Item
                label="Mã đặt vé"
                name="booking_code"
                rules={[{ required: true, message: 'Vui lòng nhập mã đặt vé' }]}
              >
                <Input
                  allowClear
                  placeholder="Nhập mã đặt vé"
                  // prefix={< />}
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

              <Form.Item label={null}>
                <Button 
                  htmlType="submit"
                  loading={loadingLookup}
                  block  
                  style={{
                    background: "var(--color-primary)",
                    color: 'black',
                    "&:hover": { background: "var(--color-primary-dark)" },
                  }}
                  icon={<SearchOutlined />}
                >
                  Tìm vé
                </Button>
              </Form.Item>
            </Form>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};
export default LookupTicketPage;


const TicketCard = () => {

  return (
    <>

    </>
  )
}