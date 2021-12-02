import threading
import random
import logging
import time

class Message:
    def __init__(self, mid) -> None:
        self.mid = mid


class MessageGeneratorThread(threading.Thread):

    def __init__(self, queue, count=100):
        """Initializes `MessageGeneratorThread` which generates messages pseudo randomly while keeping a record of the previously generated messages.

        Args:
            queue (`queue.Queue`): output queue
            count (int, optional): number of messages to be generated. Defaults to 100.
        """
        super(MessageGeneratorThread,self).__init__()
        self.name = "MessageGenerator"
        self.queue = queue
        self.count = count
        self._messages_generated = 0
        self.seen = set()

    def _random_message_(self) -> Message:
        """Generates a message with a random id within the range of `MessageGeneratorThread.count`

        Returns:
            Message: A random message
        """
        r = random.randint(0, self.count)
        if r in self.seen:
            return self._random_message_()
        self.seen.add(r)
        logging.debug(f"Generated Message({r})")
        return Message(r)

    def run(self):
        """Runs the `MessageGeneratorThread` which outputs random messages to output queue every 0.5 seconds
        """
        while self._messages_generated <= self.count:
            time.sleep(0.5) # Used to simulate delays in the messages arriving to the queue
            self.queue.put(self._random_message_())
            self._messages_generated += 1
        return