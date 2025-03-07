import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("Data Analysis Dashboard")
st.markdown("This dashboard provides insights from your data analysis.")

# Sidebar for filters and options
st.sidebar.header("Filters and Options")

# File uploader (optional)
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Load data
@st.cache_data  # This decorator caches the data to improve performance
def load_data():
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        # Load default dataset or sample data
        # Replace this with your actual data loading code
        data = pd.DataFrame(
            np.random.randn(100, 5),
            columns=['A', 'B', 'C', 'D', 'E']
        )
    return data

df = load_data()

# Display raw data in an expandable section
with st.expander("Raw Data"):
    st.dataframe(df)
    
    # Download button for the data
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='dashboard_data.csv',
        mime='text/csv',
    )

# Basic statistics
st.header("Data Summary")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Descriptive Statistics")
    st.write(df.describe())

with col2:
    st.subheader("Missing Values")
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing Values': df.isnull().sum().values,
        'Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    st.write(missing_data)

# Visualizations
st.header("Visualizations")

# Select columns for visualization
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Visualization tabs
tab1, tab2, tab3 = st.tabs(["Distribution", "Correlation", "Custom Plot"])

with tab1:
    st.subheader("Distribution Analysis")
    
    if numeric_columns:
        selected_column = st.selectbox("Select column for histogram", numeric_columns, key="hist_col")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df[selected_column], kde=True, ax=ax)
        plt.title(f'Distribution of {selected_column}')
        plt.xlabel(selected_column)
        plt.ylabel('Frequency')
        st.pyplot(fig)
        
        # Display basic statistics for the selected column
        st.write(f"Mean: {df[selected_column].mean():.2f}")
        st.write(f"Median: {df[selected_column].median():.2f}")
        st.write(f"Std Dev: {df[selected_column].std():.2f}")

with tab2:
    st.subheader("Correlation Analysis")
    
    if len(numeric_columns) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        correlation_matrix = df[numeric_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        plt.title('Correlation Matrix')
        st.pyplot(fig)
    else:
        st.write("Need at least two numeric columns for correlation analysis.")

with tab3:
    st.subheader("Custom Plot")
    
    if numeric_columns:
        plot_type = st.selectbox("Select plot type", ["Scatter", "Line", "Bar", "Box"], key="plot_type")
        
        if plot_type == "Scatter" and len(numeric_columns) >= 2:
            x_col = st.selectbox("Select X axis", numeric_columns, key="x_col")
            y_col = st.selectbox("Select Y axis", numeric_columns, index=1 if len(numeric_columns) > 1 else 0, key="y_col")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
            plt.title(f'{y_col} vs {x_col}')
            st.pyplot(fig)
            
        elif plot_type == "Line" and numeric_columns:
            selected_cols = st.multiselect("Select columns", numeric_columns, default=[numeric_columns[0]], key="line_cols")
            
            if selected_cols:
                fig, ax = plt.subplots(figsize=(10, 6))
                for col in selected_cols:
                    sns.lineplot(data=df, y=col, x=df.index, label=col, ax=ax)
                plt.title('Line Plot')
                plt.legend()
                st.pyplot(fig)
            
        elif plot_type == "Bar" and numeric_columns:
            if categorical_columns:
                x_col = st.selectbox("Select category (X axis)", categorical_columns, key="bar_x")
                y_col = st.selectbox("Select value (Y axis)", numeric_columns, key="bar_y")
                
                # Aggregate data for bar chart
                agg_data = df.groupby(x_col)[y_col].mean().reset_index()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=agg_data, x=x_col, y=y_col, ax=ax)
                plt.title(f'Average {y_col} by {x_col}')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                y_col = st.selectbox("Select column for bar chart", numeric_columns, key="bar_y_only")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=df, y=y_col, x=df.index, ax=ax)
                plt.title(f'Bar Plot of {y_col}')
                st.pyplot(fig)
                
        elif plot_type == "Box" and numeric_columns:
            selected_cols = st.multiselect("Select columns", numeric_columns, default=[numeric_columns[0]], key="box_cols")
            
            if selected_cols:
                fig, ax = plt.subplots(figsize=(10, 6))
                melted_df = pd.melt(df[selected_cols])
                sns.boxplot(data=melted_df, x='variable', y='value', ax=ax)
                plt.title('Box Plot')
                plt.xticks(rotation=45)
                st.pyplot(fig)

# Additional insights or ML section can be added here

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit")
st.markdown("For more information, contact [Your Name](mailto:your.email@example.com)")
st.markdown("© 2023 Your Company")

# Run the app with `streamlit run dashboardbikesharing.py`