from support_ticket_router.environment import SupportTicketRouterEnv,TASKS
from support_ticket_router.models import TicketAction
from support_ticket_router.grader import grade_episode


def run_and_debug(task_name,actions):
    env=SupportTicketRouterEnv(TASKS)
    env.reset(task_name)
    print(f"\n--- Testing task: {task_name} ---")
    print("Correct flow:", TASKS[task_name]["correct_flow"])
    
    for action in actions:
        obs,reward,done,info=env.step(TicketAction(action))
        print(f"\n--- Testing task: {task_name} ---")
        print("Correct flow:", TASKS[task_name]["correct_flow"])
    final_grade=grade_episode(env)
    print("Final Grade:",final_grade)
    return final_grade

def main():
    #easy task
    easy_grade=run_and_debug('easy',['assign_billing','resolve'])
    assert easy_grade==1.0,f'Easy task failed. Getting {easy_grade}'

    #medium task
    medium_grade=run_and_debug('medium',['assign_technical','resolve'])
    assert medium_grade==1.0,f'Medium task failed. Getting {medium_grade}'

    #difficult task
    hard_grade=run_and_debug('hard',['assign_billing','escalate','resolve'])
    assert hard_grade==1.0,f'Hard task failed. Getting {hard_grade}'

    print('\nSmoke test passed...')

    hard_fail_grade=run_and_debug('hard',['assign_billing','resolve'])
    print("Missed Escalation:",hard_fail_grade)
    easy_fail_grad=run_and_debug('easy',['assign_billing','assign_shipping','resolve'])
    print("Extra wrong step:",easy_fail_grad)


if __name__=="__main__":
    main()