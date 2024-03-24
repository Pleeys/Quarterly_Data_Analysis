import pandas as pd

def load_data(filename):
    return pd.read_csv(filename)

def predict_average(x_list, df):
    mean_b1_t = df['b1_t'].mean()
    mean_b2_t = df['b2_t'].mean()
    return [round(mean_b1_t * x + mean_b2_t, 2) for x in x_list]

def predict_status_quo(x_list, df):
    first_b1_t = df['b1_t'].iloc[0]
    first_b2_t = df['b2_t'].iloc[0]
    return [round(first_b1_t * x + first_b2_t, 2) for x in x_list]

def predict_weighted_average(x_list, df):
    n_elements = len(df)
    weights = [i for i in range(1, n_elements + 1)]
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    weighted_b1_t = sum(df['b1_t'] * normalized_weights)
    weighted_b2_t = sum(df['b2_t'] * normalized_weights)
    return [round(weighted_b1_t * x + weighted_b2_t, 2) for x in x_list]

def print_forecast(x_values, df, forecast_method, method_name):
    Y_values = forecast_method(x_values, df)
    print(f"\nForecasts using the '{method_name}' method:")
    for x, Y in zip(x_values, Y_values):
        print(f"For x = {x}, the forecasted Y is: {Y}")

filename = 'moving_model.csv'
data = load_data(filename)
x_values = [6.9, 7.46, 9.35, -11.02]

print_forecast(x_values, data, predict_status_quo, "status_quo")
print_forecast(x_values, data, predict_average, "average")
print_forecast(x_values, data, predict_weighted_average, "weighted_average")
