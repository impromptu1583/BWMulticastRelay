# BWMulticastRelay

## CM Wan Matchmaker
This tool allows players hosting games to make those games visible across a WAN connection using port forwarding.

### Usage
All players need to forward ports 6111 & 6112 to the computers they will be playing on

The player hosting the game creates a LAN/UDP game and runs `python .\cm_wan_matchmaker.py` and enters the WAN/external IP addresses of each player who will be joining (up to 7 add'l players) and presses 'start'. Typically leaving the host IP as localhost (127.0.0.1) should be fine.

The app will then begin sending CM game solicitations with the 'origin' addresses spoofed to the player addresses. This will trigger CM to send game announcements back to those players. They game should show up in thier CM client under "LAN"
