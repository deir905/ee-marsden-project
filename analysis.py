import numpy as np
import pingouin as pg
import pandas as pd
from scipy import stats

#If p > 0.05, the data is normally distributed.
#If p < 0.05, the normality assumption is violated.

#If p > 0.05, the assumption of sphericity is met.
#If p < 0.05, the assumption is violated

#If p < 0.05, there is a significant difference between conditions.
#If p > 0.05, no significant difference is found.

without_VR_HR = [78.06098199, 87.71100735, 75.11125855, 83.73691751, 79.39653123, 77.78837638, 87.58072116, 77.82698141, 64.02450831]
baseline_VR_HR = [79.51087412, 84.74967969, 74.97106353, 78.97458852, 69.96928554, 73.51124416, 85.24959156, 71.59970371, 64.96804532]
VR_HR = [78.15815963, 85.54858868, 72.67379777, 78.67887742, 66.33844108, 70.64208381, 82.4586985, 72.49474306, 63.63556096]

without_VR_HRV = [24.76500758, 20.13350492, 52.36026505, 48.94230377, 40.61852138, 50.3345374, 29.14474768, 65.91890688, 70.126316]
baseline_VR_HRV = [28.18372627, 27.17451901, 37.69357796, 56.97010666, 30.330527, 74.15818726, 25.80243931, 62.63461734, 21.25871562]
VR_HRV = [27.92657554, 22.93145787, 46.57414268, 55.08532849, 37.62224796, 72.43751361, 34.50992959, 61.96406682, 28.50308487]


print("Without_VR_HR Shapiro-Wilk Test for Normality")
without_VR_HR_shapiro_test = stats.shapiro(without_VR_HR)
print(f'Statistic: {without_VR_HR_shapiro_test.statistic:.4f}, p-value: {without_VR_HR_shapiro_test.pvalue:.4f}')

print("Baseline_VR_HR Shapiro-Wilk Test for Normality")
baseline_VR_HR_shapiro_test = stats.shapiro(baseline_VR_HR)
print(f'Statistic: {baseline_VR_HR_shapiro_test.statistic:.4f}, p-value: {baseline_VR_HR_shapiro_test.pvalue:.4f}')

print("VR_HR Shapiro-Wilk Test for Normality")
VR_HR_shapiro_test = stats.shapiro(VR_HR)
print(f'Statistic: {VR_HR_shapiro_test.statistic:.4f}, p-value: {VR_HR_shapiro_test.pvalue:.4f}\n')

print("HR Mauchly Test for Sphericity")
# Convert to long-format DataFrame
data = pd.DataFrame({
    "subject": np.arange(1, 10).repeat(3),  # 9 subjects, repeated 3 times
    "condition": np.tile(["without_VR", "baseline_VR", "VR"], 9),
    "HR": without_VR_HR + baseline_VR_HR + VR_HR
})

# Test for sphericity
HR_sphericity_test = pg.sphericity(data, dv="HR", subject="subject", within="condition")
print(f'Statistic: {HR_sphericity_test.W:.4f}, pvalue: {HR_sphericity_test.pval:.4f}\n')

print("HR One-way RM ANOVA")
# Run one-way repeated measures ANOVA
HR_anova_results = pg.rm_anova(data, dv="HR", within="condition", subject="subject", detailed=True)
print(f'F-value: {HR_anova_results["F"].values[0]}, p-value: {HR_anova_results["p-unc"].values[0]}, df1: {HR_anova_results["DF"].values[0]}, df2: {HR_anova_results["DF"].values[1]}')
print(f'APA Style: F({HR_anova_results["DF"].values[0]},{HR_anova_results["DF"].values[1]})={HR_anova_results["F"].values[0]:.3f},p={HR_anova_results["p-unc"].values[0]:.3f}\n\n')





print("Without_VR_HRV Shapiro-Wilk Test for Normality")
without_VR_HRV_shapiro_test = stats.shapiro(without_VR_HRV)
print(f'Statistic: {without_VR_HRV_shapiro_test.statistic:.4f}, p-value: {without_VR_HRV_shapiro_test.pvalue:.4f}')

print("Baseline_VR_HRV Shapiro-Wilk Test for Normality")
baseline_VR_HRV_shapiro_test = stats.shapiro(baseline_VR_HRV)
print(f'Statistic: {baseline_VR_HRV_shapiro_test.statistic:.4f}, p-value: {baseline_VR_HRV_shapiro_test.pvalue:.4f}')

print("VR_HRV Shapiro-Wilk Test for Normality")
VR_HRV_shapiro_test = stats.shapiro(VR_HRV)
print(f'Statistic: {VR_HRV_shapiro_test.statistic:.4f}, p-value: {VR_HRV_shapiro_test.pvalue:.4f}\n')

print("HRV Mauchly Test for Sphericity")
# Convert to long-format DataFrame
data = pd.DataFrame({
    "subject": np.arange(1, 10).repeat(3),  # 9 subjects, repeated 3 times
    "condition": np.tile(["without_VR", "baseline_VR", "VR"], 9),
    "HRV": without_VR_HRV + baseline_VR_HRV + VR_HRV
})

# Test for sphericity
HRV_sphericity_test = pg.sphericity(data, dv="HRV", subject="subject", within="condition")
print(f'Statistic: {HRV_sphericity_test.W:.4f}, pvalue: {HRV_sphericity_test.pval:.4f}\n')

print("HRV One-way RM ANOVA")
# Run one-way repeated measures ANOVA
HRV_anova_results = pg.rm_anova(data, dv="HRV", within="condition", subject="subject", detailed=True)
print(f'F-value: {HRV_anova_results["F"].values[0]}, p-value: {HRV_anova_results["p-unc"].values[0]}, df1: {HRV_anova_results["DF"].values[0]}, df2: {HRV_anova_results["DF"].values[1]}')
print(f'APA Style: F({HRV_anova_results["DF"].values[0]},{HRV_anova_results["DF"].values[1]})={HRV_anova_results["F"].values[0]:.3f},p={HRV_anova_results["p-unc"].values[0]:.3f}\n\n')
