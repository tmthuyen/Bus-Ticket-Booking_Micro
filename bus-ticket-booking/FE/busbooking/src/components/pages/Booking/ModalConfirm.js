import { Input, Modal } from 'antd';
// import { useState } from 'react';

const ModalConfirm = ({ isModalOpen, setIsModalOpen, onSubmit, otp, setOtp }) => {
  // OTP là string, ví dụ: "123456"
  // const [otp, setOtp] = useState("");

  const handleOk = () => {
    // call API confirm otp với otp string
    // console.log("Confirm OTP:", otp);

    // if (otp.length < 6) {
    //   return;
    // }

    // const OTP = otp;
    // console.log("Submitting OTP:", OTP);

    // // TODO: gọi API xác thực OTP
    // // nếu thành công:
    // //   - đóng modal
    // //   - redirect sang trang thanh toán
    // // nếu thất bại:
    // //   - show message lỗi (antd message / Modal.error)

    // setIsModalOpen(false);
    // setOtp("");
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleInput = (value) => {
    // value là string, VD: "1a3" → lọc chỉ giữ số
    if (value.length > 6) {
      setOtp(value.slice(0, 6));
      return; // giới hạn độ dài tối đa 6
    }
    if (!value) {
      setOtp("");
      return;
    } 
    console.log("Raw input:", value);
    setOtp(value?.join(""))
    
  };

  const handleChange = (text) => {
    // text là string, khi điền đủ length (6) sẽ gọi
    console.log("OTP complete:", text);
    // có thể setOtp(text); nhưng ở đây mình đã set trong onInput rồi
  };

  return (
    <Modal
      title="Xác nhận OTP với thông tin đặt vé"
      open={isModalOpen}
      onOk={onSubmit}
      onCancel={handleCancel}
      // closable chỉ cần boolean thôi
      closable
    >
      <div style={{ width: '100%' }}>
        <Input.OTP
          length={6}             // 6 số OTP
          value={otp}            // controlled string
          formatter={str => str.replace(/\D/g, "")}
          onInput={handleInput}  // lọc chỉ số
          onChange={handleChange}
          inputMode="numeric"    // gợi ý bàn phím số trên mobile
          pattern="[0-9]*"       // hint form
          // separator nếu thích thêm dấu gạch giữa các ô:
          // separator={<span style={{ margin: "0 4px" }}>-</span>}
          className="otp-input-custom"
        />
      </div>
    </Modal>
  );
};

export default ModalConfirm;
