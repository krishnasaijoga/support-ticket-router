from support_ticket_router.models import TicketAction, TicketObservation, TicketState

def baseline_policy(observation:TicketObservation,state:TicketState)->TicketAction:
  text=observation.ticket_text.lower()
  tier=observation.customer_tier.lower()
  urgency=observation.urgency.lower()
  history=state.history

  if state.resolved:
    return TicketAction('resolve')
  if "something is wrong" in text and 'request_more_info' not in history:
    return TicketAction('request_more_info')
  
  if state.assigned_team is None:
    if "payment" in text or "money deducted" in text or "charged" in text:
      return TicketAction("assign_billing")
    if "login" in text or "password" in text or "account" in text:
      return TicketAction("assign_technical")
    if "delivery" in text or "shipping" in text or "order" in text:
      return TicketAction("assign_shipping")
  
  if state.assigned_team == "billing":
    if ("account" in text or "login" in text or "password" in text) and "assign_technical" not in history:
      return TicketAction("assign_technical")
    if urgency == "high" and not state.escalated and (tier == "vip" or "urgent" in text or "third time" in text):
      return TicketAction("escalate")
    return TicketAction("resolve")
  
  if state.assigned_team == "shipping":
    if urgency == "high" and not state.escalated and tier == "vip":
      return TicketAction("escalate")
    return TicketAction("resolve")
  
  if state.assigned_team == "technical":
    return TicketAction("resolve")
  
  if "request_more_info" in history and "order" in text and "assign_shipping" not in history:
    return TicketAction("assign_shipping")
  
  if urgency == "high" and not state.escalated and (tier == "vip" or "third time" in text):
    return TicketAction("escalate")
  return TicketAction('resolve')

  # if tier=="vip" and urgency=='high':
  #   if "payment" in text and "assign_billing" not in history:
  #     return TicketAction('assign_billing')
  #   elif ("order" in text or "delivery" in text) and "assign_shipping" not in history:
  #     return TicketAction('assign_shipping')
  #   else:
  #     return TicketAction('escalate')
  
  # if state.assigned_team == "technical":
  #       return TicketAction("resolve")
  # if state.assigned_team == "shipping":
  #   if urgency == "high" and not state.escalated and tier == "vip":
  #       return TicketAction("escalate")
  #   return TicketAction("resolve")
  # if "request_more_info" in history and "order" in text and "assign_shipping" not in history:
  #       return TicketAction("assign_shipping")
  # if urgency == "high" and not state.escalated and ("vip" in text or "third time" in text):
  #       return TicketAction("escalate")
  # return TicketAction("resolve")