from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from support_ticket_router.environment import SupportTicketRouterEnv,TASKS
from support_ticket_router.models import TicketAction
from support_ticket_router.grader import grade_episode
from support_ticket_router.baseline import baseline_policy

app=FastAPI(title='Support Ticket Router API')

env=SupportTicketRouterEnv(TASKS)
last_observation=None

class ResetRequest(BaseModel):
    task_name:str='easy'

class StepRequest(BaseModel):
    action_type:str

@app.get("/")
def home():
    return {"message":"Support Ticket Router API is running"}


@app.get("/tasks")
def get_tasks():
    return {
        "available_tasks":list(TASKS.keys()),
        "task_details":TASKS
    }


@app.post("/reset")
def reset_env(request:ResetRequest):
    global last_observation
    if request.task_name not in TASKS:
        raise HTTPException(status_code=400,detail=f'Unknown task name: {request.task_name}')
    obs=env.reset(request.task_name)
    last_observation=obs
    return {
        "ticket_text":obs.ticket_text,
        "customer_tier":obs.customer_tier,
        "urgency":obs.urgency,
        "message":obs.message
    }


@app.post("/step")
def step_env(request:StepRequest):
    global last_observation
    try:
        obs, reward, done, info=env.step(TicketAction(request.action_type))
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    last_observation=obs
    return {
        "observation":{
            "ticket_text":obs.ticket_text,
            "customer_tier":obs.customer_tier,
            "urgency":obs.urgency,
            "message":obs.message
        },
        "reward":reward,
        "done":done,
        "info":info
    }


@app.get("/state")
def get_state():
    try:
        state=env.state
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    return {
        "ticket_id":state.ticket_id,
        "current_step": state.current_step,
        "assigned_team": state.assigned_team,
        "escalated": state.escalated,
        "resolved": state.resolved,
        "score": state.score,
        "done": state.done,
        "history": state.history
    }


@app.get("/grader")
def grader():
    return {"grade":grade_episode(env)}


@app.get("/baseline")
def run_baseline():
    global last_observation
    if last_observation is None:
        raise HTTPException(status_code=400,detail="Reset the Environment first")
    action=baseline_policy(last_observation,env.state)
    return {"baseline_action":action.action_type}


if __name__=='__main__':
    import uvicorn
    uvicorn.run("app:app",host="0.0.0.0",port=7860)