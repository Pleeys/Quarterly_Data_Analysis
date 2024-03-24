import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_crawling_model(X, Y, d):
    n = len(X)
    results = []

    for i in range(0, n - d + 1):
        X_t = X[i:i + d]
        Y_t = Y[i:i + d]

        linear_model = LinearRegression()
        linear_model.fit(np.array(X_t).reshape(-1, 1), Y_t)

        B1_j = linear_model.coef_[0]
        B2_j = linear_model.intercept_

        results.append({
            'X_t': X_t[0],
            'Y': Y_t[0],
            'j': i + 1,
            'T_j': ','.join(map(str, X_t)),
            'B1_j': round(B1_j, 2),
            'B2_j': round(B2_j, 2)
        })

    for i in range(n - d + 1, n):
        results.append({
            'X_t': X[i],
            'Y': Y[i],
            'j': '',
            'T_j': '',
            'B1_j': '',
            'B2_j': ''
        })

    df = pd.DataFrame(results)
    df.insert(0, 't', range(1, len(df) + 1))
    return df

def calculate_jt(X, d):
    Jt = []
    n = len(X)
    print("n: " + str(n))
    j = 0
    for i in range(1, n + 1):
        if i <= d:
            Jt.append(list(range(1, i + 1)))
        elif i >= n - d + 2:
            start = i + 1 - d
            Jt.append(list(range(start, i - j)))
            j += 1
        else:
            start = i + 1 - d if i + 1 - d > 0 else 1
            Jt.append(list(range(start, i + 1)))

    return Jt

def calculate_averages_from_parameters(model):
    averages_b1_j = []
    averages_b2_j = []
    for indices in model["Jt"]:
        values_b1_j = model.loc[[i - 1 for i in indices], 'B1_j']
        b1_j = values_b1_j.mean()
        averages_b1_j.append(round(b1_j, 2))

        values_b2_j = model.loc[[i - 1 for i in indices], 'B2_j']
        b2_j = values_b2_j.mean()
        averages_b2_j.append(round(b2_j, 2))

    return averages_b1_j, averages_b2_j

def calculate_model(model):
    models = []
    for index, row in model.iterrows():
        model_value = round(row["b1_t"] * row["X_t"] + row["b2_t"], 2)
        models.append(model_value)
    return models

def calculate_residual(model):
    model['residue'] = round(model['Y'] - model['model'], 2)
    return model

def calculate_moving_model(X, Y, d):
    crawling_model_df = calculate_crawling_model(X, Y, d)
    crawling_model_df["Jt"] = calculate_jt(X, d)
    b1_j, b2_j = calculate_averages_from_parameters(crawling_model_df)
    crawling_model_df["b1_t"] = b1_j
    crawling_model_df["b2_t"] = b2_j
    crawling_model_df["model"] = calculate_model(crawling_model_df)
    moving_model_df = calculate_residual(crawling_model_df)
    return moving_model_df

def calculate_skr(model):
    squared_residues = model['residue'] ** 2
    sum_of_squared_residues = round(squared_residues.sum(), 2)
    return sum_of_squared_residues

def calculate_osk(model):
    Y = model['Y']
    sum_Y = Y.sum()
    sum_Y_squared = (Y ** 2).sum()
    n = len(Y)
    osk = round(sum_Y_squared - (1 / n) * (sum_Y ** 2), 2)
    return osk

def calculate_r_squared(model):
    skr = calculate_skr(model)
    osk = calculate_osk(model)
    r_squared = round(1 - (skr / osk), 2)
    return r_squared

df = pd.read_csv('earnings_data.csv')
X_values = df['SurprisePercentage'].tolist()
Y_values = df['PercentageChange'].tolist()
d = 4

crawling_model_df = calculate_crawling_model(X_values, Y_values, d)
print(crawling_model_df)

moving_model = calculate_moving_model(X_values, Y_values, d)
print(moving_model)

moving_model.to_csv('moving_model.csv', index=False)

print("SKR: " + str(calculate_skr(moving_model)))
print("OSK: ", str(calculate_osk(moving_model)))
print("R^2: ", str(calculate_r_squared(moving_model)))
