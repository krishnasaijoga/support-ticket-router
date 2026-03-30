from typing import Dict, Any
from support_ticket_router.models import TicketAction, TicketObservation, TicketState

VALID_ACTIONS = [
    "assign_billing",
    "assign_technical",
    "assign_shipping",
    "request_more_info",
    "escalate",
    "resolve"
]

TASKS = {
    "easy": {
        "ticket_id": "T1",
        "ticket_text": "My payment failed but money was deducted.",
        "customer_tier": "regular",
        "urgency": "medium",
        "correct_flow": ["assign_billing", "resolve"]
    },
    "medium": {
        "ticket_id": "T2",
        "ticket_text": "I am unable to log into my account after resetting password.",
        "customer_tier": "regular",
        "urgency": "medium",
        "correct_flow": ["assign_technical", "resolve"]
    },
    "hard": {
        "ticket_id": "T3",
        "ticket_text": "I am a VIP customer. Payment failed, money deducted, and this is urgent.",
        "customer_tier": "vip",
        "urgency": "high",
        "correct_flow": ["assign_billing", "escalate", "resolve"]
    },
      "extra_hard":{
        "ticket_id":"T4",
        "ticket_text":"My payment failed and now I cannot access my account",
        "customer_tier":"regular",
        "urgency":"high",
        "correct_flow":["assign_billing","assign_technical","resolve"]
    },
    "hard_missing_info":{
      "ticket_id":"T5",
      "ticket_text":"Something is wrong with my order",
      "customer_tier":"regular",
      "urgency":"low",
      "correct_flow":["request_more_info","assign_shipping","resolve"]
    },
    "vip_priority":{
      "ticket_id":"T6",
      "ticket_text":"I am a VIP customer. My order is delayed.",
      "customer_tier":"vip",
      "urgency":"high",
      "correct_flow":["assign_billing","assign_shipping","resolve"]
    },
    "repeat_failure":{
      "ticket_id":"T7",
      "ticket_text":"This is third time my payment failed. Please fix urgently.",
      "customer_tier":"regular",
      "urgency":"high",
      "correct_flow":["assign_billing","escalate","resolve"]
    }
}

class SupportTicketRouterEnv:
    """A letter-guessing game environment following the OpenEnv pattern."""

    def __init__(self,tasks:Dict[str,Dict[str,Any]]):
        self.tasks=tasks
        self.current_task = None
        self.state_data = None

    def reset(self,task_name:str='easy') -> TicketObservation:
        """Start with an easy task."""
        task=self.tasks[task_name]
        self.current_task = task
        self.state_data = TicketState(
            ticket_id=task['ticket_id'],
            current_step=0,
            assigned_team=None,
            escalated=False,
            resolved=False,
            score=0.0,
            done=False,
            history=[]
        )
        observation=TicketObservation(
            ticket_text=task['ticket_text'],
            customer_tier=task['customer_tier'],
            urgency=task['urgency'],
            message='New ticket recieved. Choose next action.'
        )
        return observation
    def step(self,action:TicketAction):
      if self.state_data is None:
        raise ValueError('Environment is not reset. Call reset(), then take a step.')
      if self.state_data.done:
        return (TicketObservation(
            ticket_text=self.current_task['ticket_text'], # type: ignore
            customer_tier=self.current_task['customer_tier'], # pyright: ignore[reportOptionalSubscript]
            urgency=self.current_task['urgency'], # pyright: ignore[reportOptionalSubscript]
            message='Episode already finished.'
        ),0.0,True,{'error':'Episode already done'})
      action_type=action.action_type
      if action_type not in VALID_ACTIONS:
        observation=TicketObservation(
            ticket_text=self.current_task['ticket_text'], # pyright: ignore[reportOptionalSubscript]
            customer_tier=self.current_task['customer_tier'], # pyright: ignore[reportOptionalSubscript]
            urgency=self.current_task['urgency'], # pyright: ignore[reportOptionalSubscript]
            message=f'invalid action type: {action_type}'
        )
        return observation, -1.0,False, {'error':'Invalid action'}
      correct_flow=self.current_task['correct_flow'] # pyright: ignore[reportOptionalSubscript]
      current_step=self.state_data.current_step
      reward=0.0
      message=''
      self.state_data.history.append(action_type)
      if current_step<len(correct_flow) and action_type==correct_flow[current_step]:
        reward=1.0
        message=f"Correct action: {action_type}"
        if action_type == "assign_billing":
          self.state_data.assigned_team = "billing"
        elif action_type == "assign_technical":
          self.state_data.assigned_team = "technical"
        elif action_type == "assign_shipping":
          self.state_data.assigned_team = "shipping"
        elif action_type == "escalate":
          self.state_data.escalated = True
        elif action_type == "resolve":
          self.state_data.resolved = True
        self.state_data.current_step+=1
        self.state_data.score+=reward

        if action_type=='escalate' and self.current_task['urgency']=='high': # pyright: ignore[reportOptionalSubscript]
          reward+=0.5
        
        if self.state_data.current_step==len(correct_flow):
          self.state_data.done=True
          reward=+1
          self.state_data.score+=1
          message=f"Task completed successfully with action: {action_type}"
      else:
        reward=-0.5
        message=f'Wrong action type: {action_type}'
        self.state_data.score+=reward
      observation=TicketObservation(
          ticket_text=self.current_task['ticket_text'], # pyright: ignore[reportOptionalSubscript]
          customer_tier=self.current_task['customer_tier'], # pyright: ignore[reportOptionalSubscript]
          urgency=self.current_task['urgency'], # pyright: ignore[reportOptionalSubscript]
          message=message
      )
      return observation, reward, self.state_data.done, {'history':self.state_data.history}
    @property
    def state(self)->TicketState:
      if self.state_data is None:
        raise ValueError('Environment not reset. Call reset() first.')
      return self.state_data    
    
    # def _mask(self) -> str:
    #     """Show guessed letters, hide the rest."""
    #     return "".join(c if c in self._guessed else "_" for c in self._target)

print("SupportTicketRouterEnv defined.")