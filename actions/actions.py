from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import logging
import re

# Configure le logging pour déboguer les erreurs
logger = logging.getLogger(__name__)

class ActionProposerDestinations(Action):
    """Propose des destinations basées sur le thème ou la saison."""
    
    def name(self) -> Text:
        return "action_proposer_destinations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Récupère les slots pertinents
            theme = tracker.get_slot("theme")
            date = tracker.get_slot("date")
            budget = tracker.get_slot("budget")
            
            # Appel API au backend
            payload = {"theme": theme, "date": date}
            response = requests.post(
                "http://backend/api/destinations",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            
            destinations = response.json().get("destinations", ["Provence", "Bretagne"])  # Fallback
            dispatcher.utter_message(
                text=f"Je te recommande : {', '.join(destinations)}. Budget prévu ?"
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur API: {e}")
            dispatcher.utter_message(
                text="Service indisponible. Voici des idées : Provence, Bretagne, Croatie..."
            )
        return []

class ActionRechercherHebergement(Action):  # Nouvelle action
    def name(self) -> Text:
        return "action_rechercher_hebergement"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        nombre = tracker.get_slot("nombre")
        
        if not destination:
            dispatcher.utter_message(text="Vous n'avez pas précisé de destination.")
            return []

        dispatcher.utter_message(
            text=f"Je recherche des hébergements à {destination} pour {nombre} personnes..."
        )
        return []


class ActionInfosDestination(Action):
    """Récupère les infos détaillées sur une destination spécifique."""
    
    def name(self) -> Text:
        return "action_infos_destination"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Vous n'avez pas précisé de destination.")
            return []

        try:
            response = requests.get(
                f"http://backend/api/infos?destination={destination}",
                timeout=5
            )
            response.raise_for_status()
            
            infos = response.json()
            dispatcher.utter_message(
                text=f"Infos sur {destination} :\n{infos.get('description', 'Non disponible')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur: {e}")
            dispatcher.utter_message(
                text=f"Désolé, je n'ai pas pu récupérer les infos pour {destination}."
            )
        return []


class ActionComparerDestinations(Action):
    """Compare deux destinations sur des critères prédéfinis."""
    
    def name(self) -> Text:
        return "action_comparer_destinations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            dest1 = tracker.get_slot("destination1")
            dest2 = tracker.get_slot("destination2")
            
            if not dest1 or not dest2:
                dispatcher.utter_message(text="Vous devez préciser deux destinations à comparer.")
                return []

            response = requests.post(
                "http://backend/api/compare",
                json={"destination1": dest1, "destination2": dest2},
                timeout=5
            )
            response.raise_for_status()
            
            comparison = response.json()
            dispatcher.utter_message(
                text=f"Comparaison {dest1} vs {dest2} :\n{comparison.get('summary', 'Non disponible')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur: {e}")
            dispatcher.utter_message(
                text="Erreur lors de la comparaison. Essayez avec d'autres destinations."
            )
        return []


class ActionGererUrgences(Action):
    """Gère les requêtes liées aux urgences voyage."""
    
    def name(self) -> Text:
        return "action_gerer_urgences"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        try:
            response = requests.get(
                f"http://backend/api/urgences?destination={destination}",
                timeout=3  # Timeout court pour les urgences
            )
            response.raise_for_status()
            
            urgences = response.json()
            dispatcher.utter_message(
                text=f"Infos urgentes pour {destination} :\n"
                     f"- Urgences : {urgences.get('phone', '112')}\n"
                     f"- Ambassade : {urgences.get('embassy', 'Non disponible')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur urgences: {e}")
            dispatcher.utter_message(
                text=f"Contactez l'ambassade de France à {destination} en cas d'urgence."
            )
        return []


class ActionDemanderConseilsPratiques(Action):
    """Fournit des conseils pratiques (visa, santé, etc.)."""
    
    def name(self) -> Text:
        return "action_demander_conseils_pratiques"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        try:
            response = requests.get(
                f"http://backend/api/conseils?destination={destination}",
                timeout=5
            )
            response.raise_for_status()
            
            conseils = response.json()
            dispatcher.utter_message(
                text=f"Conseils pour {destination} :\n{conseils.get('advice', 'Non disponible')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur conseils: {e}")
            dispatcher.utter_message(
                text=f"Consultez le site diplomatie.gouv.fr pour {destination}."
            )
        return []


class ActionVerifierRestrictions(Action):
    """Vérifie les restrictions de voyage (COVID, visas, etc.)."""
    
    def name(self) -> Text:
        return "action_verifier_restrictions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        try:
            response = requests.get(
                f"http://backend/api/restrictions?destination={destination}",
                timeout=5
            )
            response.raise_for_status()
            
            restrictions = response.json()
            dispatcher.utter_message(
                text=f"Restrictions pour {destination} :\n{restrictions.get('rules', 'Aucune restriction')}"
            )
            
        except Exception as e:
            logger.error(f"Erreur restrictions: {e}")
            dispatcher.utter_message(
                text="Vérifiez les restrictions sur traveldoc.aero."
            )
        return []
 
class ActionValidateBudget(Action):
    def name(self) -> Text:
        return "action_validate_budget"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        budget = tracker.get_slot("budget")
        if not re.match(r'^[\d\s,.]+(€|\$|USD|CHF|euros?|dollars?)$', budget, flags=re.IGNORECASE):
            dispatcher.utter_message(text="Format invalide. Exemples valides : 500€, 1000 USD.")
            return [SlotSet("budget", None)]
        return []