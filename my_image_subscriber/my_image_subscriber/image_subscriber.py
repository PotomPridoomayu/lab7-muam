# Импортируем необходимые модули ROS 2 для работы с узлами и сообщениями
import rclpy
from rclpy.node import Node
# Импортируем сообщение Image из пакета sensor_msgs для работы с изображениями
from sensor_msgs.msg import Image
# Импортируем CvBridge для конвертации между ROS-изображениями и OpenCV
from cv_bridge import CvBridge, CvBridgeError
# Импортируем OpenCV для обработки изображений
import cv2
# Определяем класс ImageSubscriber, который наследует от Node
class ImageSubscriber(Node):
  # Конструктор класса, вызывается при создании экземпляра класса
  def __init__(self):
    # Вызываем конструктор родительского класса Node
    super().__init__('image_subscriber')
    # Создаем подписку на топик с интересуемыми данными с типом сообщения Image
    # и функцией обратного вызова listener_callback
    self.subscription = self.create_subscription(Image, # Тип сообщения
    '/robotcar/radar/cart', # Тема для подписки
    self.listener_callback, # Функция обратного вызова
    10 # QoS (Quality of Service) для подписки
    )
    # Создаем экземпляр CvBridge для конвертации между ROS-изображениями и OpenCV 
    self.bridge = CvBridge()
  # Функция обратного вызова, вызывается при получении нового сообщения
  def listener_callback(self, data):
    try:
      # Преобразуем ROS-изображение в OpenCV-изображение
      # Используем тип "bgr8" для цветных изображений
      cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
    except CvBridgeError as e:
      # Если возникает ошибка при конвертации, выводим сообщение в лог
      self.get_logger().info(f'Failed to convert image: {e}')
      return # Прерываем функцию, если ошибка
    # Пример обработки изображения: отображаем его на экране
    # cv2.imshow('Image', cv_image)
    # cv2.waitKey(1) # Задержка для обновления экрана
    self.get_logger().info(f'subscribing data[0]: {data.data[0]}') # Логирование

# Определяем функцию main, которая запускает узел ROS 2
def main(args=None):
  # Инициализируем среду ROS 2
  rclpy.init(args=args)
  # Создаем экземпляр узла ImageSubscriber
  image_subscriber = ImageSubscriber()
  try:
    # Запускаем цикл обработки сообщений узла
    rclpy.spin(image_subscriber)
  except KeyboardInterrupt:
    # Если пользователь прерывает программу (например, Ctrl+C),
    # выводим сообщение в лог и уничтожаем узел
    image_subscriber.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    # Уничтожаем узел и завершаем среду ROS 2
    image_subscriber.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
  main()
