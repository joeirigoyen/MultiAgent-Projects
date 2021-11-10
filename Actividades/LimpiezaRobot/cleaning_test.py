#%%
from cleaning_model import CleaningModel


model = CleaningModel(3, 50, 20, 90)

for i in range(1000):
    model.step()

required_steps = model.ticks
cleaned_cells = model.dirtycell_datacollector.get_model_vars_dataframe()

total_moves = model.dirtycell_datacollector.get_agent_vars_dataframe()
end_moves = total_moves.xs(249, level="Step")

cleaned_cells.plot()
end_moves.plot(kind="bar")

print(f"Completion steps: {required_steps}")

# %%
