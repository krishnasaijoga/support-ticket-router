import requests
import os
from openai import OpenAI

ENV_BASE_URL = os.getenv("ENV_BASE_URL","https://krishnajoga-support-ticket-router-v2.hf.space")
API_BASE_URL=os.getenv("API_BASE_URL","https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME","Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN","")

TASKS = [
    "easy",
    "medium",
    "hard",
    "extra_hard",
    "hard_missing_info",
    "vip_priority",
    "repeat_failure",
]

VALID_ACTIONS=[
    "assign_billing",
    "assign_technical",
    "assign_shipping",
    "request_more_info",
    "escalate",
    "resolve"
]

MAX_STEPS=8
BENCHMARK='support-ticket-router'

client=OpenAI(base_url=API_BASE_URL if API_BASE_URL.startswith("https") else None,api_key=HF_TOKEN if HF_TOKEN else "dummy")


def choose_action_with_llm(observation:dict,state:dict)->str:
    prompt=f"""You are an agent solving a customer support task. Your goal is to choose exactly one of the below tasks.{VALID_ACTIONS}

    Current Observation:
    ticket_text:{observation.get("ticket_text")}
    customer_tier:{observation.get("customer_tier")}
    urgency:{observation.get("urgency")}
    message:{observation.get("message")}

    Current State:
    current_step:{state.get("current_step")}
    assigned_team:{state.get("assigned_team")}
    escalated:{state.get("escalated")}
    resolved:{state.get("resolved")}
    history:{state.get("history")}

    Rules:
    - Return exactly one action from the allowed list.
    - Output only the action text.
    - No explanation
    - No punctuation
    - No JSON
    """.strip()

    response=client.responses.create(model=MODEL_NAME,input=prompt)
    action=response.output_text.strip()
    if action not in VALID_ACTIONS:
        return "request_more_info"
    return action


def format_reward(value:float)->str:
    return f"{value:.2f}"


def run_episode(task_name:str)->None:
    rewards=[]
    step_num=0
    success=False
    last_error=None
    print(f"[START] task={task_name} env={BENCHMARK} model={MODEL_NAME}")
    try:
        response=requests.post(f"{ENV_BASE_URL}/reset",json={'task_name':task_name},timeout=30)
        response.raise_for_status()
        obs=response.json()
        done=False
        
        while not done and step_num<MAX_STEPS:
            state_res=requests.get(f"{ENV_BASE_URL}/state",timeout=30)
            state_res.raise_for_status()
            state=state_res.json()

            try:
                action=choose_action_with_llm(obs,state)
            except Exception as e:
                last_error=str(e)
                action='request_more_info'
            
            step_res=requests.get(f"{ENV_BASE_URL}/step",json={"action_type",action},timeout=30)
            step_res.raise_for_status()
            step_data=step_res.json()

            reward=float(step_data.get('reward',0.0))
            done=bool(step_data.get('done',False))
            info=step_data.get('info',{}) or {}
            step_num+=1
            rewards.append(reward)

            raw_error=info.get('error')
            error_str=raw_error if raw_error is not None else (last_error if last_error is not None else 'null')
            print(f"[STEP] step={step_num} action={action} reward={format_reward(reward)} done={'true' if done else 'false'} error={error_str}")

            obs=step_data.get('observation',{})
        
        grader_res=requests.get(f"{ENV_BASE_URL}/grader",timeout=30)
        grader_res.raise_for_status()
        grader_payload=grader_res.json()
        grade=float(grader_payload.get('grade',0.0))
        success=grade>0.99
    except Exception as e:
        last_error=str(e)
        print(f"[STEP] step={step_num+1} action=null reward=0.0 done=true error={last_error}")
    finally:
        rewards_str=",".join(format_reward(r) for r in rewards)
        print(f"[END] success={'true' if success else 'false'} steps={step_num} rewards={rewards_str}")


if __name__=='__main__':
    for task in TASKS:
        run_episode(task)