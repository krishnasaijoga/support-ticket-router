from support_ticket_router.environment import SupportTicketRouterEnv, TASKS
from support_ticket_router.models import TicketAction
from support_ticket_router.grader import grade_episode
from support_ticket_router.baseline import baseline_policy

def run_easy_task():
    env = SupportTicketRouterEnv(TASKS)

    obs = env.reset("easy")
    print("Initial observation:")
    print(obs)

    action1 = baseline_policy(obs,env.state)
    print("\nBaseline action:")
    print(action1)

    obs, reward, done, info = env.step(action1)
    print("\nAfter first step:")
    print("Observation:", obs)
    print("Reward:", reward)
    print("Done:", done)
    print("Info:", info)

    if not done:
        obs, reward, done, info = env.step(TicketAction("resolve"))
        print("\nAfter second step:")
        print("Observation:", obs)
        print("Reward:", reward)
        print("Done:", done)
        print("Info:", info)

    print("\nFinal state:")
    print(env.state)

    print("\nFinal grader score:")
    print(grade_episode(env))


if __name__ == "__main__":
    run_easy_task()