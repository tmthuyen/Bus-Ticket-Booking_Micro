import FormPayment from "../Home/FormPayment";
import FormPayer from "../Home/FormPayer";
import FormInfo from "../Home/FormInfo";
import { useState } from "react";
import { Divider } from "antd";
import { useOutletContext } from "react-router-dom"; 
import FormPayment2 from "../Home/FormPayment_2";

function Payment() {

  const { profile } = useOutletContext();
  const [receiverData, setReceiverData] = useState(null);

  const handleReset = () => {
    setReceiverData(null); // reset dữ liệu người nhận
  };

  return (
    <>
      <FormPayer profile={profile} />
      <Divider />
      <FormInfo receiverData={receiverData} setReceiverData={setReceiverData} />
      <Divider />
      <FormPayment2 
        receiverData={receiverData}
        onReset={handleReset} 
      />
    </>
  );
}

export default Payment;
