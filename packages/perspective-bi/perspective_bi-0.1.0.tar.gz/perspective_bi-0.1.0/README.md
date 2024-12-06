# Perspective BI

A declarative business intelligence library designed for natural language interactions. Perspective BI provides a clean, intuitive API for data transformation and visualization, making it easy to create beautiful dashboards from natural language queries.

## Installation

```bash
pip install perspective-bi
```

## Quick Start

```python
import perspective_bi as px

# Load and transform data
sales_data = (
    px.DataSet('sales.csv')
    .filter(date='last_month')
    .aggregate(group_by=['category'])
    .sort_values('sales', ascending=False)
)

# Create visualization
chart = px.bar(
    data=sales_data,
    x='category', 
    y='sales',
    title='Sales by Category'
)

# Display in notebook or save
chart.show()
```

## Features

- **Declarative API**: Simple, intuitive interface for data manipulation and visualization
- **Natural Language Ready**: Designed to work seamlessly with LLM-generated instructions
- **Powerful Data Transformations**: Built on pandas with an intuitive API
- **Beautiful Visualizations**: Leverages Plotly for interactive charts
- **Flexible Data Sources**: Support for CSV, Excel, and more

## Documentation

### DataSet Operations

- `filter()`: Filter data based on conditions
- `aggregate()`: Group and aggregate data
- `sort_values()`: Sort data by columns
- `save()`: Save transformed data

### Visualizations

- `bar()`: Create bar charts
- `line()`: Create line charts
- `scatter()`: Create scatter plots
- `pie()`: Create pie charts

## License

MIT License
