"""MCP Server for Chord DHT Skill."""
import json
import sys
from client import ChordNode

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "lookup_chord_successor",
                            "description": "Find successor node for key using Chord finger table",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "node_id": {"type": "integer"},
                                    "all_nodes": {"type": "array", "items": {"type": "integer"}},
                                    "key": {"type": "integer"},
                                    "m_bits": {"type": "integer"}
                                },
                                "required": ["node_id", "all_nodes", "key"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                c = ChordNode(args["node_id"], args.get("m_bits", 6))
                c.update_finger_table(sorted(args["all_nodes"]))
                s = c.find_successor(args["key"])
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps({"successor_node": s})}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
