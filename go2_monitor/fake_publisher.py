import rclpy
from rclpy.node import Node
from unitree_go.msg import LowState

class FakePublisher(Node):
    def __init__(self):
        super().__init__('fake_publisher')                      # 【空1】节点名
        self.publisher = self.create_publisher(LowState, '/lowstate', 10)   # 【空2】话题名
        self.timer = self.create_timer(0.5, self.timer_callback)  # 【空3】回调函数名
        self.get_logger().info('假数据发布者已启动，开始模拟机器狗数据...')

    def timer_callback(self):                                    # 【空4】和空3 一致
        msg = LowState()
        msg.imu_state.rpy = [0.1, 0.05, 0.2]
        msg.bms_state.soc = 85
        msg.motor_state[0].q = 0.5
        msg.motor_state[0].dq = 0.1
        msg.motor_state[0].tau_est = 1.2
        self.publisher.publish(msg)
        self.get_logger().info('已发布一条模拟数据')

def main(args=None):
    rclpy.init(args=args)
    node = FakePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
