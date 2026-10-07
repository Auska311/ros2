import platform
import time

import psutil
import rclpy
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from rclpy.node import Node

from status_interfaces.msg import SystemStatus


class SystemStatusPublisher(Node):
    def __init__(self):
        super().__init__('system_status_publisher')

        self.publisher = self.create_publisher(
            SystemStatus,
            'system_status',
            10
        )

        self.timer = self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()

        msg = SystemStatus()

        msg.timestamp = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime()
        )
        msg.hostname = platform.node()
        msg.cpu_usage = psutil.cpu_percent(interval=None)
        msg.memory_usage = memory.percent
        msg.total_memory = memory.total
        msg.free_memory = memory.available
        msg.network_rx_bytes = network.bytes_recv
        msg.network_tx_bytes = network.bytes_sent

        self.publisher.publish(msg)


class StatusWindow(QWidget):
    def __init__(self, node):
        super().__init__()

        self.node = node

        self.setWindowTitle('System Status')
        self.resize(400, 300)

        self.label = QLabel()
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

        self.update_status()

    def update_status(self):
        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()

        text = (
            f'Time: {time.strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'Host Name: {platform.node()}\n'
            f'CPU Usage: {psutil.cpu_percent(interval=None):.1f}%\n'
            f'Memory Usage: {memory.percent:.1f}%\n'
            f'Total Memory: {memory.total} bytes\n'
            f'Free Memory: {memory.available} bytes\n'
            f'Network RX: {network.bytes_recv} bytes\n'
            f'Network TX: {network.bytes_sent} bytes'
        )

        self.label.setText(text)


def main(args=None):
    rclpy.init(args=args)

    node = SystemStatusPublisher()

    app = QApplication([])

    window = StatusWindow(node)
    window.show()

    ros_timer = QTimer()
    ros_timer.timeout.connect(
        lambda: rclpy.spin_once(node, timeout_sec=0)
    )
    ros_timer.start(10)

    try:
        app.exec_()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
