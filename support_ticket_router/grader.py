from support_ticket_router.environment import SupportTicketRouterEnv

def grade_episode(env:SupportTicketRouterEnv)->float:
  if env.state_data is None or env.current_task is None:
    return 0.0
  correct_flow=env.current_task['correct_flow']
  history=env.state_data.history
  matches=0
  for i in range(min(len(history),len(correct_flow))):
    if history[i]==correct_flow[i]:
      matches+=1
  score=matches/len(correct_flow)
  if env.state_data.done and env.state_data.resolved:
    score=min(1.0,score)
  return round(score,2)