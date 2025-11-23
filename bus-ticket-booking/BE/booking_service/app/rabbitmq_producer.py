"""
RabbitMQ Producer for Booking Service
Publishes events to message queues
"""
import pika
import json
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQProducer:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300,
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logger.info(f"Producer connected to RabbitMQ at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            return False

    def publish_message(
        self,
        queue_name: str,
        message: Dict[str, Any],
        priority: int = 0
    ) -> bool:
        """
        Publish a message to a specific queue
        """
        if not self.channel:
            logger.error("Channel not initialized. Call connect() first.")
            return False

        try:
            # Declare queue (idempotent) - MUST match consumer's queue declaration exactly
            self.channel.queue_declare(
                queue=queue_name,
                durable=True,
                arguments={
                    'x-dead-letter-exchange': 'dlx_exchange',
                    'x-dead-letter-routing-key': 'dead_letter',
                    'x-message-ttl': 86400000  # 24 hours - MUST match consumer
                }
            )

            # Publish message
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            
            logger.info(f"Published message to {queue_name}: {message.get('booking_code', 'N/A')}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish message to {queue_name}: {e}")
            return False

    def publish_booking_confirmation(
        self,
        to_email: str,
        booking_code: str,
        customer_name: str,
        trip_info: str,
        seat_numbers: list,
        total_price: float,
        booking_time: str
    ) -> bool:
        """Publish booking confirmation event"""
        message = {
            'to_email': to_email,
            'booking_code': booking_code,
            'customer_name': customer_name,
            'trip_info': trip_info,
            'seat_numbers': seat_numbers,
            'total_price': total_price,
            'booking_time': booking_time
        }
        return self.publish_message('booking_confirmation_queue', message, priority=5)

    def publish_booking_cancellation(
        self,
        to_email: str,
        booking_code: str,
        customer_name: str,
        cancellation_reason: str = "Khách hàng yêu cầu hủy"
    ) -> bool:
        """Publish booking cancellation event"""
        message = {
            'to_email': to_email,
            'booking_code': booking_code,
            'customer_name': customer_name,
            'cancellation_reason': cancellation_reason
        }
        return self.publish_message('booking_cancellation_queue', message, priority=7)

    def publish_booking_refund(
        self,
        to_email: str,
        booking_code: str,
        customer_name: str,
        refund_amount: float
    ) -> bool:
        """Publish booking refund event"""
        message = {
            'to_email': to_email,
            'booking_code': booking_code,
            'customer_name': customer_name,
            'refund_amount': refund_amount
        }
        return self.publish_message('booking_refund_queue', message, priority=8)

    def publish_otp(
        self,
        email: str,
        otp_code: str,
        booking_code: str,
        expiry_minutes: int = 5
    ) -> bool:
        """Publish OTP generation event for email verification"""
        message = {
            'email': email,
            'otp_code': otp_code,
            'booking_code': booking_code,
            'expiry_minutes': expiry_minutes
        }
        return self.publish_message('otp_queue', message)

    def close(self):
        """Close connection"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("Producer connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")


# Global producer instance
_producer_instance = None


def get_producer(rabbitmq_config: dict) -> RabbitMQProducer:
    """Get or create producer instance (singleton pattern)"""
    global _producer_instance
    
    if _producer_instance is None:
        _producer_instance = RabbitMQProducer(
            host=rabbitmq_config['host'],
            port=rabbitmq_config['port'],
            username=rabbitmq_config['username'],
            password=rabbitmq_config['password']
        )
        _producer_instance.connect()
    
    return _producer_instance
