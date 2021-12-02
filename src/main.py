import logging
import queue
import time

from handlers.generator import MessageGeneratorThread
from handlers.listener import MessageListenerThread
from handlers.process import MessageProcessThread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

if __name__ == '__main__':
    generator_q = queue.Queue()
    processor_q = queue.Queue()

    message_generator = MessageGeneratorThread(queue=generator_q, count=100)
    message_processor = MessageProcessThread(queue=processor_q)
    message_listener = MessageListenerThread(generator_queue=generator_q, processor_queue=processor_q)

    # Set threads as daemon to ensure graceful exit
    message_generator.daemon = True
    message_processor.daemon = True
    message_listener.daemon = True 

    message_processor.start()
    message_listener.start()
    message_generator.start()


    try:
        while True:
            # Keep checking for keyboard interrupt to end program
            time.sleep(2)
    except KeyboardInterrupt:
        exit(0)

