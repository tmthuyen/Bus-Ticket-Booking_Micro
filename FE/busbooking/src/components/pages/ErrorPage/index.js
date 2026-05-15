import { Button } from 'antd';
import { useSearchParams } from 'react-router-dom';

function ErrorPage(props) {
  const { status, message } = props;
  const [searchParams] = useSearchParams();
//   console.log('ErrorPage params:', searchParams.get('status'), searchParams.get('message'));
  return (
    <div
      style={{
        fontSize: '30px',
      }}
    >
      <h2>{searchParams.get('status') || status}</h2>
      <p>{searchParams.get('message') || message}</p>
      <Button type="primary" onClick={() => window.location.href = '/'}>
          Go Back Home 
      </Button>
    </div>
  );
}

export default ErrorPage;
