import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 读取。。。路径下所有文件
# father_path = "../name_cpl/"
# file_path = []
# for root, dirs, files in os.walk(father_path):
#     for file in files:
#         if file.endswith(".csv"):
#             file_path.append(os.path.join(root, file))
# for path in file_path:
path = '/home/test/fuzz/code/stockfish/name_cpl/202006.csv'
df = pd.read_csv(path)
print("-------------------")
print(path)
# 过滤掉object列中值不为1的行
df = df[df['object'] == 1]
filtered_df = df[df['win'] == 0]

# 过滤掉CPL列中的null值
cpl_values = filtered_df['CPL'].dropna()

# 计算均值
mean_cpl = cpl_values.mean()
print(f"Mean CPL: {mean_cpl}")

# 计算众数
mode_cpl = cpl_values.mode()[0]
print(f"Mode CPL: {mode_cpl}")

# 计算离群点
Q1 = cpl_values.quantile(0.25)
Q3 = cpl_values.quantile(0.75)
IQR = Q3 - Q1
outliers = cpl_values[(cpl_values < (Q1 - 16 * IQR)) | (cpl_values > 1000)]
print(f"Outliers: {outliers}")
print(f"Number of outliers: {len(outliers)}")
print(f"IQR: {IQR}, Q1: {Q1}, Q3: {Q3}")

# 去掉离群点
cpl_values_no_outliers = cpl_values[~cpl_values.isin(outliers)]

# 重新计算均值
mean_cpl_no_outliers = cpl_values_no_outliers.mean()
print(f"Mean CPL without outliers: {mean_cpl_no_outliers}")

# 绘制去掉离群点后的CPL列的值的分布图
plt.figure(figsize=(10, 6))
plt.hist(cpl_values_no_outliers, bins=1000, edgecolor='black')
plt.title('Distribution of CPL Values (Without Outliers)')
plt.xlabel('CPL')
plt.ylabel('Frequency')
plt.axvline(mean_cpl_no_outliers, color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_cpl_no_outliers:.2f}')
plt.axvline(mode_cpl, color='g', linestyle='dashed', linewidth=1, label=f'Mode: {mode_cpl:.2f}')
plt.legend()
plt.savefig('CPL_fig_no_outliers.png')
