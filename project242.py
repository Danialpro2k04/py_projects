from segment import Segment, PacketType
from unreliable_channel import UnreliableChannel
import time


class RDTLayer:
    MAX_PAYLOAD_SIZE = 1024
    WINDOW_SIZE = 4
    TIMEOUT = 5

    def __init__(self, unreliable_channel):
        self.uc = unreliable_channel
        self.segments_to_send = []
        self.segments_sent = {}
        self.segments_received = {}
        self.next_seq_num = 0
        self.expected_seq_num = 0
        self.window_start = 0

    def process_send(self, data):
        # Split data into segments
        data_segments = [data[i:i+self.MAX_PAYLOAD_SIZE]
                         for i in range(0, len(data), self.MAX_PAYLOAD_SIZE)]
        # Create segments with sequence numbers and add to list
        for i, segment_data in enumerate(data_segments):
            segment = Segment(self.next_seq_num + i,
                              segment_data, PacketType.DATA)
            self.segments_to_send.append(segment)
        # Send segments up to window size
        while self.next_seq_num < self.window_start + self.WINDOW_SIZE and self.next_seq_num < len(data_segments):
            self.send_segment(self.segments_to_send[self.next_seq_num])
            self.segments_sent[self.next_seq_num] = time.time()
            self.next_seq_num += 1

    def process_receive_and_send_respond(self):
        # Receive segment from unreliable channel
        segment = self.uc.receive()
        if segment:
            if segment.packet_type == PacketType.DATA:
                # Check if segment is in window
                if segment.seq_num >= self.expected_seq_num and segment.seq_num < self.expected_seq_num + self.WINDOW_SIZE:
                    # If segment is the expected segment, deliver data to upper layer
                    if segment.seq_num == self.expected_seq_num:
                        self.deliver_data(segment.payload)
                        self.expected_seq_num += 1
                        # Check if there are any segments in received buffer that can be delivered now
                        while self.expected_seq_num in self.segments_received:
                            self.deliver_data(
                                self.segments_received[self.expected_seq_num])
                            del self.segments_received[self.expected_seq_num]
                            self.expected_seq_num += 1
                    # Otherwise, buffer segment and send cumulative ack
                    else:
                        self.segments_received[segment.seq_num] = segment.payload
                    ack = Segment(segment.seq_num, '', PacketType.ACK)
                    self.send_segment(ack)
                # If segment is outside of window, send cumulative ack with previous sequence number
                elif segment.seq_num >= self.window_start and segment.seq_num < self.expected_seq_num:
                    ack = Segment(self.expected_seq_num -
                                  1, '', PacketType.ACK)
                    self.send_segment(ack)
            elif segment.packet_type == PacketType.ACK:
                # Update window start and remove acknowledged segments from sent buffer
                if segment.seq_num >= self.window_start:
                    self.window_start = segment.seq_num + 1
                    for seq_num in range(self.window_start):
                        if seq_num in self.segments_sent:
                            del self.segments_sent[seq_num]
                # If received segment has already been acknowledged, re-send cumulative ack
                else:
                    ack = Segment(self.expected_seq_num -
                                  1, '', PacketType.ACK)
                    self.send_segment(ack)

        # Check for timed out segments and re-send
        for seq_num, timestamp in self.segments_sent.items():
            if time.time() - timestamp > self.TIMEOUT:
                self.send_segment(self.segments_to_send[seq_num])
                self.segments_sent[seq_num] = time.time()

    def send_segment(self, segment):
        self.uc.send(segment)
