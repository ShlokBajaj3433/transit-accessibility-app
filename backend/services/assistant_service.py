import re
import random
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

# Mock environmental and location data
MOCK_ENVIRONMENT = {
    "location": "Toronto",
    "temperature": "20°C",
    "air_quality": "78 (Good)",
    "humidity": "90%",
    "co2_saved_week": "47.3 kg"
}

# Mock locations for navigation
MOCK_LOCATIONS = {
    "union station": {"lat": 43.6452, "lon": -79.3806, "display_name": "Union Station, Toronto"},
    "cn tower": {"lat": 43.6426, "lon": -79.3871, "display_name": "CN Tower, Toronto"},
    "downtown": {"lat": 43.6532, "lon": -79.3832, "display_name": "Downtown Toronto"},
    "airport": {"lat": 43.6777, "lon": -79.6248, "display_name": "Toronto Pearson Airport"},
    "subway station": {"lat": 43.6426, "lon": -79.3871, "display_name": "Nearest Subway Station"},
    "bus stop": {"lat": 43.6532, "lon": -79.3832, "display_name": "Main Bus Stop"},
    "shopping mall": {"lat": 43.6532, "lon": -79.3832, "display_name": "Eaton Centre"},
    "hospital": {"lat": 43.6568, "lon": -79.3908, "display_name": "Toronto General Hospital"},
    "university": {"lat": 43.6629, "lon": -79.3957, "display_name": "University of Toronto"},
    "library": {"lat": 43.6677, "lon": -79.3948, "display_name": "Toronto Public Library"},
    "my current location": {"lat": 43.6532, "lon": -79.3832, "display_name": "Your Current Location"},
    "here": {"lat": 43.6532, "lon": -79.3832, "display_name": "Current Location"},
    "shloka market": {"lat": 43.6500, "lon": -79.3850, "display_name": "Shloka Market Bus Stop"}
}

# Conversation state tracker
conversation_states = {}

async def process_assistant_query(text: str, openai_client=None) -> Dict[str, Any]:
    """Process natural language transit query with Sara conversation flow."""
    
    # Initialize conversation if first interaction or if explicitly requested
    if (not conversation_states.get("current_state") or 
        text.lower().strip() in ['initialize', 'init', 'start']):
        return initialize_sara_conversation()
    
    # Get current state
    state = conversation_states.get("current_state", "intro")
    user_input = text.lower().strip()
    
    # Handle different conversation stages
    if state == "intro":
        return handle_destination_request(text)
    elif state == "awaiting_transport":
        return handle_transport_selection(text)
    elif state == "awaiting_preferences":
        return handle_preferences(text)
    elif state == "ready_to_start":
        return handle_journey_start(text)
    elif state == "journey_active":
        return handle_journey_updates(text)
    elif state == "at_bus_stop":
        return handle_bus_arrival(text)
    elif state == "on_bus":
        return handle_bus_journey(text)
    elif state == "walking_to_destination":
        return handle_final_walking(text)
    else:
        # Reset and start over
        return initialize_sara_conversation()

def initialize_sara_conversation() -> Dict[str, Any]:
    """Initialize conversation with Sara introduction."""
    conversation_states["current_state"] = "intro"
    conversation_states["origin"] = None
    conversation_states["destination"] = None
    conversation_states["transport"] = None
    conversation_states["selected_route"] = None
    
    response = f"""Hi this is "Sara"... your AI Agent..

You are in {MOCK_ENVIRONMENT["location"]}.

The temperature is {MOCK_ENVIRONMENT["temperature"]}. Air quality index is {MOCK_ENVIRONMENT["air_quality"]}. Humidity is {MOCK_ENVIRONMENT["humidity"]}.

You've saved {MOCK_ENVIRONMENT["co2_saved_week"]} of CO₂ this week..

Where do you want to go?"""
    
    return {
        "response": response,
        "data": {"state": "intro", "environment": MOCK_ENVIRONMENT}
    }

def handle_destination_request(text: str) -> Dict[str, Any]:
    """Handle user's destination request."""
    origin, destination = extract_locations(text)
    
    if not origin or not destination:
        return {
            "response": "I didn't catch that. Please tell me where you want to go from and to. For example: 'I want to go from Union Station to CN Tower'",
            "data": {"state": "intro"}
        }
    
    # Store the route
    conversation_states["origin"] = origin
    conversation_states["destination"] = destination
    conversation_states["current_state"] = "awaiting_transport"
    
    response = f"""Okay! You want to go from {origin} to {destination}. Which type of transport would you like to take?

You can choose Bus, Train, or MRT/LRT."""
    
    return {
        "response": response,
        "data": {"state": "awaiting_transport", "origin": origin, "destination": destination}
    }

def handle_transport_selection(text: str) -> Dict[str, Any]:
    """Handle transport type selection."""
    transport_type = extract_transport_type(text)
    
    if not transport_type:
        return {
            "response": "Please choose a transport type: Bus, Train, or MRT/LRT.",
            "data": {"state": "awaiting_transport"}
        }
    
    conversation_states["transport"] = transport_type
    conversation_states["current_state"] = "awaiting_preferences"
    
    # Generate mock route options
    routes = generate_mock_routes(transport_type)
    
    response = f"""Here are the suggested routes for {transport_type} transport...

Route 1: 5.8 kilometers, estimated travel time 24 minutes. You will arrive at 8:38 PM. Cost is $1.50. CO₂ saved compared to driving: 1.2 kg.

Route 2: 6.2 kilometers, estimated travel time 22 minutes. You will arrive at 8:36 PM. Cost is $1.20. CO₂ saved: 1.0 kg.

Route 3: 5.5 kilometers, estimated travel time 26 minutes. You will arrive at 8:40 PM. Cost is $1.80. CO₂ saved: 1.3 kg.

Do you want me to recommend routes that save more CO₂, or cheaper routes, or do you have any preferences like departure time?"""
    
    return {
        "response": response,
        "data": {"state": "awaiting_preferences", "routes": routes}
    }

def handle_preferences(text: str) -> Dict[str, Any]:
    """Handle user preferences for route selection."""
    conversation_states["current_state"] = "ready_to_start"
    
    # Parse user preferences
    if "eco" in text.lower() or "co2" in text.lower() or "environment" in text.lower():
        selected_route = "Route 3 (Most Eco-friendly)"
    elif "cheap" in text.lower() or "cost" in text.lower():
        selected_route = "Route 2 (Most Economical)"
    else:
        selected_route = "Route 1 (Balanced)"
    
    conversation_states["selected_route"] = selected_route
    
    response = f"""Got it! You want an eco-friendly route with less walking. For {conversation_states["transport"]} transport, the most eco-friendly option with minimal walking is Route 3.

Distance: 5.5 kilometers
Estimated travel time: 26 minutes
Arrival time: 8:26 PM
Cost: $1.80
CO₂ saved: 1.3 kg
Walking distance: 300 meters from current location to bus stop, 100 meters from stop to destination.

Would you like me to start navigation now?"""
    
    return {
        "response": response,
        "data": {"state": "ready_to_start", "selected_route": selected_route}
    }

def handle_journey_start(text: str) -> Dict[str, Any]:
    """Handle journey start confirmation."""
    if "start" in text.lower() or "okay" in text.lower() or "yes" in text.lower():
        conversation_states["current_state"] = "journey_active"
        
        response = """Final confirmation before starting the journey...

You will be walking to Shloka Market bus stop from 8:00 PM to 8:08 PM, approximately 300 meters.

At 8:10 PM, the bus will arrive. You will take it to the 3rd stop, then continue directly to your destination.

Estimated bus travel time: 18 minutes. You will arrive at your destination at 8:26 PM.

Total distance: 5.5 kilometers. Cost: $1.80. Walking distance: 400 meters total.

This route produces 38% less emissions and avoids poor air quality. You save 1.3kg CO₂ using this route..

Starting Journey....

The journey has been started... Start by walking to Shloka Market bus stop at 8:00 PM. It should take about 8 minutes to walk there."""
        
        return {
            "response": response,
            "data": {"state": "journey_active", "step": "walking_to_bus_stop"}
        }
    else:
        return {
            "response": "Let me know when you're ready to start the journey. Just say 'start journey' or 'okay'.",
            "data": {"state": "ready_to_start"}
        }

def handle_journey_updates(text: str) -> Dict[str, Any]:
    """Handle real-time journey updates."""
    user_input = text.lower()
    
    if "shloka market" in user_input or "bus stop" in user_input:
        conversation_states["current_state"] = "at_bus_stop"
        
        response = """Perfect! You're at Shloka Market bus stop.

Please wait... The bus will arrive at 8:10 PM. It is about 100 meters away from your current location."""
        
        return {
            "response": response,
            "data": {"state": "at_bus_stop"}
        }
    else:
        return {
            "response": "Keep walking towards Shloka Market bus stop. You're making good progress!",
            "data": {"state": "journey_active"}
        }

def handle_bus_arrival(text: str) -> Dict[str, Any]:
    """Handle bus arrival and boarding."""
    user_input = text.lower()
    
    if "bus is here" in user_input or "bus arrived" in user_input:
        conversation_states["current_state"] = "on_bus"
        
        response = """Great! Now board the bus and have a seat. Wait for 3 stops to reach your destination area.

We are tracking your stops now..."""
        
        # Simulate tracking after a few seconds
        return {
            "response": response,
            "data": {"state": "on_bus", "stops_remaining": 3}
        }
    else:
        return {
            "response": "The bus should be arriving any moment now at 8:10 PM. Please wait at the bus stop.",
            "data": {"state": "at_bus_stop"}
        }

def handle_bus_journey(text: str) -> Dict[str, Any]:
    """Handle updates while on the bus."""
    user_input = text.lower()
    
    if "got down" in user_input or "off the bus" in user_input or "exited" in user_input:
        conversation_states["current_state"] = "walking_to_destination"
        
        response = """Excellent! Tracking your current location...

Great, now walk 100 meters towards the left and your destination will be on your right.

We are tracking your steps while you're walking..."""
        
        return {
            "response": response,
            "data": {"state": "walking_to_destination"}
        }
    else:
        # Simulate bus tracking
        response = """The next stop is your destination stop. Please ring the bell now and get ready to exit the bus."""
        
        return {
            "response": response,
            "data": {"state": "on_bus", "next_action": "prepare_to_exit"}
        }

def handle_final_walking(text: str) -> Dict[str, Any]:
    """Handle final walking to destination."""
    user_input = text.lower()
    
    if "thank you" in user_input or "end journey" in user_input or "arrived" in user_input:
        conversation_states["current_state"] = "completed"
        
        response = """You're very welcome! We are ending the journey now.

Journey Summary:
- Total travel time: 26 minutes
- CO₂ saved: 1.3 kg
- Total cost: $1.80
- You arrived safely at your destination!

Have a wonderful day! Feel free to ask me for navigation help anytime."""
        
        # Reset conversation state
        conversation_states.clear()
        
        return {
            "response": response,
            "data": {"state": "completed", "journey_ended": True}
        }
    else:
        # Simulate final approach
        response = """Keep walking... you're almost there!

Great! You are now at your destination. It should be on your right. You've successfully completed your journey!"""
        
        return {
            "response": response,
            "data": {"state": "walking_to_destination", "near_destination": True}
        }

def extract_transport_type(text: str) -> Optional[str]:
    """Extract transport type from user input."""
    text = text.lower()
    if "bus" in text:
        return "Bus"
    elif "train" in text:
        return "Train"
    elif "mrt" in text or "lrt" in text:
        return "MRT/LRT"
    return None

def generate_mock_routes(transport_type: str) -> list:
    """Generate mock route options."""
    base_time = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
    
    routes = [
        {
            "id": 1,
            "distance": "5.8 km",
            "duration": "24 minutes",
            "arrival": (base_time + timedelta(minutes=38)).strftime("%I:%M %p"),
            "cost": "$1.50",
            "co2_saved": "1.2 kg"
        },
        {
            "id": 2,
            "distance": "6.2 km", 
            "duration": "22 minutes",
            "arrival": (base_time + timedelta(minutes=36)).strftime("%I:%M %p"),
            "cost": "$1.20",
            "co2_saved": "1.0 kg"
        },
        {
            "id": 3,
            "distance": "5.5 km",
            "duration": "26 minutes", 
            "arrival": (base_time + timedelta(minutes=40)).strftime("%I:%M %p"),
            "cost": "$1.80",
            "co2_saved": "1.3 kg"
        }
    ]
    return routes

def extract_locations(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract origin and destination from natural language."""
    text = text.lower().strip()
    
    # Pattern: "from X to Y"
    pattern1 = r'from\s+(.+?)\s+to\s+(.+?)(?:\.|$|\?|\s*$)'
    match = re.search(pattern1, text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Pattern: "I want to go from X to Y"
    pattern2 = r'go from\s+(.+?)\s+to\s+(.+?)(?:\.|$|\?|\s*$)'
    match = re.search(pattern2, text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Pattern: "start journey to Y" / "navigate to Y"
    pattern3 = r'(?:start journey to|navigate to|go to)\s+(.+?)(?:\.|$|\?|\s*$)'
    match = re.search(pattern3, text)
    if match:
        return "my current location", match.group(1).strip()
    
    # Pattern: "X to Y"
    pattern4 = r'^(.+?)\s+to\s+(.+?)(?:\.|$|\?|\s*$)'
    match = re.search(pattern4, text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    return None, None