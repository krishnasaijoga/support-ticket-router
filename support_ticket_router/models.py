from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TicketAction(BaseModel):
    """Actions required for a ticket."""
    action_type: str=Field(...,description='Action chosen by the agent')


class TicketObservation(BaseModel):
    """Observation fields for each ticket."""
    ticket_text: str=Field(...,description='Customer support Ticket text')
    customer_tier: str=Field(...,description='Customer tier. Eg. vip or regular')
    urgency: str=Field(...,description='urgency level. Eg. low, medium, high')
    message: str=Field(...,description='Environment Feedback message')


class TicketReward(BaseModel):
    "Reward signal for the ticket"
    reward:float=Field(...,ge=-1.0,le=1.0,description='Step reward')
    cumulative_score:float=Field(...,description='Running episode score')
    reason:str=Field(...,description='Why this reward was assigned')


class TicketState(BaseModel):
    """Ticket States"""
    ticket_id: str
    current_step: int
    assigned_team: Optional[str]=None
    escalated: bool=False
    resolved:bool=False
    score:float=0.0
    done:bool=False
    history:List[str]=Field(default_factory=list)


class StepInfo(BaseModel):
    """Additional Info returned from a step"""
    history:List[str]=Field(default_factory=list)
    error:Optional[str]=None
    expected_action:Optional[str]=None
    metadata:Dict[str,Any]=Field(default_factory=dict)


print("Types defined: Ticketaction, TicketObservation, TicketState")