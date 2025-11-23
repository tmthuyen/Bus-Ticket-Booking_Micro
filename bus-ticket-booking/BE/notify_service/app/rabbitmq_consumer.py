"""
RabbitMQ Consumer for Notification Service
Listens to message queues and processes email/OTP events
"""
import pika
import json
import time
import logging
from typing import Callable, Dict
from sqlalchemy.orm import Session

from . import utils
from .database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        max_retries: int = 5,
        retry_delay: int = 5
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connection = None
        self.channel = None
        self.handlers: Dict[str, Callable] = {}

    def connect(self):
        """Establish connection to RabbitMQ with retry logic"""
        retries = 0
        while retries < self.max_retries:
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
                logger.info(f"Connected to RabbitMQ at {self.host}:{self.port}")
                return True
            except Exception as e:
                retries += 1
                logger.error(f"Failed to connect to RabbitMQ (attempt {retries}/{self.max_retries}): {e}")
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
        
        logger.error("Could not connect to RabbitMQ after maximum retries")
        return False

    def declare_queues(self):
        """Declare all queues with DLX (Dead Letter Exchange) support"""
        if not self.channel:
            logger.error("Channel not initialized. Call connect() first.")
            return False

        try:
            # Declare Dead Letter Exchange
            self.channel.exchange_declare(
                exchange='dlx_exchange',
                exchange_type='direct',
                durable=True
            )

            # Declare Dead Letter Queue
            self.channel.queue_declare(
                queue='dead_letter_queue',
                durable=True
            )

            self.channel.queue_bind(
                exchange='dlx_exchange',
                queue='dead_letter_queue',
                routing_key='dead_letter'
            )

            # Main queues with DLX
            queues_config = [
                'booking_confirmation_queue',
                'booking_cancellation_queue',
                'booking_refund_queue',
                'otp_queue'
            ]

            for queue_name in queues_config:
                self.channel.queue_declare(
                    queue=queue_name,
                    durable=True,
                    arguments={
                        'x-dead-letter-exchange': 'dlx_exchange',
                        'x-dead-letter-routing-key': 'dead_letter',
                        'x-message-ttl': 86400000  # 24 hours
                    }
                )
                logger.info(f"Declared queue: {queue_name}")

            return True
        except Exception as e:
            logger.error(f"Failed to declare queues: {e}")
            return False

    def register_handler(self, queue_name: str, handler: Callable):
        """Register a handler function for a specific queue"""
        self.handlers[queue_name] = handler
        logger.info(f"Registered handler for queue: {queue_name}")

    def _callback_wrapper(self, queue_name: str):
        """Create a callback wrapper for the handler"""
        def callback(ch, method, properties, body):
            try:
                logger.info(f"Received message from {queue_name}")
                data = json.loads(body)
                
                # Get handler for this queue
                handler = self.handlers.get(queue_name)
                if not handler:
                    logger.error(f"No handler registered for queue: {queue_name}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    return

                # Process message
                db = SessionLocal()
                try:
                    success = handler(data, db)
                    if success:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        logger.info(f"Message processed successfully from {queue_name}")
                    else:
                        # Retry with requeue
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                        logger.warning(f"Message processing failed, requeued: {queue_name}")
                finally:
                    db.close()

            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                logger.error(f"Error processing message from {queue_name}: {e}")
                # Send to DLX after 3 failed attempts
                if method.delivery_tag % 3 == 0:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                else:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        return callback

    def start_consuming(self):
        """Start consuming messages from all registered queues"""
        if not self.channel:
            logger.error("Channel not initialized. Call connect() first.")
            return

        try:
            # Set QoS - process one message at a time
            self.channel.basic_qos(prefetch_count=1)

            # Start consuming from all queues
            for queue_name in self.handlers.keys():
                self.channel.basic_consume(
                    queue=queue_name,
                    on_message_callback=self._callback_wrapper(queue_name)
                )
                logger.info(f"Listening to queue: {queue_name}")

            logger.info("RabbitMQ Consumer started. Waiting for messages...")
            self.channel.start_consuming()

        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Error in consumer: {e}")
            self.stop_consuming()

    def stop_consuming(self):
        """Stop consuming and close connections"""
        try:
            if self.channel:
                self.channel.stop_consuming()
            if self.connection:
                self.connection.close()
            logger.info("RabbitMQ Consumer stopped")
        except Exception as e:
            logger.error(f"Error stopping consumer: {e}")


# Message Handlers
def handle_booking_confirmation(data: dict, db: Session) -> bool:
    """Handle booking confirmation email"""
    try:
        logger.info(f"Sending booking confirmation to {data.get('to_email')}")
        utils.send_booking_confirmation_email(
            receiver_email=data.get('to_email'),
            booking_code=data.get('booking_code'),
            customer_name=data.get('customer_name'),
            trip_info=data.get('trip_info'),
            seat_numbers=data.get('seat_numbers', []),
            total_price=data.get('total_price'),
            booking_time=data.get('booking_time')
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send booking confirmation: {e}")
        return False


def handle_booking_cancellation(data: dict, db: Session) -> bool:
    """Handle booking cancellation email"""
    try:
        logger.info(f"Sending booking cancellation to {data.get('to_email')}")
        utils.send_booking_cancellation_email(
            receiver_email=data.get('to_email'),
            booking_code=data.get('booking_code'),
            customer_name=data.get('customer_name'),
            cancellation_reason=data.get('cancellation_reason', 'Khách hàng yêu cầu hủy')
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send booking cancellation: {e}")
        return False


def handle_booking_refund(data: dict, db: Session) -> bool:
    """Handle booking refund email"""
    try:
        logger.info(f"Sending booking refund to {data.get('to_email')}")
        utils.send_booking_refund_email(
            receiver_email=data.get('to_email'),
            booking_code=data.get('booking_code'),
            customer_name=data.get('customer_name'),
            refund_amount=data.get('refund_amount')
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send booking refund: {e}")
        return False


def handle_otp_message(data: dict, db: Session) -> bool:
    """Handle OTP generation and sending - Email verification for booking"""
    try:
        email = data.get('email')
        booking_code = data.get('booking_code')
        logger.info(f"Sending OTP to {email} for booking {booking_code}")
        
        utils.send_otp_email(
            receiver_email=email,
            otp_code=data.get('otp_code'),
            booking_code=booking_code,
            expiry_minutes=data.get('expiry_minutes', 5)
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send OTP: {e}")
        return False


def setup_consumer(rabbitmq_config: dict) -> RabbitMQConsumer:
    """Setup and configure RabbitMQ consumer"""
    consumer = RabbitMQConsumer(
        host=rabbitmq_config['host'],
        port=rabbitmq_config['port'],
        username=rabbitmq_config['username'],
        password=rabbitmq_config['password']
    )

    # Connect and declare queues
    if consumer.connect():
        consumer.declare_queues()
        
        # Register handlers
        consumer.register_handler('booking_confirmation_queue', handle_booking_confirmation)
        consumer.register_handler('booking_cancellation_queue', handle_booking_cancellation)
        consumer.register_handler('booking_refund_queue', handle_booking_refund)
        consumer.register_handler('otp_queue', handle_otp_message)
        
        return consumer
    
    return None
