from support_ticket_router.environment import SupportTicketRouterEnv

def grade_episode(env:SupportTicketRouterEnv)->float:
  if env.state_data is None or env.current_task is None:
    return 0.0
  correct_flow=env.current_task['correct_flow']
  history=env.state_data.history
  score=0.0
  matches=0
  for i in range(min(len(history),len(correct_flow))):
    if history[i]==correct_flow[i]:
      matches+=1
  sequence_score=matches/len(correct_flow)
  extra_steps=max(0,len(history)-len(correct_flow))
  penalty=0.1*extra_steps
  if not env.state_data.resolved:
    penalty+=0.2
  if not env.state_data.done:
    penalty+=0.2
  final_score=max(0.0,sequence_score-penalty)
  return round(min(1.0,final_score),2)