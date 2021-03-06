"""This module provides a very basic Node class template.

Examples:
    ::
        from hippocampus_common.node import Node

        if __name__ == "__main__":
            my_node = Node(name="my_simple_node")
            default = "If you see this, the param was not set before."
            param = my_node.get_param("~my_private_param", default=default)
            print(param)
            my_node.run()

    ::
        from hippocampus_common.node import Node


        class MyAdvancedNode(Node):
            def __init__(self, name):
                super(MyAdvancedNode, self).__init__(name=name)
                ...


        if name == "__main__":
            my_node = MyAdvancedNode("my_advanced_node")

"""
import rospy


class Node(object):
    """A basic node class to start off with, when implementing a ROS node.
    """
    def __init__(self, name, anonymous=False, disable_signals=False):
        """Initializes a ROS node by calling ``rospy.init_node``.

        Args:
            name (str): Name of the node.
            anonymous (bool, optional): If true a random number is appended to
                the node's name. Defaults to False.
            disable_signals (bool, optional): ROS handles ctrl+c if set to
                false. Defaults to False.
        """
        rospy.init_node(name,
                        anonymous=anonymous,
                        disable_signals=disable_signals)
        rospy.loginfo("[{}] Initialized.".format(rospy.get_name()))

    def run(self):
        """Enters a loop (namely ``rospy.spin()``) until ROS is shut down to
        keep the program from exiting prematurely.

        Override this method if your node should do something besides waiting
        for arriving messages.
        """
        while not rospy.is_shutdown():
            rospy.spin()
        rospy.loginfo("[{}] Shutting down...".format(rospy.get_name()))

    @staticmethod
    def get_param(name, default=None, verbose=True, limit=80 * 5):
        """Get a parameter from the ROS parameter server.

        Logs a warning if parameter does not exist sets the default value
        afterwards.

        Args:
            name (str): Name of the parameter.
            default (optinal): Default value to be used if parameter does not
                exist. Defaults to None.
            verbose (bool, optional): Defaults to True.
            limit (int, optional): Limit the length of the printed parameter
                value to specified number of characters if > 0. Defaults to
                ``80 * 50``.
        Returns:
            Any: Either the read parameter or the default value if
                it does not exist. If no default value was given, None will be
                returned.
        """
        try:
            param = rospy.get_param(name)
        except KeyError:
            param = default
            if default is None:
                rospy.logwarn(
                    "[{}] No default value given for parameter '{}', unexpected"
                    " behaviour possible.".format(rospy.get_name(), name))
            else:
                rospy.set_param(name, default)
                rospy.logwarn("[{}] Parameter '{}' does not exist. "
                              "Using default value '{}'.".format(
                                  rospy.get_name(), name, default))
        else:
            if verbose:
                param_string = "{}".format(param)
                if limit > 0 and len(param_string) > limit:
                    param_string = param_string[:limit] + "..."
                rospy.loginfo("[{}] {}={}".format(rospy.get_name(), name,
                                                  param_string))
        return param

    @staticmethod
    def set_param(name, value, verbose=True, limit=80 * 5):
        """Set parameter verbosly.

        Args:
            name (str): Name of the parameter.
            value: Value of the parameter that is set.
            verbose (bool, optional): Defaults to True.
            limit (int, optional): Limit the length of the printed parameter
                value to specified number of characters if > 0. Defaults to
                ``80 * 50``.
        """
        rospy.set_param(name, value)
        value_string = "{}".format(value)
        if limit > 0 and len(value_string) > limit:
            value_string = value_string[:limit] + "..."
        rospy.loginfo("[{}] {}={}".format(rospy.get_name(), name, value_string))
