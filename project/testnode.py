from TcpServerNode import *

node = None # global variable

def callbackNodeEvent(event, node, other, data):
   print("Event Node 1 (" + node.id + "): %s: %s" % (event, data))
   node.send_to_nodes({"thank": "you"})

node = Node('localhost', 9998, callbackNodeEvent)

node.start()

node.connect_with_node('localhost', 9999)

node.terminate_flag.set() # Stopping the thread

node.send_to_nodes({"type": "message", "message": "test"})

while True:
    time.sleep(1)

node.stop()
node.join()
