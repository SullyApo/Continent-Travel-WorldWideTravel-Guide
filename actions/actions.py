from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ConversationPaused
import requests
import logging
import re
from datetime import datetime

# Configuration du logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# URL de base de l'API backend
BACKEND_API_URL = "http://backend:8000"

class ActionProposerDestinations(Action):
    def name(self) -> Text:
        return "action_proposer_destinations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            params = {
                "theme": tracker.get_slot("theme"),
                "budget": tracker.get_slot("budget"),
                "date": tracker.get_slot("date"),
                "duree": tracker.get_slot("duree")
            }
            
            response = requests.get(
                f"{BACKEND_API_URL}/api/destinations",
                params={k: v for k, v in params.items() if v is not None},
                timeout=5
            )
            response.raise_for_status()
            
            destinations = response.json().get("destinations", [])
            if destinations:
                message = "Voici mes recommandations : " + ", ".join(destinations[:5])
            else:
                message = "Aucune destination trouvée avec ces critères."
                
        except Exception as e:
            logger.error(f"Erreur API destinations: {str(e)}")
            message = "Je n'ai pas pu accéder aux recommandations. Essayez avec d'autres critères."
        
        dispatcher.utter_message(text=message)
        return []

class ActionRechercherHebergement(Action):
    def name(self) -> Text:
        return "action_rechercher_hebergement"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Veuillez préciser une destination.")
            return []

        try:
            params = {
                "destination": destination,
                "nombre": tracker.get_slot("nombre"),
                "theme": tracker.get_slot("theme")
            }
            
            response = requests.get(
                f"{BACKEND_API_URL}/api/hebergements",
                params={k: v for k, v in params.items() if v is not None},
                timeout=5
            )
            response.raise_for_status()
            
            hebergements = response.json().get("hebergements", [])
            if hebergements:
                message = f"Options à {destination} : " + ", ".join(h["nom"] for h in hebergements[:3])
            else:
                message = f"Aucun hébergement trouvé à {destination}."
                
        except Exception as e:
            logger.error(f"Erreur API hébergements: {str(e)}")
            message = f"Erreur lors de la recherche à {destination}."
        
        dispatcher.utter_message(text=message)
        return [SlotSet("derniere_recherche", datetime.now().isoformat())]

class ActionComparerDestinations(Action):
    def name(self) -> Text:
        return "action_comparer_destinations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dest1, dest2 = tracker.get_slot("destination1"), tracker.get_slot("destination2")
        if not dest1 or not dest2:
            dispatcher.utter_message(text="Veuillez préciser deux destinations à comparer.")
            return []

        try:
            response = requests.post(
                f"{BACKEND_API_URL}/api/voyages/compare",
                json={"destination1": dest1, "destination2": dest2},
                timeout=5
            )
            response.raise_for_status()
            
            comparison = response.json()
            message = comparison.get("message", 
                f"Comparaison entre {dest1} et {dest2}:\n" +
                f"- Meilleure destination plage: {comparison.get('plage', 'N/A')}\n" +
                f"- Meilleure destination culture: {comparison.get('culture', 'N/A')}")
                
        except Exception as e:
            logger.error(f"Erreur API comparaison: {str(e)}")
            message = f"Comparaison impossible entre {dest1} et {dest2}."
        
        dispatcher.utter_message(text=message)
        return []

class ActionGererUrgences(Action):
    def name(self) -> Text:
        return "action_gerer_urgences"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Veuillez préciser une destination.")
            return []

        try:
            response = requests.get(
                f"{BACKEND_API_URL}/api/urgences",
                params={"destination": destination},
                timeout=3
            )
            response.raise_for_status()
            
            infos = response.json()
            message = (
                f"Urgences à {destination}:\n"
                f"- Police: {infos.get('police', '112/911')}\n"
                f"- Ambassade: {infos.get('embassy', 'Non disponible')}\n"
                f"- Hôpitaux: {infos.get('hopitaux', 'Non disponible')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur API urgences: {str(e)}")
            message = f"Contactez l'ambassade française à {destination} en cas d'urgence."
        
        dispatcher.utter_message(text=message)
        return []

class ActionValidateBudget(Action):
    def name(self) -> Text:
        return "action_validate_budget"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        budget = tracker.get_slot("budget")
        if not budget or not re.match(r'^[\d\s,.]+(€|\$|USD|CHF|EUR|euros?|dollars?)$', budget, re.IGNORECASE):
            dispatcher.utter_message(text="Format de budget invalide. Ex: 500€ ou 1000 USD")
            return [SlotSet("budget", None)]
        return []

class ActionVerifierRestrictions(Action):
    def name(self) -> Text:
        return "action_verifier_restrictions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Veuillez préciser une destination.")
            return []

        try:
            response = requests.get(
                f"{BACKEND_API_URL}/api/restrictions",
                params={"destination": destination},
                timeout=5
            )
            response.raise_for_status()
            
            restrictions = response.json()
            message = (
                f"Restrictions pour {destination}:\n"
                f"- Visa: {restrictions.get('visa', 'Non requis')}\n"
                f"- Vaccins: {restrictions.get('vaccins', 'Aucun')}\n"
                f"- COVID: {restrictions.get('covid', 'Aucune restriction')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur API restrictions: {str(e)}")
            message = f"Impossible de vérifier les restrictions pour {destination}."
        
        dispatcher.utter_message(text=message)
        return []

class ActionDemanderConseilsPratiques(Action):
    def name(self) -> Text:
        return "action_demander_conseils_pratiques"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Veuillez préciser une destination.")
            return []

        try:
            response = requests.get(
                f"{BACKEND_API_URL}/api/conseils",
                params={"destination": destination},
                timeout=5
            )
            response.raise_for_status()
            
            conseils = response.json()
            message = (
                f"Conseils pour {destination}:\n"
                f"- Devise: {conseils.get('devise', 'Non spécifié')}\n"
                f"- Adaptateur: {conseils.get('adaptateur', 'Non spécifié')}\n"
                f"- Sécurité: {conseils.get('securite', 'Standard')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur API conseils: {str(e)}")
            message = f"Impossible de récupérer les conseils pour {destination}."
        
        dispatcher.utter_message(text=message)
        return []

class ActionSaveConversation(Action):
    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            requests.post(
                f"{BACKEND_API_URL}/api/conversations",
                json={
                    "user_id": tracker.sender_id,
                    "conversation": list(tracker.events),
                    "timestamp": datetime.now().isoformat()
                },
                timeout=2
            )
        except Exception as e:
            logger.error(f"Erreur sauvegarde conversation: {str(e)}")
        
        return []

class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_rephrase")
        return []