from typing import Optional, Union, Dict, Any
import re

def is_valid_message(message: Optional[Union[str, bytes]]) -> bool:
    """Valide qu'un message est non-vide et sécurisé.
    
    Args:
        message: Chaîne ou bytes à valider
        
    Returns:
        bool: True si le message est valide
    """
    if not message:
        return False
    if isinstance(message, bytes):
        try:
            message = message.decode('utf-8')
        except UnicodeDecodeError:
            return False
    
    message = str(message).strip()
    return (len(message) > 0 
            and len(message) <= 2000 
            and not contains_malicious_code(message))

def contains_malicious_code(text: str) -> bool:
    """Détecte des motifs potentiellement dangereux."""
    patterns = [
        r"<script>",
        r"DROP TABLE",
        r"DELETE FROM",
        r"--"
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

def sanitize_input(data: Union[str, Dict[str, Any]]) -> Union[str, Dict[str, Any]]:
    """Nettoie les entrées utilisateur."""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    return str(data).strip() if data else ""