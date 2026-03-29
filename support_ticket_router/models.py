from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# These would normally go in models.py

@dataclass
class TicketAction:
    """Actions required for a ticket."""
    action_type: str

@dataclass
class TicketObservation:
    """Observation fields for each ticket."""
    ticket_text: str
    customer_tier: str
    urgency: str
    message: str

@dataclass
class TicketState:
    """Ticket States."""
    ticket_id: str
    current_step: int
    assigned_team: Optional[str]=None
    escalated: bool=False
    resolved:bool=False
    score:float=0.0
    done:bool=False
    history:List[str]=field(default_factory=list)

print("Types defined: Ticketaction, TicketObservation, TicketState")