# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy

import serial_protocol # Для работы с радаром

import serial # для работы с UART Если что - pip3 install pyserial

from rclpy.node import Node

from std_msgs.msg import String# Может другой формат сообщения выбрать?


class MinimalPublisher(Node):

    def __init__(self):
	# Open the serial port
	ser = serial.Serial('/dev/ttyUSB0', 256000, timeout=1)# Тут введи адрес своего UART порта! Иначе надо искать ttl2uart. Хотя у меня где-то есть.
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.01  # seconds потестить скорость работы!
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
	# Read a line from the serial port
        serial_port_line = ser.read_until(serial_protocol.REPORT_TAIL)
        all_target_values = serial_protocol.read_radar_data(serial_port_line)
        
        if all_target_values is None:
            continue # возможно надо иметь некое сообщение, что целей нет.
        target1_x, target1_y, target1_speed, target1_distance_res, \
        target2_x, target2_y, target2_speed, target2_distance_res, \
        target3_x, target3_y, target3_speed, target3_distance_res \
            = all_target_values # Вот все эти данные из all_target_values и передай в сообщение.
        msg.data = 'values: %d' % all_target_values
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
