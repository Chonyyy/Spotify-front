import socket
import struct
import json
import time, logging

logger = logging.getLogger("__main__")

MULTICAST_GROUPS = {
    'gateway': '224.1.1.3',
}
MULTICAST_PORT = 5000
DISCOVERY_MESSAGE = "CHORD_DISCOVERY"

# Método para recibir mensajes multicast
def receive_multicast(role, timeout=10):
    multicast_group = MULTICAST_GROUPS.get(role)
    if not multicast_group:
        raise ValueError(f"Invalid role: {role}")
    
    logger.info(f'Receiving multicast messages from {multicast_group} for role {role}')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    
    mreq = struct.pack('4sl', socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    sock.settimeout(timeout)
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                message = json.loads(data.decode('utf-8'))
                logger.info("Estoy en el try")
                if message['message'] == DISCOVERY_MESSAGE and message['role'] == role:
                    logger.info(f"Discovered node: {addr[0]} with role: {message['role']}")
                    if message.get('leader_ip') and message.get('leader_id'):
                        logger.info(f"Detected leader: {message['leader_ip']}, {message['leader_id']}")
                        return addr, message  # Return IP and leader info
                    logger.info('addr'+ addr)
                    return addr, message
            except (json.JSONDecodeError, KeyError):
                logger.error(f"Received invalid discovery message: {data}")
    except socket.timeout:
        logger.info(f"No discovery message received within the timeout of {timeout} seconds.")
        return None, None
    finally:
        sock.close()

# Método para realizar el descubrimiento
def discover_gateway():
    retries = 2
    retry_interval = 5

    for _ in range(retries):
        multi_response = receive_multicast('gateway')
        discovered_ip = multi_response[0][0] if multi_response[0] else None
        if discovered_ip:
            logger.info(f"Discovered entry point: {discovered_ip}")
            return discovered_ip
        time.sleep(retry_interval)
    
    return None
