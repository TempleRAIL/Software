#!/usr/bin/env python


# Imports
import rospy
from fleet_messaging.duckiemq import DuckieMQSender
from std_msgs.msg             import ByteMultiArray
from ruamel.yaml              import YAML


class Sender(object):
    """
    Sender class for the duckietown fleet messaging.
    Listens to an outbox topic and then sends out msg to other duckiebots.
    """
    def __init__(self):
        # Initialize node
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing." %(self.node_name))

        rospy.loginfo("[%s] 1" %(self.node_name))

        # Load the parameters
        config_path = self.__setup_parameter("~config")
        rospy.loginfo("[%s] 2" %(self.node_name))
        self.iface = self.__setup_parameter("~iface")
        rospy.loginfo("[%s] 3" %(self.node_name))

        # Load the configuration
        try:
            with open(config_path, "r") as config_file:
                # Load the configuration file
                yaml_obj = YAML()
                config_yaml = yaml_obj.load(config_file)
        except IOError:
            output = "[%s] File \"%s\" does not exist! Please use an existing file!"
            rospy.logfatal(output %(self.node_name, config_path))
            raise
        
        rospy.loginfo("[%s] 4" %(self.node_name))

        # Loop through the configuration
        try:
            self.config = {}
            for entry in config_yaml:
                # Create the socket
                port = entry["port"]
                socket = DuckieMQSender(self.iface, port)

                # Create the subscriber
                sub_topic = entry["sub"]
                cb_fun = create_cb(self.node_name, socket)
                sub = rospy.Subscriber(sub_topic, ByteMultiArray, cb_fun)

                # Populate the configuration
                self.config[entry["name"]] = (
                    port,
                    sub_topic,
                    sub,
                    socket
                )
        except TypeError:
            output = "[%s] Syntax error in \"%s\"!"
            rospy.logfatal(output %(self.node_name, config_path))
            raise

    def __setup_parameter(self, param_name, default_value="None"):
        """
        Setup a node parameter.
        Inputs:
        - param_name:    Parameter name (see launch file)
        - default_value: Default parameter value (define in launch file!)
        Outputs:
        - value: Parameter value
        """
        rospy.loginfo("[%s] config 1" %(self.node_name))
        value = rospy.get_param(param_name, default_value)
        rospy.loginfo("[%s] name: %s (%s), value: %s" %(self.node_name, param_name, rospy.resolve_name(param_name), value))
        rospy.set_param(param_name, value)

        rospy.loginfo("[%s] %s = %s " %(self.node_name, param_name, value))

        return value

    def on_shutdown(self):
        """
        Perform cleanup on shutdown.
        """
        rospy.loginfo("[%s] Shutting down." %(self.node_name))

        # Loop through the configuration
        for key in self.config:
            # Destroy the sockets
            self.config[key][3].cleanup()


def create_cb(node_name, socket):
    """
    Create a callback function for an incomin ROS topic.
    Inputs:
    - node_name: ROS node name
    - socket:    ZeroMQ socket
    Outputs:
    - send_cb: Callback function (pointer)
    """
    def send_cb(msg):
        """
        A callback that sends out message to other duckiebots through
        multicast.
        Inputs:
        - msg: ROS message
        Outputs:
        None
        """
        timestamp = rospy.Time.now()
        socket.send_serialized(msg)
        rospy.loginfo("[%s] Sending msg at time: %s" %(node_name,
                                                       str(timestamp)))

    return send_cb


if __name__ == "__main__":
    # Initialize the node with rospy
    rospy.init_node('sender_node', anonymous=False)

    # Create the sender object
    SENDER = Sender()

    # Setup proper shutdown behavior
    rospy.on_shutdown(SENDER.on_shutdown)

    # Keep it spinning to keep the node alive
    rospy.spin()