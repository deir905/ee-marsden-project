import numpy as np
import matplotlib.pyplot as plt

# Data
without_VR_HR = [78.06098199, 87.71100735, 75.11125855, 83.73691751, 79.39653123, 77.78837638, 87.58072116, 77.82698141, 64.02450831]
baseline_VR_HR = [79.51087412, 84.74967969, 74.97106353, 78.97458852, 69.96928554, 73.51124416, 85.24959156, 71.59970371, 64.96804532]
VR_HR = [78.15815963, 85.54858868, 72.67379777, 78.67887742, 66.33844108, 70.64208381, 82.4586985, 72.49474306, 63.63556096]

# Number of participants
num_participants = len(without_VR_HR)
indices = np.arange(num_participants)

# Define consistent colors for each condition
colors = {
    "Without VR HR": "royalblue",
    "Baseline VR HR": "seagreen",
    "VR HR": "tomato"
}

# Create subplots for pairwise comparisons
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Pairwise comparisons
pairs = [("Without VR HR", without_VR_HR, "Baseline VR HR", baseline_VR_HR),
         ("Without VR HR", without_VR_HR, "VR HR", VR_HR),
         ("Baseline VR HR", baseline_VR_HR, "VR HR", VR_HR)]

# Bar width
bar_width = 0.3

# Loop through pairs and create subplots
for ax, (label1, data1, label2, data2) in zip(axes, pairs):
    ax.bar(indices - bar_width/2, data1, width=bar_width, label=label1, color=colors[label1])
    ax.bar(indices + bar_width/2, data2, width=bar_width, label=label2, color=colors[label2])
    ax.set_xlabel("Participant Index")
    ax.set_ylabel("Heart Rate (BPM)")
    ax.set_title(f"{label1} vs {label2}")
    ax.set_xticks(indices)
    ax.set_xticklabels([f"P{i+1}" for i in range(num_participants)])
    ax.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
