import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class DistanceListenerNode(Node):
  def __init__(self):
    super().__init__('listener_node')

    self.tf_buffer = Buffer()
    self.tf_listener = TransformListener(self.tf_buffer, self)
    self.dist_publisher = self.create_publisher(Float64,'distance_rotating_link', 10)
    self.timer = self.create_timer(0.5, self.on_timer)

  def on_timer(self):
    try:
      t = self.tf_buffer.lookup_transform(
        'base_link',
        'camera_link',
        rclpy.time.Time()
                                          )
    except TransformException as ex:
      self.get_logger().info(f'Esperando al TF rotating_link...({ex})')
      return
    
    #Extraer coordenadas
    x = t.transform.translation.x
    y = t.transform.translation.y
    z = t.transform.translation.z

    distance = math.sqrt(x**2 + y**2 + z**2)

    msg = Float64()
    msg.data = float(distance)
    self.dist_publisher.publish(msg)

    self.get_logger().info(f'Distancia desde rotating_link a base_link: {distance:.2f} metros')

def main():
  rclpy.init()
  node = DistanceListenerNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()

