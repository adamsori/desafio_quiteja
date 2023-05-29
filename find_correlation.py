import pandas as pd
import zipfile


def set_status_id(row):
    if row['status'] == 'CRITICO':
        return 1

    if row['status'] == 'NORMAL':
        return 0


with zipfile.ZipFile('dados.zip', 'r') as zip_ref:
    zip_ref.extractall()

data = pd.read_csv('origem-dados.csv', parse_dates=['created_at'])
data['status_id'] = data.apply(lambda row: set_status_id(row), axis=1)

data = data.drop(columns=['status'])
print(data.corr(method='pearson', min_periods=1, numeric_only=False))
print(data.corr(method='spearman', min_periods=1, numeric_only=False))
