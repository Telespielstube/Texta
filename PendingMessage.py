class PendingMessageTable:

    def __init__(self, pending_message=None, retry=None):
        self.pending_message = pending_message
        self.retry = retry
    # Compares pending_message_list message destination and routing table destination esntry for matches.
    # @return     list with matching messages
    def get_pending_message(self, pending_message_list, routing_table):
        match = [pending_message_list.index(entry.destination) for entry in routing_table.search_entry(entry.destination)]
        return match
        # match = Queue()
        # # for entry in pending_message_list:   
        # #     if routing_table.search_entry(entry.pending_message.destination) is entry.message.destination:
        # #          match.put(entry)
        # #          continue
        #     return match

    def add_retry(self, pending_message_list):
        for entry in pending_message_list:
            entry.destination +=1
                    
     def delete_peding_message(self, pending_message_list):
         for entry in pending_message_list:
             if entry.retry == 3:
                 pending_message_list.remove(entry)