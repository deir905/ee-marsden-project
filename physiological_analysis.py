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

without_VR_Tonic = [-1.489627957, -1.070893363, -1.23658167, 1.700419284, -0.706948502, -0.550960361, -0.990634973, 0.282991424, -1.491298022]
baseline_VR_Tonic = [-0.260396076, 0.053150416, 0.233887042, 0.778513466, -1.469885343, 0.644772746, 0.026168615, 1.348346233, 0.673108436]
VR_Tonic = [0.51485527, 0.387535068, 0.639599817, -0.67455437, 0.333406956, -0.564709816, 0.281620152, -0.296542799, 0.533326696]

without_VR_Phasic = [-0.000266331, -0.000133371, 0.00000490095282930525, 0.001217579, 0.000253161, 0.0000565477692761481, 0.0000812537681729234, -0.0000567939657170112, 0.002895032]
baseline_VR_Phasic = [0.0000882, -0.000438519, 0.000133421010995866, 0.0000332149028333078, 0.00089389, -0.00000314641363601047, -0.0000427930814691671, 0.0000105971411432056, -0.000126324]
VR_Phasic = [0.000109921, 0.0000402484347404567, -0.0000423180652569983, -0.00000993393618846607, 0.0000457471926570951, -0.0000111636268705864, -0.0000108657400612203, 
-0.00000740940753763706, 0.0000343287803061832]

without_VR_EDA = [-1.489769155, -1.070618426, -1.236561483, 1.702140148, -0.705158324, -0.551068943, -0.994012155, 0.595982731, -1.488597004]
baseline_VR_EDA = [-0.258823036, 0.052188669, 0.234353739, 0.77886589, -1.465540182, 0.644350503, 0.025840592, 1.347481767, 0.672525453]
VR_EDA = [0.515071482, 0.387708109, 0.639950809, -0.674447237, 0.333180587, -0.564729501, 0.282991424, -0.296576891, 0.533362248]

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




print("Without_VR_Tonic Shapiro-Wilk Test for Normality")
without_VR_Tonic_shapiro_test = stats.shapiro(without_VR_Tonic)
print(f'Statistic: {without_VR_Tonic_shapiro_test.statistic:.4f}, p-value: {without_VR_Tonic_shapiro_test.pvalue:.4f}')

print("Baseline_VR_Tonic Shapiro-Wilk Test for Normality")
baseline_VR_Tonic_shapiro_test = stats.shapiro(baseline_VR_Tonic)
print(f'Statistic: {baseline_VR_Tonic_shapiro_test.statistic:.4f}, p-value: {baseline_VR_Tonic_shapiro_test.pvalue:.4f}')

print("VR_Tonic Shapiro-Wilk Test for Normality")
VR_Tonic_shapiro_test = stats.shapiro(VR_Tonic)
print(f'Statistic: {VR_Tonic_shapiro_test.statistic:.4f}, p-value: {VR_Tonic_shapiro_test.pvalue:.4f}\n')

print("Tonic Mauchly Test for Sphericity")
# Convert to long-format DataFrame
data = pd.DataFrame({
    "subject": np.arange(1, 10).repeat(3),  # 9 subjects, repeated 3 times
    "condition": np.tile(["without_VR", "baseline_VR", "VR"], 9),
    "Tonic": without_VR_Tonic + baseline_VR_Tonic + VR_Tonic
})

# Test for sphericity
Tonic_sphericity_test = pg.sphericity(data, dv="Tonic", subject="subject", within="condition")
print(f'Statistic: {Tonic_sphericity_test.W:.4f}, pvalue: {Tonic_sphericity_test.pval:.4f}\n')

print("Tonic One-way RM ANOVA")
# Run one-way repeated measures ANOVA
Tonic_anova_results = pg.rm_anova(data, dv="Tonic", within="condition", subject="subject", detailed=True)
print(f'F-value: {Tonic_anova_results["F"].values[0]}, p-value: {Tonic_anova_results["p-unc"].values[0]}, df1: {Tonic_anova_results["DF"].values[0]}, df2: {Tonic_anova_results["DF"].values[1]}')
print(f'APA Style: F({Tonic_anova_results["DF"].values[0]},{Tonic_anova_results["DF"].values[1]})={Tonic_anova_results["F"].values[0]:.3f},p={Tonic_anova_results["p-unc"].values[0]:.3f}\n\n')









print("Without_VR_Phasic Shapiro-Wilk Test for Normality")
without_VR_Phasic_shapiro_test = stats.shapiro(without_VR_Phasic)
print(f'Statistic: {without_VR_Phasic_shapiro_test.statistic:.4f}, p-value: {without_VR_Phasic_shapiro_test.pvalue:.4f}')

print("Baseline_VR_Phasic Shapiro-Wilk Test for Normality")
baseline_VR_Phasic_shapiro_test = stats.shapiro(baseline_VR_Phasic)
print(f'Statistic: {baseline_VR_Phasic_shapiro_test.statistic:.4f}, p-value: {baseline_VR_Phasic_shapiro_test.pvalue:.4f}')

print("VR_Phasic Shapiro-Wilk Test for Normality")
VR_Phasic_shapiro_test = stats.shapiro(VR_Phasic)
print(f'Statistic: {VR_Phasic_shapiro_test.statistic:.4f}, p-value: {VR_Phasic_shapiro_test.pvalue:.4f}\n')

print("Phasic Mauchly Test for Sphericity")
# Convert to long-format DataFrame
data = pd.DataFrame({
    "subject": np.arange(1, 10).repeat(3),  # 9 subjects, repeated 3 times
    "condition": np.tile(["without_VR", "baseline_VR", "VR"], 9),
    "Phasic": without_VR_Phasic + baseline_VR_Phasic + VR_Phasic
})

# Test for sphericity
Phasic_sphericity_test = pg.sphericity(data, dv="Phasic", subject="subject", within="condition")
print(f'Statistic: {Phasic_sphericity_test.W:.4f}, pvalue: {Phasic_sphericity_test.pval:.4f}\n')

print("Phasic One-way RM ANOVA")
# Run one-way repeated measures ANOVA
Phasic_anova_results = pg.rm_anova(data, dv="Phasic", within="condition", subject="subject", detailed=True)
print(f'F-value: {Phasic_anova_results["F"].values[0]}, p-value: {Phasic_anova_results["p-unc"].values[0]}, df1: {Phasic_anova_results["DF"].values[0]}, df2: {Phasic_anova_results["DF"].values[1]}')
print(f'APA Style: F({Phasic_anova_results["DF"].values[0]},{Phasic_anova_results["DF"].values[1]})={Phasic_anova_results["F"].values[0]:.3f},p={Phasic_anova_results["p-unc"].values[0]:.3f}\n\n')










print("Without_VR_EDA Shapiro-Wilk Test for Normality")
without_VR_EDA_shapiro_test = stats.shapiro(without_VR_EDA)
print(f'Statistic: {without_VR_EDA_shapiro_test.statistic:.4f}, p-value: {without_VR_EDA_shapiro_test.pvalue:.4f}')

print("Baseline_VR_EDA Shapiro-Wilk Test for Normality")
baseline_VR_EDA_shapiro_test = stats.shapiro(baseline_VR_EDA)
print(f'Statistic: {baseline_VR_EDA_shapiro_test.statistic:.4f}, p-value: {baseline_VR_EDA_shapiro_test.pvalue:.4f}')

print("VR_EDA Shapiro-Wilk Test for Normality")
VR_EDA_shapiro_test = stats.shapiro(VR_EDA)
print(f'Statistic: {VR_EDA_shapiro_test.statistic:.4f}, p-value: {VR_EDA_shapiro_test.pvalue:.4f}\n')

print("EDA Mauchly Test for Sphericity")
# Convert to long-format DataFrame
data = pd.DataFrame({
    "subject": np.arange(1, 10).repeat(3),  # 9 subjects, repeated 3 times
    "condition": np.tile(["without_VR", "baseline_VR", "VR"], 9),
    "EDA": without_VR_EDA + baseline_VR_EDA + VR_EDA
})

# Test for sphericity
EDA_sphericity_test = pg.sphericity(data, dv="EDA", subject="subject", within="condition")
print(f'Statistic: {EDA_sphericity_test.W:.4f}, pvalue: {EDA_sphericity_test.pval:.4f}\n')

print("EDA Friedman test")
# Run one-way repeated measures ANOVA
EDA_friedman_results = stats.friedmanchisquare(without_VR_EDA, baseline_VR_EDA, VR_EDA)
print(f'Statistic: {EDA_friedman_results.statistic:.4f}, p-value: {EDA_friedman_results.pvalue:.4f}\n')



print("Paired T-test HR baseline without VR vs baseline with VR")
results = stats.ttest_ind(without_VR_HR, baseline_VR_HR)
print(f't-value: {results.statistic:.4f}, p-value: {results.pvalue:.4f}, df: {results.df}')

print("Paired T-test HR baseline without VR vs VR scenario")
results = stats.ttest_ind(without_VR_HR, VR_HR)
print(f't-value: {results.statistic:.4f}, p-value: {results.pvalue:.4f}, df: {results.df}')

print("Paired T-test HR baseline with VR vs VR scenario")
results = stats.ttest_ind(baseline_VR_HR, VR_HR)
print(f't-value: {results.statistic:.4f}, p-value: {results.pvalue:.4f}, df: {results.df}')




