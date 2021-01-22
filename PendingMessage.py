class PendingMessageTable:

    def __init__(self, pending_message=None, retry=None):
        self.pending_message = pending_message
        self.retry = retry

    def get_pending_message(self, pending_message_list, routing_table):
        for entry in pending_message_list:   
            if routing_table.search_entry(entry.pending_message.destination) is entry.message.destination:
                 match = entry
            return match