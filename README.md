# Priority Queue Listener

## Problem Statement

A message processing component receives an unknown number of messages that are numbered from 0..N, one at a time. The value of N is unknown. Delivery is reliable in the sense that all messages will eventually be received. However, the order in which they are received can be completely random.

## Solution

To solve this problem we define three different thread classes, and a data class to both simulate the problem and solve the problem.

To simulate messages being sent and received we define a very simple `Message` class by just having a message-id attribute.

```python
class Message:
    def __init__(self, mid) -> None:
        self.mid = mid
```

The problem describes that an undefined number of messages will be arriving at the system which indicates that the data structure used for the buffer can be dynamic. The main criteria we have for the buffer is that the problem requires us to process batches now and then in an ordered fashion. A simple queue can be dynamic however does not store the messages correctly ordered. To achieve this property we can make use of priority queues which orders items inserted into the queue based on their priorities.

With these assumptions as to the basis of our solution, we implement three different threads to simulate the problem while solving it.

- `MessageListenerThread` is responsible for listening to messages from the input `Queue` and buffering them with an instance of `PriorityQueue`. The messages stored in the buffer are processed once the conditions in the problem are met by outputting `List<Message>` to the output `Queue`.
- `MessageGeneratorThread` generates multiple instances of `Message` and assigns them random message-ids while outputting to a given `Queue`.
- `MessageProcessorThread` is a simple thread that encapsulates a simple processing mechanism and does not do any computation on the received instances of `Message` other than logging them for progress.

Threads defined for the solution of this problem are designed for simulation as such most of them make use of logging statements to show the state of the program throughout the runtime.
