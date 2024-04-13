# CosmonarchyMatchMaker (CMMM)
## Design Explanation

### Server
- Accepts websocket connections from clients and maintains a list of currently connected clients.
- Each time this list is updated, (new client added or old client removed), the server sends the updated list to all clients still connected.

### Client
- The client connects to the server to be added to the client list and in return receives an updated list of peers.
- Every 2 seconds the client sends a CM solicitation message on ports 6111&6112 (see [Design.md](Design.md))
    - this triggers peers with open lobbies to reply with map announcements and also serves as UDP hole punch for NAT Traversal (hopefully no port forward required typically)
        - further testing required
