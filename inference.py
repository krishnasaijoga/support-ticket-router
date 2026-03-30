import requests

BASE_URL = "https://krishnajoga-support-ticket-router-v2.hf.space"

def run_episode(task_name):
    response=requests.post(f"{BASE_URL}/reset",json={'task_name':task_name})
    obs=response.json()
    print(f"\nTask name: {task_name}")
    print("Initial Observation:",obs)
    done=False
    
    while not done:
        action_res=requests.get(f"{BASE_URL}/baseline")
        action=action_res.json()['baseline_action']

        print("Action:",action)

        step_res=requests.post(f"{BASE_URL}/step",json={"action_type":action})
        data=step_res.json()

        print("Reward:",data['reward'])
        print("Message:",data['observation']['message'])

        done=data['done']
    
    grader_res=requests.get(f"{BASE_URL}/grader")
    print("Final_grade:",grader_res.json())

if "__name__"=="__main__":
    run_episode('easy')
    run_episode('medium')
    # run_episode('hard')
    # run_episode('extra_hard')
    # run_episode('hard_missing_info')
    # run_episode('vip_priority')
    # run_episode('repeat_failure')