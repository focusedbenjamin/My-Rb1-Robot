from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    package_name = 'my_rb1_description'

    urdf_file = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        'my_rb1_robot.urdf'
    )

    # Start Gazebo
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', 'empty.world'],
        output='screen'
    )

    # Robot state publisher 
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(urdf_file).read()},
        {'use_sim_time': True}],
        output='screen'
    )

    # Spawn robot 
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'rb1_robot',
        '   -topic', 'robot_description'
        ],
        output='screen'
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock]",
            "/cmd_vel@geometry_msgs/msg/Twist[gz.msgs.Twist]",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry]",
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan]",
            "/tf_static@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V]"
        ],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        spawn_entity,
        bridge
    ])