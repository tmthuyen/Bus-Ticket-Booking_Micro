// params

import { useNavigate, useSearchParams } from 'react-router-dom';
import { PAYMENT_METHOD, PREFIX_SERVICES } from '../../../constants';
import api from '../../../api/api';
import { useState } from 'react';
import { Container, Typography } from '@mui/material';
 
const PaymentReturn = () => {
  // const location = useLocation();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const bookingCode = searchParams.get('bookingCode');
  const email = searchParams.get('email');
  const tripId = searchParams.get('tripId');
  

  const callBackPayment = async (method = PAYMENT_METHOD.MOMO) => {
    if (method === PAYMENT_METHOD.MOMO) {
      // query params
      const partnerCode = searchParams.get('partnerCode');
      const resultCode = parseInt(searchParams.get('resultCode'));
      const message = searchParams.get('message');
      const orderId = searchParams.get('orderId');
      const requestId = searchParams.get('requestId');
      const amount = parseInt(searchParams.get('amount'));
      const orderInfo = searchParams.get('orderInfo');
      const orderType = searchParams.get('orderType');
      const transId = parseInt(searchParams.get('transId'));
      const payType = searchParams.get('payType');
      const responseTime = parseInt(searchParams.get('responseTime'));
      const extraData = searchParams.get('extraData');
      const signature = searchParams.get('signature');

      const bodyCallback = {
        partnerCode,
        orderId,
        requestId,
        amount,
        orderInfo,
        orderType,
        transId,
        resultCode,
        message,
        payType,
        responseTime,
        extraData,
        signature,
      };

      try {
        const resp = await api.post(
          `${PREFIX_SERVICES.PAYMENTS}/payments/momo/callback`,
          bodyCallback
        );

        console.log('MOMO callback response:', resp.data);

        // setResultPayment(resp.data);
        const { resultCode, booking_id } = resp.data;
        if (resultCode === 0) {
          // Handle successful payment
          console.log(`Payment successful for booking ID: ${booking_id}`);
          navigate(`/booking-result?bookingId=${booking_id}&paymentId=${orderId}&status=success`);

        } else if (resultCode === 1002) {
          // Handle failed payment
          console.log(`Payment failed with resultCode: ${resultCode}`);
          
          navigate(`/booking-result?bookingId=${booking_id}&paymentId=${orderId}&status=failed`);
        }
      } catch (error) {
        console.error('Error in MOMO callback:', error);
      }
    } else if (method === PAYMENT_METHOD.VNPAY) {
    }
  };

  callBackPayment(searchParams.get('partnerCode'));
  return (
    <>
      <Container maxWidth="lg" sx={{ mt: 1, mb: 4 }}>
        <Typography
          variant="h4"
          style={{ textAlign: 'center', marginBottom: '20px' }}
        >
          Payment Return Page
        </Typography>

        {/* <button onClick={() => callBackPayment(PAYMENT_METHOD.MOMO)}>
          Xử lý callback MOMO
        </button> */}
      </Container>
    </>
  );
};

export default PaymentReturn;
