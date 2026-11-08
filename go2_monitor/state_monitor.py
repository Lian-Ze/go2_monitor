import time
import rclpy
from rclpy.node import Node
from unitree_go.msg import LowState


class StateMonitorNode(Node):
    def __init__(self):
        super().__init__('state_monitor')
        self.subscription = self.create_subscription(
            LowState, '/lowstate', self.callback, 10)
        # 记录"上次收到数据的时间"，初始为当前时间
        self.last_msg_time = time.time()
        # 定时器：每 1 秒检查一次是否失联
        self.timer = self.create_timer(1.0, self.check_timeout)
        self.get_logger().info('状态监控节点已启动，等待 /lowstate 数据...')

    def callback(self, msg):
        # 每次收到消息，更新"最后收到时间"
        self.last_msg_time = time.time()

        # 读取 IMU 姿态（横滚/俯仰/偏航）
        rpy = msg.imu_state.rpy
        self.get_logger().info(
            f'IMU姿态  roll={rpy[0]:.2f}  pitch={rpy[1]:.2f}  yaw={rpy[2]:.2f}')

        # 读取电池电量
        soc = msg.bms_state.soc
        self.get_logger().info(f'电池电量 = {soc}%')
        if soc < 20:                             
            self.get_logger().warn(f'⚠️ 低电量告警：电量只剩 {soc}%！')
        else:
            self.get_logger().info(f'电池电量 = {soc}%')

        # 读取第 0 号关节电机的状态
        m0 = msg.motor_state[0]
        self.get_logger().info(
            f'关节0  位置={m0.q:.2f}  速度={m0.dq:.2f}  力矩={m0.tau_est:.2f}')

    def check_timeout(self):
        # 超过 3 秒没收到数据，判定失联
        if time.time() - self.last_msg_time > 3.0:
            self.get_logger().warn('⚠️ 失联告警：超过 3 秒未收到数据！')


def main(args=None):
    rclpy.init(args=args)
    node = StateMonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
