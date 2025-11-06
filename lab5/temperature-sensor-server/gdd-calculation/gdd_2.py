import pandas as pd
import matplotlib.pyplot as plt

# === 1. Базова температура для розрахунку GDD ===
base_temperature = 102

# === 2. Завантаження CSV файлу з температурами ===
# Файл має містити щонайменше колонки: 'date' і 'temperature'
df = pd.read_csv('temperature.csv')

# === 3. Візуалізація температури по датах ===
plt.figure(figsize=(15, 8))
plt.plot(df['date'], df['temperature'], label='Temperature')
plt.xticks(rotation='vertical')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Temperature over Time')
plt.legend()
plt.show()

# === 4. Групування даних за датою та пошук мінімуму/максимуму ===
df['date'] = pd.to_datetime(df['date']).dt.date
data_by_date = df.groupby('date')

min_by_date = data_by_date.min()
max_by_date = data_by_date.max()

min_max_by_date = min_by_date.join(max_by_date, on='date', lsuffix='_min', rsuffix='_max').reset_index()

# === 5. Розрахунок GDD (Growing Degree Days) ===
def calculate_gdd(row):
    return ((row['temperature_max'] + row['temperature_min']) / 2) - base_temperature

min_max_by_date['gdd'] = min_max_by_date.apply(lambda row: calculate_gdd(row), axis=1)

# === 6. Вивід результатів ===
print(min_max_by_date[['date', 'gdd']].to_string(index=False))