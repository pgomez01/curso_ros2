import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
import math

class tfNodePublisher(Node):
  def __init__(self):
    super().__init__('tfnodepublisher')

    #Inicializar el publicador estático
    self.tf_static_broadcaster = StaticTransformBroadcaster(self)
    #Función que crea y publica TFs
    self.publish_static_tfs()

  def publish_static_tfs(self):
    
    tfs = []

    now = self.get_clock().now().to_msg()

    # TF 1: base_link -> sensor_1 (Desplazado en X)
    t1 = TransformStamped()
    t1.header.stamp = now
    t1.header.frame_id = 'base_link'
    t1.child_frame_id = 'sensor_1'
    t1.transform.translation.x = 1.0
    t1.transform.rotation.w = 1.0
    tfs.append(t1)

    # TF 2: base_link -> sensor_2 (Desplazado en Y)
    t2 = TransformStamped()
    t2.header.stamp = now
    t2.header.frame_id = 'base_link'
    t2.child_frame_id = 'sensor_2'
    t2.transform.translation.y = 1.0
    t2.transform.rotation.w = 1.0
    tfs.append(t2)
    
    # TF 3: base_link -> sensor_3 (Desplazado en Z)

    t3 = TransformStamped()
    t3.header.stamp = now
    t3.header.frame_id = 'base_link'
    t3.child_frame_id = 'sensor_3'
    t3.transform.translation.z = 1.0
    t3.transform.rotation.w = 1.0
    tfs.append(t3)

    self.tf_static_broadcaster.sendTransform(tfs)
    self.get_logger().info('Las 3 TFs estáticas han sido publicadas')

def main (args=None):
  rclpy.init()
  node = tfNodePublisher()
  rclpy.spin(node)
  rclpy.shutdown()

if __name__ == 'main':
  main()




    
  