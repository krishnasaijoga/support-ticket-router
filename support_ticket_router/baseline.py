from support_ticket_router.models import TicketAction, TicketObservation

def baseline_policy(observation:TicketObservation)->TicketAction:
  text=observation.ticket_text.lower()
  tier=observation.customer_tier.lower()
  urgency=observation.urgency.lower()
  if tier=="vip" and urgency=='high':
    if "payment" in text:
      return TicketAction('assign_billing')
    elif "order" in text or "delivery" in text:
      return TicketAction('assign_shipping')
    else:
      return TicketAction('escalate')
    
  if "something is wrong" in text:
    return TicketAction('request_more_info')
  
  if 'payment' in text or 'money deducted' in text or 'charged' in text:
    return TicketAction('assign_billing')
  elif 'login' in text or 'password' in text or 'account' in text:
    return TicketAction('assign_technical')
  elif 'delivery' in text or 'shipping' in text or 'order' in text:
    return TicketAction('assign_shipping')
  else:
    return TicketAction('request_more_info')