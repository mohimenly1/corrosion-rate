"""
Script to generate visualizations from database data for research paper
Generates charts and saves them as images
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from database.db_connection import DatabaseConnection
from config import Config
import os
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Arabic font support
try:
    # Try to use a font that supports Arabic
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

def format_arabic_text(text):
    """Format Arabic text for proper display in matplotlib"""
    if text:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    return text

# Create output directory
output_dir = 'research_visualizations'
os.makedirs(output_dir, exist_ok=True)

# Initialize database connection
db = DatabaseConnection()

def fetch_data():
    """Fetch all corrosion samples from database"""
    try:
        query = """
            SELECT 
                material,
                temperature,
                ph,
                nacl_percentage,
                medium,
                corrosion_rate_mm_per_yr,
                corrosion_rate_mpy
            FROM corrosion_samples
            WHERE temperature IS NOT NULL 
            AND corrosion_rate_mm_per_yr IS NOT NULL
            ORDER BY temperature, ph
        """
        results = db.execute_query(query)
        df = pd.DataFrame(results)
        
        # Convert numeric columns to float (handle Decimal types from MySQL)
        numeric_cols = ['temperature', 'ph', 'nacl_percentage', 'corrosion_rate_mm_per_yr', 'corrosion_rate_mpy']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with NaN in critical columns
        df = df.dropna(subset=['temperature', 'corrosion_rate_mm_per_yr'])
        
        print(f"✅ Loaded {len(df)} samples from database")
        return df
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_ph_vs_corrosion_chart(df):
    """Generate chart: Corrosion Rate vs pH"""
    plt.figure(figsize=(12, 8))
    
    # Filter out NaN values
    ph_df = df[df['ph'].notna() & df['corrosion_rate_mm_per_yr'].notna()].copy()
    
    if len(ph_df) == 0:
        print("⚠️  No pH data available")
        plt.close()
        return
    
    # Group by pH and calculate average
    ph_data = ph_df.groupby('ph')['corrosion_rate_mm_per_yr'].mean().reset_index()
    ph_data = ph_data.sort_values('ph')
    
    # Ensure numeric types
    ph_data['ph'] = pd.to_numeric(ph_data['ph'], errors='coerce')
    ph_data['corrosion_rate_mm_per_yr'] = pd.to_numeric(ph_data['corrosion_rate_mm_per_yr'], errors='coerce')
    ph_data = ph_data.dropna()
    
    if len(ph_data) == 0:
        print("⚠️  No valid pH data after processing")
        plt.close()
        return
    
    plt.plot(ph_data['ph'], ph_data['corrosion_rate_mm_per_yr'], 
             marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
    plt.fill_between(ph_data['ph'], ph_data['corrosion_rate_mm_per_yr'], 
                     alpha=0.3, color='#2E86AB')
    
    plt.xlabel('pH', fontsize=14, fontweight='bold')
    plt.ylabel('Corrosion Rate (mm/year)', fontsize=14, fontweight='bold')
    plt.title('Corrosion Rate vs pH\n' + format_arabic_text('معدل التآكل مقابل درجة الحموضة'), 
              fontsize=16, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '1_corrosion_vs_ph.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def generate_temperature_vs_corrosion_chart(df):
    """Generate chart: Corrosion Rate vs Temperature"""
    plt.figure(figsize=(12, 8))
    
    # Filter out NaN values
    temp_df = df[df['temperature'].notna() & df['corrosion_rate_mm_per_yr'].notna()].copy()
    
    if len(temp_df) == 0:
        print("⚠️  No temperature data available")
        plt.close()
        return
    
    # Group by temperature and calculate average
    temp_data = temp_df.groupby('temperature')['corrosion_rate_mm_per_yr'].mean().reset_index()
    temp_data = temp_data.sort_values('temperature')
    
    # Ensure numeric types
    temp_data['temperature'] = pd.to_numeric(temp_data['temperature'], errors='coerce')
    temp_data['corrosion_rate_mm_per_yr'] = pd.to_numeric(temp_data['corrosion_rate_mm_per_yr'], errors='coerce')
    temp_data = temp_data.dropna()
    
    if len(temp_data) == 0:
        print("⚠️  No valid temperature data after processing")
        plt.close()
        return
    
    plt.plot(temp_data['temperature'], temp_data['corrosion_rate_mm_per_yr'], 
             marker='s', linewidth=2.5, markersize=8, color='#A23B72')
    plt.fill_between(temp_data['temperature'], temp_data['corrosion_rate_mm_per_yr'], 
                     alpha=0.3, color='#A23B72')
    
    plt.xlabel('Temperature (°C)', fontsize=14, fontweight='bold')
    plt.ylabel('Corrosion Rate (mm/year)', fontsize=14, fontweight='bold')
    plt.title('Corrosion Rate vs Temperature\n' + format_arabic_text('معدل التآكل مقابل درجة الحرارة'), 
              fontsize=16, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '2_corrosion_vs_temperature.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def generate_medium_vs_corrosion_chart(df):
    """Generate chart: Corrosion Rate vs Medium"""
    plt.figure(figsize=(14, 8))
    
    # Filter out NaN values
    medium_df = df[df['medium'].notna() & df['corrosion_rate_mm_per_yr'].notna()].copy()
    
    if len(medium_df) == 0:
        print("⚠️  No medium data available")
        plt.close()
        return
    
    # Group by medium and calculate average
    medium_data = medium_df.groupby('medium')['corrosion_rate_mm_per_yr'].mean().reset_index()
    medium_data['corrosion_rate_mm_per_yr'] = pd.to_numeric(medium_data['corrosion_rate_mm_per_yr'], errors='coerce')
    medium_data = medium_data.dropna()
    medium_data = medium_data.sort_values('corrosion_rate_mm_per_yr', ascending=False)
    medium_data = medium_data.head(10)  # Top 10 mediums
    
    if len(medium_data) == 0:
        print("⚠️  No valid medium data after processing")
        plt.close()
        return
    
    colors = sns.color_palette("husl", len(medium_data))
    bars = plt.bar(range(len(medium_data)), medium_data['corrosion_rate_mm_per_yr'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, medium_data['corrosion_rate_mm_per_yr'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xlabel('Medium/Environment', fontsize=14, fontweight='bold')
    plt.ylabel('Average Corrosion Rate (mm/year)', fontsize=14, fontweight='bold')
    plt.title('Corrosion Rate vs Medium\n' + format_arabic_text('معدل التآكل مقابل الوسط'), 
              fontsize=16, fontweight='bold', pad=20)
    plt.xticks(range(len(medium_data)), medium_data['medium'], rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '3_corrosion_vs_medium.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def generate_material_comparison_chart(df):
    """Generate chart: Material Comparison"""
    plt.figure(figsize=(12, 8))
    
    # Filter out NaN values
    material_df = df[df['material'].notna() & df['corrosion_rate_mm_per_yr'].notna()].copy()
    
    if len(material_df) == 0:
        print("⚠️  No material data available")
        plt.close()
        return
    
    # Group by material and calculate statistics
    material_data = material_df.groupby('material').agg({
        'corrosion_rate_mm_per_yr': ['mean', 'count']
    }).reset_index()
    material_data.columns = ['material', 'avg_rate', 'count']
    material_data['avg_rate'] = pd.to_numeric(material_data['avg_rate'], errors='coerce')
    material_data = material_data.dropna()
    material_data = material_data.sort_values('avg_rate', ascending=False)
    
    if len(material_data) == 0:
        print("⚠️  No valid material data after processing")
        plt.close()
        return
    
    colors = ['#F18F01' if 'X65' in mat.upper() or 'API' in mat.upper() 
              else '#C73E1D' for mat in material_data['material']]
    
    bars = plt.barh(range(len(material_data)), material_data['avg_rate'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (bar, value, count) in enumerate(zip(bars, material_data['avg_rate'], 
                                                  material_data['count'])):
        plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{value:.4f} mm/yr (n={count})', 
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.ylabel('Material Type', fontsize=14, fontweight='bold')
    plt.xlabel('Average Corrosion Rate (mm/year)', fontsize=14, fontweight='bold')
    plt.title('Material Comparison\n' + format_arabic_text('مقارنة المواد'), 
              fontsize=16, fontweight='bold', pad=20)
    plt.yticks(range(len(material_data)), material_data['material'])
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '4_material_comparison.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def generate_nacl_vs_corrosion_chart(df):
    """Generate chart: Corrosion Rate vs NaCl Concentration"""
    plt.figure(figsize=(12, 8))
    
    # Filter data with NaCl percentage
    nacl_data = df[df['nacl_percentage'].notna()].copy()
    if len(nacl_data) > 0:
        nacl_grouped = nacl_data.groupby('nacl_percentage')['corrosion_rate_mm_per_yr'].mean().reset_index()
        nacl_grouped = nacl_grouped.sort_values('nacl_percentage')
        
        plt.scatter(nacl_grouped['nacl_percentage'], nacl_grouped['corrosion_rate_mm_per_yr'], 
                   s=100, alpha=0.7, color='#06A77D', edgecolors='black', linewidth=2)
        
        # Add trend line
        z = np.polyfit(nacl_grouped['nacl_percentage'], nacl_grouped['corrosion_rate_mm_per_yr'], 1)
        p = np.poly1d(z)
        plt.plot(nacl_grouped['nacl_percentage'], p(nacl_grouped['nacl_percentage']), 
                "r--", alpha=0.8, linewidth=2, label='Trend Line')
        
        plt.xlabel('NaCl Concentration (%)', fontsize=14, fontweight='bold')
        plt.ylabel('Corrosion Rate (mm/year)', fontsize=14, fontweight='bold')
        plt.title('Corrosion Rate vs NaCl Concentration\n' + format_arabic_text('معدل التآكل مقابل تركيز كلوريد الصوديوم'), 
                  fontsize=16, fontweight='bold', pad=20)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = os.path.join(output_dir, '5_corrosion_vs_nacl.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {filename}")
    else:
        print("⚠️  No NaCl data available")
    plt.close()

def generate_3d_surface_plot(df):
    """Generate 3D surface plot: Temperature vs pH vs Corrosion Rate"""
    from mpl_toolkits.mplot3d import Axes3D
    
    # Filter out NaN values
    plot_df = df[df['temperature'].notna() & df['ph'].notna() & df['corrosion_rate_mm_per_yr'].notna()].copy()
    
    if len(plot_df) == 0:
        print("⚠️  No data available for 3D plot")
        plt.close()
        return
    
    # Ensure numeric types
    plot_df['temperature'] = pd.to_numeric(plot_df['temperature'], errors='coerce')
    plot_df['ph'] = pd.to_numeric(plot_df['ph'], errors='coerce')
    plot_df['corrosion_rate_mm_per_yr'] = pd.to_numeric(plot_df['corrosion_rate_mm_per_yr'], errors='coerce')
    plot_df = plot_df.dropna()
    
    if len(plot_df) == 0:
        print("⚠️  No valid data for 3D plot after processing")
        plt.close()
        return
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create meshgrid
    temp_range = np.linspace(plot_df['temperature'].min(), plot_df['temperature'].max(), 20)
    ph_range = np.linspace(plot_df['ph'].min(), plot_df['ph'].max(), 20)
    T, P = np.meshgrid(temp_range, ph_range)
    
    # Calculate average corrosion rate for each combination
    Z = np.zeros_like(T)
    for i in range(len(ph_range)):
        for j in range(len(temp_range)):
            subset = plot_df[(plot_df['ph'].between(ph_range[i]-0.5, ph_range[i]+0.5)) & 
                           (plot_df['temperature'].between(temp_range[j]-5, temp_range[j]+5))]
            if len(subset) > 0:
                Z[i, j] = subset['corrosion_rate_mm_per_yr'].mean()
            else:
                Z[i, j] = plot_df['corrosion_rate_mm_per_yr'].mean()
    
    surf = ax.plot_surface(T, P, Z, cmap='viridis', alpha=0.8, edgecolor='none')
    ax.set_xlabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('pH', fontsize=12, fontweight='bold')
    ax.set_zlabel('Corrosion Rate (mm/year)', fontsize=12, fontweight='bold')
    ax.set_title('3D Surface: Corrosion Rate vs Temperature & pH\n' +
                 format_arabic_text('السطح ثلاثي الأبعاد: معدل التآكل مقابل درجة الحرارة و pH'), 
                 fontsize=14, fontweight='bold', pad=20)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '6_3d_surface_plot.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def generate_statistics_summary(df):
    """Generate statistics summary table as image"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Ensure numeric types for calculations
    df_numeric = df.copy()
    df_numeric['corrosion_rate_mm_per_yr'] = pd.to_numeric(df_numeric['corrosion_rate_mm_per_yr'], errors='coerce')
    df_numeric['temperature'] = pd.to_numeric(df_numeric['temperature'], errors='coerce')
    df_numeric['ph'] = pd.to_numeric(df_numeric['ph'], errors='coerce')
    
    # Calculate statistics
    stats_data = {
        'Metric': [
            'Total Samples',
            'Average Corrosion Rate (mm/yr)',
            'Min Corrosion Rate (mm/yr)',
            'Max Corrosion Rate (mm/yr)',
            'Std Deviation (mm/yr)',
            'Average Temperature (°C)',
            'Average pH',
            'Number of Materials',
            'Number of Mediums'
        ],
        'Value': [
            len(df),
            f"{df_numeric['corrosion_rate_mm_per_yr'].mean():.4f}" if df_numeric['corrosion_rate_mm_per_yr'].notna().any() else "N/A",
            f"{df_numeric['corrosion_rate_mm_per_yr'].min():.4f}" if df_numeric['corrosion_rate_mm_per_yr'].notna().any() else "N/A",
            f"{df_numeric['corrosion_rate_mm_per_yr'].max():.4f}" if df_numeric['corrosion_rate_mm_per_yr'].notna().any() else "N/A",
            f"{df_numeric['corrosion_rate_mm_per_yr'].std():.4f}" if df_numeric['corrosion_rate_mm_per_yr'].notna().any() else "N/A",
            f"{df_numeric['temperature'].mean():.2f}" if df_numeric['temperature'].notna().any() else "N/A",
            f"{df_numeric['ph'].mean():.2f}" if df_numeric['ph'].notna().any() else "N/A",
            df['material'].nunique() if 'material' in df.columns else 0,
            df['medium'].nunique() if 'medium' in df.columns else 0
        ]
    }
    
    table = ax.table(cellText=[[stats_data['Metric'][i], stats_data['Value'][i]] 
                               for i in range(len(stats_data['Metric']))],
                    colLabels=['Metric / ' + format_arabic_text('المؤشر'), 
                              'Value / ' + format_arabic_text('القيمة')],
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.6, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5)
    
    # Style the table
    for i in range(len(stats_data['Metric'])):
        if i % 2 == 0:
            table[(i+1, 0)].set_facecolor('#E8E8E8')
            table[(i+1, 1)].set_facecolor('#E8E8E8')
    
    table[(0, 0)].set_facecolor('#2E86AB')
    table[(0, 1)].set_facecolor('#2E86AB')
    table[(0, 0)].set_text_props(weight='bold', color='white')
    table[(0, 1)].set_text_props(weight='bold', color='white')
    
    plt.title('Statistical Summary\n' + format_arabic_text('الملخص الإحصائي'), 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '7_statistics_summary.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def generate_correlation_heatmap(df):
    """Generate correlation heatmap"""
    plt.figure(figsize=(10, 8))
    
    # Select numeric columns and convert to numeric
    numeric_cols = ['temperature', 'ph', 'nacl_percentage', 'corrosion_rate_mm_per_yr']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_cols) < 2:
        print("⚠️  Not enough numeric columns for correlation heatmap")
        plt.close()
        return
    
    # Convert to numeric
    corr_df = df[available_cols].copy()
    for col in available_cols:
        corr_df[col] = pd.to_numeric(corr_df[col], errors='coerce')
    
    corr_df = corr_df.dropna()
    
    if len(corr_df) == 0:
        print("⚠️  No valid data for correlation heatmap")
        plt.close()
        return
    
    corr_data = corr_df.corr()
    
    sns.heatmap(corr_data, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                vmin=-1, vmax=1)
    
    plt.title('Correlation Matrix\n' + format_arabic_text('مصفوفة الارتباط'), 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '8_correlation_heatmap.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    plt.close()

def main():
    """Main function to generate all visualizations"""
    print("=" * 60)
    print("Generating Research Paper Visualizations")
    print("إنشاء الرسوم البيانية للورقة البحثية")
    print("=" * 60)
    
    # Fetch data
    df = fetch_data()
    if df is None or len(df) == 0:
        print("❌ No data available. Please upload CSV files first.")
        return
    
    print(f"\n📊 Generating visualizations from {len(df)} samples...\n")
    
    # Generate all charts
    try:
        generate_ph_vs_corrosion_chart(df)
        generate_temperature_vs_corrosion_chart(df)
        generate_medium_vs_corrosion_chart(df)
        generate_material_comparison_chart(df)
        generate_nacl_vs_corrosion_chart(df)
        generate_3d_surface_plot(df)
        generate_statistics_summary(df)
        generate_correlation_heatmap(df)
        
        print("\n" + "=" * 60)
        print("✅ All visualizations generated successfully!")
        print(f"📁 Output directory: {os.path.abspath(output_dir)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

