// params

import { useSearchParams } from 'react-router-dom';
import { PAYMENT_METHOD, PREFIX_SERVICES } from '../../../constants';
import api from '../../../api/api';
import { useState } from 'react';
import { Container, Typography } from '@mui/material';

/*

http://localhost:3000/payment-return? 
&bookingCode=BK2311256191
&email=tranthuyen2222@gmail.com
&tripId=1
&partnerCode=MOMO
&orderId=BOOK209015b7202511230425236B53ADFB
&requestId=b230dc58-4892-4ffa-b747-d8b3e5861eb5
&amount=850000
&orderInfo=Thanh+to%C3%A1n+v%C3%A9+xe
&orderType=momo_wallet
&transId=4614096933
&resultCode=1002
&message=Successful.
&payType=napas
&responseTime=1763872191084
&extraData=
&signature=31549feb0d74c73d730284e5311edb26a78b7a0974eee3e6ed15e5a3df58d834

*/
const PaymentReturn = () => {
  // const location = useLocation();
  const [searchParams] = useSearchParams();
  const bookingCode = searchParams.get('bookingCode');
  const email = searchParams.get('email');
  const tripId = searchParams.get('tripId');
  // const [resultPayment, setResultPayment] = useState(null);

  /**
   * 
   * class MoMoCallbackRequest(BaseModel):
    """Schema callback từ MoMo"""
    partnerCode: str
    orderId: str
    requestId: str  
    amount: int
    orderInfo: str
    orderType: str
    transId: Optional[int] = None
    resultCode: int
    message: str
    payType: str
    responseTime: int
    extraData: Optional[str] = ""
    signature: str
   */

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
        } else {
          // Handle failed payment
          console.log(`Payment failed with resultCode: ${resultCode}`);
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
