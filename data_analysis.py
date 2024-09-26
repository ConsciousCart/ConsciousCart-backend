import json
import pandas as pd
import matplotlib.pyplot as plt

# Load and parse the JSON data
with open('paste.txt', 'r') as file:
    data = json.load(file)

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Extract macronutrients and energy information
df['total_fat'] = df['macronutrients'].apply(lambda x: x['total_fat']['per_serving']['value'] if x and 'total_fat' in x else 0)
df['carbohydrates'] = df['macronutrients'].apply(lambda x: x['carbohydrates']['per_serving']['value'] if x and 'carbohydrates' in x else 0)
df['protein'] = df['macronutrients'].apply(lambda x: x['protein']['per_serving']['value'] if x and 'protein' in x else 0)
df['energy'] = df['energy'].apply(lambda x: x['per_serving']['value'] if x and 'per_serving' in x else 0)

# Set up the plotting style
plt.style.use('default')

# Create a figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(20, 20))
fig.suptitle('Nutritional Information Visualization', fontsize=16)

# 1. Bar plot of macronutrients for each product
df[['product_name', 'total_fat', 'carbohydrates', 'protein']].set_index('product_name').plot(kind='bar', stacked=True, ax=axes[0, 0])
axes[0, 0].set_title('Macronutrient Composition per Product')
axes[0, 0].set_xlabel('Product')
axes[0, 0].set_ylabel('Grams')
axes[0, 0].tick_params(axis='x', rotation=90)

# 2. Scatter plot of energy vs price
axes[0, 1].scatter(df['energy'], df['price_paid'])
axes[0, 1].set_title('Energy vs Price')
axes[0, 1].set_xlabel('Energy (kcal)')
axes[0, 1].set_ylabel('Price Paid')

# 3. Pie chart of average macronutrient composition
macro_avg = df[['total_fat', 'carbohydrates', 'protein']].mean()
axes[1, 0].pie(macro_avg, labels=macro_avg.index, autopct='%1.1f%%')
axes[1, 0].set_title('Average Macronutrient Composition')

# 4. Heatmap of correlations between numerical variables
corr = df[['total_fat', 'carbohydrates', 'protein', 'energy', 'price_paid']].corr()
im = axes[1, 1].imshow(corr, cmap='coolwarm')
axes[1, 1].set_title('Correlation Heatmap')
plt.colorbar(im, ax=axes[1, 1])

# Adjust layout and display the plot
plt.tight_layout()
plt.show()