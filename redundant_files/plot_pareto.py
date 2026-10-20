import matplotlib.pyplot as plt
import optuna

study = optuna.load_study(
    study_name="slow_down_turn",
    storage="sqlite:///fast_bats.db",
)

completed = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]

obj1 = [t.values[0] for t in completed]
obj2 = [t.values[1] for t in completed]

pareto_trials = study.best_trials
pareto_obj1 = [t.values[0] for t in pareto_trials]
pareto_obj2 = [t.values[1] for t in pareto_trials]

fig, ax = plt.subplots(figsize=(8, 8))  # equal width/height figure

ax.scatter(obj1, obj2, alpha=0.4, label="All trials", color="gray")
ax.scatter(pareto_obj1, pareto_obj2, color="red", label="Pareto front")

ax.set_xlabel("Objective 1")
ax.set_ylabel("Objective 2")
ax.set_title("Pareto Front")
ax.legend()

ax.set_box_aspect(
    1
)  # forces the actual plotted box to be square regardless of data range

plt.savefig("pareto_front_manual.png", dpi=150, bbox_inches="tight")
plt.show()

from optuna.visualization import (
    plot_parallel_coordinate,
    plot_param_importances,
    plot_pareto_front,
)

fig = plot_pareto_front(
    study, target_names=["wall collision", "bat bat collision"]
)  # "polarization"])

fig.update_layout(
    width=700,
    height=700,
    # yaxis=dict(
    #     scaleanchor="x",   # locks y-axis scale to x-axis scale
    #     scaleratio=1,      # 1:1 ratio
    # ),
)

fig.show()


fig = plot_parallel_coordinate(
    study, target=lambda t: t.values[0], target_name="wall_collision"
)
fig.show()

# optuna.visualization.plot_param_importances(

fig = plot_param_importances(
    study, target=lambda t: t.values[0], target_name="wall_collision"
)
fig.show()
