import { useState } from "react";
import { Input } from "antd";

const OtpConfirm = ({ otp, setOtp }) => {
  // // value của OTP là mảng string, mỗi ô 1 phần tử
  // const [otp, setOtp] = useState([]);

  const handleInput = (valueArr) => {
    // valueArr: ["1", "a", "3", ...]
    const digitsOnly = valueArr.map((ch) => ch.replace(/\D/g, "")); // chỉ giữ 0–9
    setOtp(digitsOnly);
    console.log("onInput (raw):", valueArr, "=> digits:", digitsOnly);
  };

  const handleChange = (text) => {
    // text: "123456" khi đã nhập đủ length
    console.log("OTP complete:", text);
  };

  return (
    <div style={{ width: "100%" }}>
      <Input.OTP
        length={6}                      // số ô OTP
        value={otp}                     // controlled
        onInput={handleInput}           // lọc chỉ số
        onChange={handleChange}         // khi nhập đủ
        inputMode="numeric"             // gợi ý bàn phím số trên mobile
        pattern="[0-9]*"                // hint cho browser
        separator={(i) => (
          <span style={{ color: i & 1 ? "red" : "blue" }}>—</span>
        )}
      />
    </div>
  );
};

export default OtpConfirm;
