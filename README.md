[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# PyJavaZ

PyJavaZ is a high-performance bridge that allows Java code to be called in Python using pure python syntax. Inspired by the design of Jupyter notebooks, it uses a backend based on the ZeroMQ messaging protocol. This means it can be used both on a single machine, or across a network.

## Background

PyJavaZ was originally developed as part of the [Pycro-Manager](https://github.com/micro-manager/pycro-manager) project, a Python interface to the Java-based Micro-Manager software for microscope control. It was developed because of the need for a unique set of requirements compared to existing Java-Python interoperability libraries like Jython, Py4J, and JPype. Specifically, operating the Java Virtual Machine and python interpreter in independent processes, while maintaining high enough data transfer performance to be able to handle large amounts of data passing between processes.

## Key Features

- High-performance data transfer speeds of up to 200MB/s
- No need for deep understanding of Java or changes to shared memory configuration
- Simplifies the developer experience by running Python and Java in separate processes
- Supports multi-threading in both languages

## Contributing

This repository works and is actively used as part of the pycro-manager project, but its original authors have no concrete plans for future development. Contributions are welcome! In particular, automated testing would ensure its robustness and allow the addition of new features.

## Getting Started

Download the jar file containing the Java-side code, either by including it as a maven dependency or directly downloading it. Launch the `ZMQServer` class, which will automatically discover the signatures of available classes:

```java
int port = 4827; // which port the server will listen on
new ZMQServer(port);
```

Once this server is running, python client processes can connect to it and call Java code as if it were written in python. To connect to it, first install the python side library: `pip install pyjavaz`, then run:

```python
from pyjavaz import JavaObject

point = JavaObject("java.awt.Point", args=[1, 2])

# access fields
print(point.x, point.y)

# run methods
point.translate(3, 5)
print(point.x, point.y)
```

## How it works

The PyJavaZ bridge operates by running a ZeroMQ server within the Java layer. This server provides access to Java objects, functions, and data in the form of language-agnostic messages. On the Python side, a ZeroMQ client dynamically translates these messages into Python objects/functions and NumPy arrays.

When a new Java object is requested from the Python side, a message is sent to the Java server with the classpath, argument types, and arguments for the constructor. The Java server then creates the object and sends back a JSON string containing information about the object's fields, methods, and unique identifier.

The Python client deserializes this JSON and dynamically creates a Python object with the same fields and methods as the Java object. When a field is accessed or a method is called on the Python object, a message is sent to the Java server with instructions on what action to take on the shadowed Java object.

When the Python object is garbage collected, a message is sent to the Java server to release the reference to the corresponding Java object, allowing it to be garbage collected as well.

### Multi-threading support

The library supports multi-threading in both languages, with the caveat that blocking calls on a single port can prevent other threads from communicating across the bridge. For this reason, multiple servers/clients can be created that operate on different ports.




### Passing Python objects to Java

Currently, PyJavaZ does not directly support passing arbitrary Python objects to Java. However, you can use the push and pull sockets to achieve this.

### Push and Pull Sockets

Push and Pull Sockets

In addition to the main request-reply socket, PyJavaZ also supports push and pull sockets. These allow for one-way communication between Java and Python.

A push socket in Java can be used to send messages to a pull socket in Python, without expecting a reply. This is useful for passing objects or data from Java to Python asynchronously.

Conversely, a pull socket in Java can receive messages sent from a push socket in Python. This allows Python code to pass objects or data to Java without blocking.

These sockets are created and used similarly to the main request-reply socket:

```python

from pyjavaz import PushSocket, PullSocket

# In Python
push_socket = PushSocket(port=5555)
push_socket.send(some_object)

pull_socket = PullSocket(port=5556)
data = pull_socket.receive()
```

```java

PullSocket<SomeType> pullSocket = new PullSocket<>(port, deserializationFunction);
SomeType data = pullSocket.next();

PushSocket<SomeType> pushSocket = new PushSocket<>(port, serializationFunction);
pushSocket.push(someData);
```


In Java, the PullSocket and PushSocket classes are generic, allowing you to specify the type of data you expect to receive or send. They also require a deserialization or serialization function, respectively, to convert between the data type and a JSONObject.

The PullSocket has a `next()` method that blocks until a message is received, deserializes it using the provided deserialization function, and returns the result.

The PushSocket has a `push()` method that takes an object of the specified type, serializes it using the provided serialization function, and sends it to any connected pull sockets.

This additional socket types provide flexibility for more complex communication patterns between Java and Python.
