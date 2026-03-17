# India Weather Pattern Analyzer

A data science project analyzing 32 years (1990–2022) of daily weather data across 8 major Indian cities. Built with Python, Pandas, Matplotlib, and Seaborn.

---

## Insights Uncovered

- **Chennai** is the hottest city on average and shows the most rapid warming trend over 32 years
- **Rourkela** peaks at 33.2°C in April — the highest single city-month in the dataset
- **Mumbai** shows a clear monsoon spike in June–September with the highest rainfall of all cities
- **Bangalore** remains remarkably stable at 23–24°C year-round — earning its "Garden City" reputation with data
- **Chennai** experiences a secondary rainfall peak in October–November due to the northeast monsoon
- Coastal cities (Mumbai, Chennai) show far less seasonal temperature variation than inland cities (Delhi, Lucknow)

---

## Charts

| Chart | Description |
|-------|-------------|
| `avg_temperature_by_city.png` | Bar chart comparing 32-year average temperatures across all cities |
| `monthly_rainfall.png` | Line chart showing monthly rainfall patterns — monsoon season clearly visible |
| `temperature_heatmap.png` | Heatmap of monthly average temperatures per city |
| `yearly_temperature_trend.png` | Year-over-year temperature trends with long-term trend lines per city |

---

## Project Structure

```
India_Weather_Analysis/
│
├── data/                        # Raw CSV files (one per city)
│   ├── Bangalore.csv
│   ├── Chennai.csv
│   ├── Delhi.csv
│   ├── Lucknow.csv
│   ├── Mumbai.csv
│   ├── Rajasthan.csv
│   ├── Bhubaneswar.csv
│   ├── Rourkela.csv
│   └── Station_GeoLocation.csv
│
├── code/                        # Python scripts
│   └── analysis.py              # Main analysis and chart generation
│
├── outputs/                     # Generated charts (auto-created on run)
│   ├── avg_temperature_by_city.png
│   ├── monthly_rainfall.png
│   ├── temperature_heatmap.png
│   └── yearly_temperature_trend.png
│
└── README.md
```

---

## Setup and Usage

### 1. Clone the repository
```bash
git clone https://github.com/your-username/India_Weather_Analysis.git
cd India_Weather_Analysis
```

### 2. Install dependencies
```bash
pip install pandas matplotlib seaborn numpy
```

### 3. Run the analysis
```bash
python code/analysis.py
```

Charts will be saved automatically to the `outputs/` folder.

---

## Dataset

**Indian Weather Repository** by Nidula Elgiriyewithana — available on [Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/indian-weather-repository-daily-snapshot).

- 8 cities: Bangalore, Chennai, Delhi, Lucknow, Mumbai, Rajasthan, Bhubaneswar, Rourkela
- ~11,900 rows per city (daily records)
- Columns: `time`, `tavg`, `tmin`, `tmax`, `prcp`

---

## Tech Stack

- **Python 3.11+**
- **Pandas** — data loading and transformation
- **Matplotlib** — chart rendering
- **Seaborn** — heatmap visualization
- **NumPy** — trend line calculations

---

## Author

**Dhruv Singh**  
[GitHub](https://github.com/shecallsmedhruvu) · [LinkedIn](https://linkedin.com/in/dhruvsinghds)
