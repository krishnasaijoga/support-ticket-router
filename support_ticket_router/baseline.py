from support_ticket_router.models import TicketAction, TicketObservation

def baseline_policy(observation:TicketObservation)->TicketAction:
  text=observation.ticket_text.lower()
  if 'payment' in text or 'money deducted' in text:
    return TicketAction('assign_billing')
  elif 'login' in text or 'password' in text or 'account' in text:
    return TicketAction('assign_technical')
  elif 'delivery' in text or 'shipping' in text:
    return TicketAction('assign_shipping')
  else:
    return TicketAction('request_more_info')