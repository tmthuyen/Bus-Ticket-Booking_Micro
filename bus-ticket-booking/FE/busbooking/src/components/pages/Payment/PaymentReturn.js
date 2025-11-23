
// params

import { useSearchParams } from "react-router-dom";

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

  // query params
  const bookingCode = searchParams.get('bookingCode');
  const email = searchParams.get('email');
  const tripId = searchParams.get('tripId');
  const partnerCode = searchParams.get('partnerCode');
  const resultCode = parseInt(searchParams.get('resultCode'));
  const message = searchParams.get('message');
  console.log('Payment Return - query params:', {
    bookingCode,
    email,
    tripId,
    partnerCode,
    resultCode,
    message
  });

  return (
    <>
      <h2>Payment Return Page</h2>
      <div>
        <p>Booking Code: {bookingCode}</p>
        <p>Email: {email}</p>
        <p>Trip ID: {tripId}</p>
        <p>Partner Code: {partnerCode}</p>
        <p>Result Code: {resultCode}</p>
        <p>{resultCode === 0 ? 'Payment Successful' : 'Payment Failed'}</p>
        <p>Message: {message}</p>
      </div>
    </>
  )
};

export default PaymentReturn;