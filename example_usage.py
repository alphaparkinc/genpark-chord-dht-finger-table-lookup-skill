"""Example usage for Chord DHT Skill."""
from client import ChordNode

def main():
    print("Executing Chord DHT...")
    cluster_nodes = [1, 12, 32, 45]
    node1 = ChordNode(1, m_bits=6)
    node1.update_finger_table(cluster_nodes)

    succ = node1.find_successor(10)
    print("Successor of key 10:", succ)
    assert succ == 12
    print("Chord DHT verified successfully!")

if __name__ == "__main__":
    main()
