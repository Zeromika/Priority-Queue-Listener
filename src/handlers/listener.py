import logging
from queue import Queue, PriorityQueue
import threading

class MessageListenerThread(threading.Thread):

    def __init__(self, generator_queue, processor_queue):
        """Initializes the `MessageListenerThread` whch receives messages from a given queue, buffers them in a `PriorityQueue` and then sends them to be processed in an ordered manner.

        Args:
            generator_queue (queue.Queue): input queue (to be consumed)
            processor_queue (queue.Queue): output queue (to be processed)
        """
        super(MessageListenerThread,self).__init__()
        self.name = "MessageListener"
        self.buffer : PriorityQueue = PriorityQueue()
        self.generator_queue : Queue = generator_queue
        self.processor_queue : Queue = processor_queue
        self.expected_message_id : int = 0 # last message id

    def run(self):
        """Executes `MessageListenerThread` to start consuming messages on the input queue"""
        while True:
            if not self.generator_queue.empty():
                message = self.generator_queue.get()
                self.buffer.put((message.mid, message)) # Store a tuple so that `PriorityQueue `can order them based on the priority.
                logging.debug(f"Received Message({message.mid})")
                # Create and fill the batch
                batch = []
                while not self.buffer.empty() and self.buffer.queue[0][0] == self.expected_message_id :
                    buffered_msg = self.buffer.get()
                    message_to_process = buffered_msg[1] # Get the second item of the tuple stored in the queue
                    self.expected_message_id += 1
                    batch.append(message_to_process)
                if batch:
                    self.processor_queue.put(batch)