# mon_bot_rasa/actions/__init__.py

from typing import Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Import de toutes les actions custom définies dans actions.py
from .actions import (
    ActionProposerDestinations,
    ActionRechercherHebergement,
    ActionInfosDestination,
    ActionComparerDestinations,
    ActionGererUrgences,
    ActionDemanderConseilsPratiques,
    ActionVerifierRestrictions
)

# Dictionnaire global pour enregistrer les actions (facultatif mais utile pour le debug)
actions_registry: Dict[Text, Any] = {
    "action_proposer_destinations": ActionProposerDestinations,
    "action_rechercher_hebergement": ActionRechercherHebergement,
    "action_infos_destination": ActionInfosDestination,
    "action_comparer_destinations": ActionComparerDestinations,
    "action_gerer_urgences": ActionGererUrgences,
    "action_demander_conseils_pratiques": ActionDemanderConseilsPratiques,
    "action_verifier_restrictions": ActionVerifierRestrictions
}

# Version alternative si vous préférez exporter directement les classes
__all__ = [
    'ActionProposerDestinations',
    'ActionRechercherHebergement',
    'ActionInfosDestination',
    'ActionComparerDestinations',
    'ActionGererUrgences',
    'ActionDemanderConseilsPratiques',
    'ActionVerifierRestrictions'
]

# Note : Ce fichier est optionnel dans Rasa 3.x+ mais recommandé pour :
# 1. Clarifier les imports
# 2. Centraliser la configuration des actions
# 3. Faciliter les tests unitaires