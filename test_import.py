import sys
from pathlib import Path

# Affiche tous les chemins où Python cherche les imports
print("=== Chemins Python ===")
print("\n".join(sys.path))

# Test d'import
try:
    from app.services.destination_service import une_fonction  # Remplacez par une vraie fonction/classe
    print("✅ Import réussi !")
except ImportError as e:
    print(f"❌ Erreur : {e}")