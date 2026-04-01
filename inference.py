import requests
import os
from openai import OpenAI

BASE_URL = os.getenv("BASE_URL","https://krishnajoga-support-ticket-router-v2.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME","gpt-5-mini")
HF_TOKEN = os.getenv("HF_TOKEN","")

VALID_ACTIONS=[
    "assign_billing",
    "assign_technical",
    "assign_shipping",
    "request_more_info",
    "escalate",
    "resolve"
]

client=OpenAI(base_url=BASE_URL if BASE_URL.startswith("http") else None,api_key=HF_TOKEN if HF_TOKEN else "dummy")

def choose_action_with_llm(observation:dict,state:dict)->str:
    prompt=f"""You are an agent solving a customer support task. Your goal is to choose exactly one of the below tasks.{VALID_ACTIONS}.
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
    - Return only one string.
    - Do not explain.
    - Prefer efficient resolution.
    - Escalate when urgency is high and issue is critical or repeated."""

    response=client.responses.create(model="gpt-5-mini",input=prompt)
    action=response.output_text.strip()
    if action not in VALID_ACTIONS:
        return "request_more_info"
    return action

def run_episode(task_name:str):
    response=requests.post(f"{BASE_URL}/reset",json={'task_name':task_name},timeout=30)
    response.raise_for_status()
    obs=response.json()
    print(f"\nTask name: {task_name}")
    print("Initial Observation:",obs)
    done=False
    
    while not done:
        action_res=requests.get(f"{BASE_URL}/baseline")
        action_res.raise_for_status()
        action=action_res.json()['baseline_action']

        print("Action:",action)

        step_res=requests.post(f"{BASE_URL}/step",json={"action_type":action})
        step_res.raise_for_status()
        data=step_res.json()

        print("Reward:",data['reward'])
        print("Message:",data['observation']['message'])

        done=data['done']
    
    grader_res=requests.get(f"{BASE_URL}/grader")
    grader_res.raise_for_status()
    print("Final_grade:",grader_res.json())


def run_episode_llm(task_name:str):
    reset_res=requests.post(f"{BASE_URL}/reset",json={"task_name":task_name})
    observation=reset_res.json()
    print(f"\n----Task:{task_name}---")
    print("Initial Observation:",observation)
    done=False
    while not done:
        state_res=requests.get(f"{BASE_URL}/state")
        state=state_res.json()
        try:
            action=choose_action_with_llm(observation,state)
        except Exception:
            action="request_more_info" #not necessary, just for robustness
        print("Chosen action:",action)
        step_res=requests.post(f"{BASE_URL}/step",json={"action_type":action})
        step_data=step_res.json()
        print("Reward:",step_data["reward"])
        print("Message:",step_data["observation"]["message"])
        observation=step_data['observation']
        done=step_data['done']
    grade_res=requests.get(f"{BASE_URL}/grader")
    print("Final Grade:",grade_res.json())

if __name__=="__main__":
    for task in ['easy','medium','hard','extra_hard','hard_missing_info','vip_priority','repeat_failure']:
        run_episode(task)
    # run_episode('easy')
    # run_episode('medium')
    # run_episode('hard')
    # run_episode('extra_hard')
    # run_episode('hard_missing_info')
    # run_episode('vip_priority')
    # run_episode('repeat_failure')
    # run_episode_llm('easy')
    # run_episode_llm('hard')
    # run_episode_llm('hard_missing_info')