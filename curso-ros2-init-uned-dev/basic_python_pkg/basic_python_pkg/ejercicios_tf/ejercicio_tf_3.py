import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
import math

class CombinedTFPublisher(Node):
    def __init__(self):
        super().__init__('combined_tf_publisher')

        # Broadcasters
        self.tf_broadcaster = TransformBroadcaster(self) #tf dinamico
        self.static_broadcaster = StaticTransformBroadcaster(self) #tf estatico

        # Publicar TF estática una vez
        self.publish_static_tf()

        # Temporizador para la TF dinámica
        self.angle = 0.0
        self.timer = self.create_timer(0.1, self.publish_dynamic_tf)

    def publish_static_tf(self):
        """Transformación estática: arm_link → camera_link"""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'arm_link'
        t.child_frame_id = 'sensor_mount'

        # Cámara fija en la punta del brazo
        t.transform.translation.x = 0.3
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.static_broadcaster.sendTransform(t)
        self.get_logger().info('Soporte estático publicado en la punta del brazo')

    def publish_dynamic_tf(self):
        now = self.get_clock().now().to_msg()
        
        """Transformación dinámica 1: base_link → arm_link"""
        # El brazo gira constantemente en circulo
        t_arm = TransformStamped()
        t_arm.header.stamp = self.get_clock().now().to_msg()
        t_arm.header.frame_id = 'base_link'
        t_arm.child_frame_id = 'arm_link'

        # Brazo girando en yaw
        t_arm.transform.translation.x = 0.0
        t_arm.transform.translation.y = 0.0
        t_arm.transform.translation.z = 0.5

        qz = float(math.sin(self.angle / 2.0))
        qw = float(math.cos(self.angle / 2.0))
        t_arm.transform.rotation.x = 0.0
        t_arm.transform.rotation.y = 0.0
        t_arm.transform.rotation.z = qz
        t_arm.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(t_arm)

        """"Transformación dinámica 2: sensor_mount"""
        # El sensor hace un "barrido" rápido de izquierda a derecha sobre su soporte
        t_sensor = TransformStamped()
        t_sensor.header.stamp = now
        t_sensor.header.frame_id = 'sensor_mount'
        t_sensor.child_frame_id = 'moving_sensor'

        t_sensor.transform.translation.x = 0.0
        t_sensor.transform.translation.y = 0.0
        t_sensor.transform.translation.z = 0.2

        # Calculamos un barrido rapido multiplicando la velocidad de angulo
        sweep_angle = math.sin(self.angle * 3.0)
        qz = float(math.sin(sweep_angle / 2.0))
        qw = float(math.cos(sweep_angle / 2.0))
        t_sensor.transform.rotation.x = 0.0
        t_sensor.transform.rotation.y = 0.0
        t_sensor.transform.rotation.z = qz
        t_sensor.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(t_sensor)

        self.angle += 0.05

def main():
    rclpy.init()
    node = CombinedTFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()