---
sidebar_position: 1
---

# ROS 2 Communication Model

## Core Communication Concepts

ROS 2 provides several ways for nodes to communicate with each other:

### Nodes
Nodes are the fundamental unit of computation in ROS 2. Each node is a process that performs computation. Nodes are organized into packages for better software management.

### Topics and Publishing/Subscription
Topics are named buses over which nodes exchange messages. Messages are data published to a topic and subscribed to by other nodes.

```python
# Example of creating a publisher in Python
import rclpy
from std_msgs.msg import String

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('publisher_node')
    publisher = node.create_publisher(String, 'topic_name', 10)

    def timer_callback():
        msg = String()
        msg.data = 'Hello World'
        publisher.publish(msg)

    timer = node.create_timer(0.5, timer_callback)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

### Services
Services provide a request/reply communication pattern. A service client sends a request to a service server, which processes the request and sends back a response.

### Actions
Actions are used for long-running tasks that may take some time to complete and may be canceled. They provide feedback during execution and result upon completion.

## Basic rclpy-based Agent → Controller Communication Flow

In a typical humanoid robot setup, you might have:

1. **Agent Node**: Makes high-level decisions
2. **Controller Node**: Translates high-level commands to low-level motor commands
3. **Communication**: Through topics, services, or actions depending on the use case

### Example Communication Pattern

```
Agent Node (High-level)
    ↓ (commands via topics/actions)
Controller Node (Low-level)
    ↓ (motor commands)
Hardware Interface
```

## Quality of Service (QoS) Settings

QoS settings allow you to configure how messages are delivered:

- **Reliability**: Best effort or reliable delivery
- **Durability**: Volatile or transient local
- **History**: Keep all or keep last N messages
- **Depth**: Size of the history queue

## Communication Best Practices

1. **Use appropriate QoS settings** for your use case
2. **Keep messages small** to reduce latency
3. **Use services for synchronous requests** and topics for asynchronous data
4. **Use actions for long-running tasks** with feedback
5. **Design clear message interfaces** for better maintainability

## Summary

Understanding the ROS 2 communication model is crucial for building robust humanoid robot systems. The choice of communication pattern (topics, services, or actions) depends on the specific requirements of your application.