#%%
from cleaning_model import CleaningModel

MAX_STEPS = 500

model = CleaningModel(5, 20, 20, 100)

for i in range(MAX_STEPS):
    model.step()

required_steps = model.ticks
cleaned_cells = model.dirtycell_datacollector.get_model_vars_dataframe()

total_moves = model.dirtycell_datacollector.get_agent_vars_dataframe()
end_moves = total_moves.xs(MAX_STEPS - 1, level="Step")

cleaned_cells.plot()
end_moves.plot(kind="bar")

print(f"Completion steps: {required_steps}")
print(f"Clean cell percentage: {(model.total_cells - model.dirty_cells_count) / (model.total_cells) * 100}%")

# %%
    