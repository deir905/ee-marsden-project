import numpy as np
import pingouin as pg
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

empathic_concern_pre = [32, 27, 24, 30, 27, 24.5, 31, 35, 30]
perspective_taking_pre = [29, 25, 22, 29, 20, 24.4, 32, 28, 28]

empathic_concern_post = [29, 22, 22, 26, 27, 30, 35, 35, 31]
perspective_taking_post = [27, 23, 26, 27, 24, 24, 31, 31, 26]


print("Paired T-test Empathy Concern Pre-VR vs Post-VR")
results = stats.ttest_ind(empathic_concern_pre, empathic_concern_post)
print(f't-value: {results.statistic:.4f}, p-value: {results.pvalue:.4f}, df: {results.df}')

print("Paired T-test Perspective-taking Pre-VR vs Post-VR")
results = stats.ttest_ind(perspective_taking_pre, perspective_taking_post)
print(f't-value: {results.statistic:.4f}, p-value: {results.pvalue:.4f}, df: {results.df}')


# Create box plots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Empathic Concern Box Plot
axes[0].boxplot([empathic_concern_pre, empathic_concern_post], labels=['Pre', 'Post'])
axes[0].set_title('Empathic Concern Subscale')
axes[0].set_ylabel('Scores')

# Perspective-Taking Box Plot
axes[1].boxplot([perspective_taking_pre, perspective_taking_post], labels=['Pre', 'Post'])
axes[1].set_title('Perspective-Taking Subscale')
axes[1].set_ylabel('Scores')

# Show plots
plt.tight_layout()
plt.show()