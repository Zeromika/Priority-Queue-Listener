import threading
import logging
from .generator import Message


class UnexpectedMessageError(Exception):
    """Exception raised when the expected message id is not the same as message being processed.

    Attributes:
        value -- expected message id
    """

    def __init__(self, value):
        self.message = f"Message ID does not match the expected Message ID ({value})"


class MessageProcessThread(threading.Thread):
    def __init__(self, queue):
        """Initializes a `MessageProcessorThread` designed to simulate messages being processed from an attached `queue.Queue`.

        Args:
            queue (`queue.Queue`): queue to be used as the output for the generator
        """
        super(MessageProcessThread,self).__init__()
        self.name = "MessageGenerator"
        self.queue = queue
        self.expected_message_id = 0

    def process_message(self, messages: list[Message]):
        """[summary]

        Args:
            messages (list[Message]): List of messages being processed

        Raises:
            UnexpectedMessageError: Unexpected message id error
        """
        for m in messages:
            logging.debug(f"Processed Message({m.mid})")
            try:
                if m.mid != self.expected_message_id:
                    raise UnexpectedMessageError(self.expected_message_id)
            except UnexpectedMessageError as e:
                logging.error(e)
            self.expected_message_id += 1

    def run(self):
        """Runs the thread and starts processing messages when the attached queue is non-empty."""
        while True:
            if not self.queue.empty():
                messages = self.queue.get()
                self.process_message(messages)