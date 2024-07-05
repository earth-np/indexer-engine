curl https://sepolia.base.org \
-X POST \
-H "Content-Type: application/json" \
-d '[{"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []},
{"jsonrpc": "2.0", "id": 2, "method": "eth_blockNumber", "params": []},
{"jsonrpc": "2.0", "id": 3, "method": "eth_blockNumber", "params": []},
{"jsonrpc": "2.0", "id": 4, "method": "eth_blockNumber", "params": []}]'