import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import os
import numpy as np

# ── Global dark theme ──────────────────────────────────────────────
BG        = '#0D0D0D'
SURFACE   = '#161616'
BORDER    = '#2A2A2A'
TEXT      = '#F0F0F0'
MUTED     = '#666666'
ACCENT    = '#E8FF47'
COLORS    = ['#47FFD4','#FF6B35','#E8FF47','#FF47A0','#A78BFA','#38BDF8','#FB923C','#4ADE80']

plt.rcParams.update({
    'figure.facecolor'  : BG,
    'axes.facecolor'    : SURFACE,
    'axes.edgecolor'    : BORDER,
    'axes.labelcolor'   : MUTED,
    'axes.spines.top'   : False,
    'axes.spines.right' : False,
    'text.color'        : TEXT,
    'xtick.color'       : MUTED,
    'ytick.color'       : MUTED,
    'xtick.labelsize'   : 9,
    'ytick.labelsize'   : 9,
    'grid.color'        : BORDER,
    'grid.linewidth'    : 0.5,
    'grid.linestyle'    : '--',
    'legend.facecolor'  : SURFACE,
    'legend.edgecolor'  : BORDER,
    'legend.labelcolor' : TEXT,
    'legend.fontsize'   : 8,
    'font.family'       : 'sans-serif',
})

def styled_title(ax, title, subtitle=None):
    ax.set_title(title, color=TEXT, fontsize=13, fontweight='bold',
                 pad=18, loc='left')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes,
                color=MUTED, fontsize=8, va='bottom')

def add_watermark(fig):
    fig.text(0.99, 0.01, 'India Weather Analysis · 1990–2022',
             ha='right', va='bottom', color=MUTED, fontsize=7, alpha=0.5)

# ── Load data ──────────────────────────────────────────────────────
data_folder = 'data/'

def get_city_name(filename):
    name = filename.replace('.csv', '')
    if name.startswith('weather_'):
        name = name.replace('weather_', '')
    parts = name.split('_')
    for part in parts:
        if not part.isdigit():
            return part
    return parts[0]

cities = {}
for file in os.listdir(data_folder):
    if file.endswith('.csv') and 'Station' not in file:
        city_name = get_city_name(file)
        cities[city_name] = pd.read_csv(data_folder + file)
        print(f"Loaded {city_name}: {cities[city_name].shape[0]} rows")

print("\nAll cities loaded!")

# Pre-parse dates once
for city_name, df in cities.items():
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['month'] = df['time'].dt.month
    df['year']  = df['time'].dt.year

# ── Chart 1: Average Temperature Bar Chart ────────────────────────
city_avg_temps = {name: df['tavg'].mean() for name, df in cities.items()}
labels = list(city_avg_temps.keys())
values = list(city_avg_temps.values())
sorted_pairs = sorted(zip(values, labels), reverse=True)
values, labels = zip(*sorted_pairs)

fig, ax = plt.subplots(figsize=(11, 6))
fig.subplots_adjust(left=0.08, right=0.97, top=0.88, bottom=0.12)

bars = ax.bar(labels, values, color=BORDER, width=0.6, zorder=2)
# Highlight the hottest bar
for i, (bar, val) in enumerate(zip(bars, values)):
    bar.set_color(ACCENT if i == 0 else '#2A2A2A')
    bar.set_edgecolor(ACCENT if i == 0 else '#3A3A3A')
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.1,
            f'{val:.1f}°', ha='center', va='bottom',
            color=ACCENT if i == 0 else MUTED, fontsize=8, fontweight='bold')

ax.set_ylim(20, max(values) + 2)
ax.yaxis.set_major_locator(MaxNLocator(5))
ax.set_ylabel('Avg Temp (°C)', labelpad=10)
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=15)
ax.grid(axis='y', zorder=0)
styled_title(ax, 'Average Temperature by City', '32 years of daily data · sorted hottest to coolest')
add_watermark(fig)
plt.savefig('outputs/avg_temperature_by_city.png', dpi=150, facecolor=BG)
plt.show()

# ── Chart 2: Monthly Rainfall Line Chart ──────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))
fig.subplots_adjust(left=0.07, right=0.82, top=0.88, bottom=0.12)

month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

for i, (city_name, df) in enumerate(cities.items()):
    monthly_rain = df.groupby('month')['prcp'].mean()
    color = COLORS[i % len(COLORS)]
    ax.plot(monthly_rain.index, monthly_rain.values,
            color=color, linewidth=2, marker='o', markersize=4,
            markerfacecolor=BG, markeredgewidth=1.5,
            label=city_name, zorder=3)

ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_labels)
ax.set_ylabel('Avg Rainfall (mm)', labelpad=10)
ax.grid(axis='y', zorder=0)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', framealpha=0.9)
styled_title(ax, 'Monthly Rainfall Pattern by City', 'Monsoon season clearly visible · Jun–Sep peak')
add_watermark(fig)
plt.savefig('outputs/monthly_rainfall.png', dpi=150, facecolor=BG)
plt.show()

# ── Chart 3: Temperature Heatmap ──────────────────────────────────
heatmap_data = {}
for city_name, df in cities.items():
    heatmap_data[city_name] = df.groupby('month')['tavg'].mean()

heatmap_df = pd.DataFrame(heatmap_data).T
heatmap_df.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax = plt.subplots(figsize=(14, 5))
fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.12)

cmap = sns.color_palette("YlOrRd", as_cmap=True)
sns.heatmap(heatmap_df, annot=True, fmt='.1f', cmap=cmap,
            linewidths=1, linecolor=BG,
            annot_kws={'size': 9, 'color': '#111'},
            cbar_kws={'shrink': 0.8, 'pad': 0.02},
            ax=ax)

ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(left=False, bottom=False)
plt.setp(ax.get_xticklabels(), color=MUTED, fontsize=9)
plt.setp(ax.get_yticklabels(), color=TEXT, fontsize=9, rotation=0)
ax.collections[0].colorbar.ax.tick_params(colors=MUTED, labelsize=8)
styled_title(ax, 'Monthly Temperature Heatmap (°C)', 'Darker = hotter · Rourkela peaks at 33.2° in April')
add_watermark(fig)
plt.savefig('outputs/temperature_heatmap.png', dpi=150, facecolor=BG)
plt.show()

# ── Chart 4: Yearly Trend Line Chart ──────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
fig.subplots_adjust(left=0.07, right=0.82, top=0.88, bottom=0.12)

for i, (city_name, df) in enumerate(cities.items()):
    if city_name == 'Rourkela':
        continue
    yearly_avg = df.groupby('year')['tavg'].mean()
    color = COLORS[i % len(COLORS)]
    ax.plot(yearly_avg.index, yearly_avg.values,
            color=color, linewidth=1.8, marker='o', markersize=3,
            markerfacecolor=BG, markeredgewidth=1.2,
            label=city_name, alpha=0.9, zorder=3)

    # Trend line
    x = yearly_avg.index.values
    y = yearly_avg.values
    mask = ~np.isnan(y)
    if mask.sum() > 2:
        z = np.polyfit(x[mask], y[mask], 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), color=color, linewidth=0.6,
                linestyle='--', alpha=0.4, zorder=2)

ax.set_ylabel('Avg Temperature (°C)', labelpad=10)
ax.set_xlabel('Year', labelpad=10)
ax.grid(axis='y', zorder=0)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', framealpha=0.9)
styled_title(ax, 'Yearly Temperature Trend (1990–2022)', 'Dashed lines show long-term trend · Chennai warming most rapidly')
add_watermark(fig)
plt.savefig('outputs/yearly_temperature_trend.png', dpi=150, facecolor=BG)
plt.show()

print("\nAll charts saved to outputs/")
