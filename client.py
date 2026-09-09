"""
Autonomous Agent Chord DHT Protocol Skill
Pure Python Standard Library implementation.
"""
from typing import List, Dict, Optional, Any

class ChordNode:
    """
    Chord circular DHT node with finger table routing.
    """
    def __init__(self, node_id: int, m_bits: int = 6):
        self.id = node_id
        self.m = m_bits
        self.size = 1 << m_bits
        self.finger = [node_id] * m_bits
        self.successor = node_id

    def update_finger_table(self, all_nodes_sorted: List[int]):
        for i in range(self.m):
            start = (self.id + (1 << i)) % self.size
            succ = all_nodes_sorted[0]
            for n in all_nodes_sorted:
                if n >= start:
                    succ = n
                    break
            self.finger[i] = succ
        self.successor = self.finger[0]

    def find_successor(self, target_id: int) -> int:
        if self.id < self.successor:
            if self.id < target_id <= self.successor:
                return self.successor
        else:
            if target_id > self.id or target_id <= self.successor:
                return self.successor

        for i in reversed(range(self.m)):
            f = self.finger[i]
            if self.id < target_id:
                if self.id < f < target_id:
                    return f
            else:
                if f > self.id or f < target_id:
                    return f
        return self.successor
