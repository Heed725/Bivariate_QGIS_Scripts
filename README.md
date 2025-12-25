# Bivariate QGIS Scripts

A collection of three QGIS Processing scripts for creating bivariate choropleth maps. These scripts integrate directly into the QGIS Processing Toolbox, streamlining the process of generating bivariate visualizations by automating the creation of raster data, styled layers, and custom legends.

## ✨ Features

- **Seamless QGIS Integration**: Works directly in the Processing Toolbox alongside native QGIS tools
- **Graphical Interface**: User-friendly dialog boxes for all parameters - no coding required
- **Batch Processing Support**: Process multiple datasets efficiently using QGIS batch mode
- **Flexible Classification**: Support for 3x3, 4x4, and custom classification schemes
- **Multiple Color Schemes**: Choose from various sequential and diverging color palettes
- **Automated Styling**: Automatically applies symbology - no manual layer styling needed
- **Custom Legends**: Generates professional bivariate legends ready for print layouts
- **Reproducible Workflow**: Can be automated via Python scripts or QGIS Model Designer

## 📊 What are Bivariate Maps?

Bivariate choropleth maps visualize two variables simultaneously on a single map, using color combinations to show relationships between the variables. Unlike univariate maps that show a single variable, bivariate maps reveal patterns of correlation, agreement, or disagreement between two datasets.

**Common applications include:**
- Comparing socioeconomic indicators with environmental data
- Analyzing health outcomes versus access to services
- Studying electoral results for multiple candidates
- Examining population density alongside infrastructure quality

## 📁 Processing Scripts Overview

This repository contains three QGIS Processing scripts that integrate into your Processing Toolbox. These complementary tools work together to create complete bivariate map visualizations:

### 1. **Bivariate_Raster_Generator.py**
A Processing algorithm that generates the underlying bivariate raster data by combining two input variables into a single classified output.

**Functionality:**
- Takes two input raster or vector layers with quantitative data
- Classifies each variable into categories (typically 3x3 or 4x4 grids)
- Combines classifications into a single bivariate raster layer
- Creates values representing all possible combinations of the two variables
- Outputs a classified raster ready for styling

### 2. **Bivariate_Style_Generator.py**
A Processing algorithm that applies appropriate symbology to bivariate data for visualization.

**Functionality:**
- Generates color schemes optimized for bivariate visualization
- Applies graduated or categorized symbology based on bivariate classes
- Supports various color palettes (sequential, diverging, custom)
- Ensures visual distinction between all bivariate categories
- Automatically styles the output layer

### 3. **Bivariate_Legend_Box_Generator.py**
A Processing algorithm that creates custom legend graphics for bivariate maps.

**Functionality:**
- Generates a 2D legend grid showing color combinations
- Labels axes with variable names and value ranges
- Creates a vector or raster legend that can be added to map layouts
- Provides a clear visual key for interpreting the bivariate map
- Exports legend as a separate layer or graphic file

## 🚀 Getting Started

### Quick Start

1. Install the scripts in your QGIS Processing Toolbox (see Installation below)
2. Open QGIS and load two layers with quantitative data
3. Open Processing Toolbox (`Ctrl+Alt+T` or Processing menu)
4. Find the scripts under **Scripts** section
5. Run them in sequence: Raster Generator → Style Generator → Legend Generator

### Prerequisites

- **QGIS 3.x** (QGIS 3.10 or higher recommended)
- **Python 3.x** (bundled with QGIS)
- Basic understanding of QGIS interface and Processing Toolbox
- Spatial data with at least two quantitative attributes

### Installation

1. **Download the scripts:**
```bash
git clone https://github.com/Heed725/Bivariate_QGIS_Scripts.git
```
Or download as ZIP and extract to your preferred location.

2. **Add scripts to QGIS Processing:**

   **Option A: Copy to Scripts Folder (Recommended)**
   - Copy the three `.py` files to your QGIS Processing Scripts folder:
     - **Windows**: `C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts`
     - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/processing/scripts`
     - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts`
   
   **Option B: Add from Processing Toolbox**
   - Open QGIS
   - Open the **Processing Toolbox** (Processing → Toolbox or `Ctrl+Alt+T`)
   - Click the Python icon at the top of the Processing Toolbox
   - Select **Add Script to Toolbox...**
   - Browse to each `.py` file and add them

3. **Refresh the Processing Toolbox:**
   - The scripts should appear under **Scripts** in the Processing Toolbox
   - If they don't appear, restart QGIS or click the refresh button in the Processing Toolbox

4. **Verify Installation:**
   - Look for the scripts in: **Processing Toolbox → Scripts**
   - They may be grouped under a category like "Bivariate" or appear individually

## 💡 Usage Workflow

### Basic Workflow

These scripts work as standard QGIS Processing algorithms with graphical interfaces:

1. **Prepare Your Data**
   - Load your spatial data layers into QGIS
   - Ensure you have two quantitative variables to visualize
   - Data should be normalized (e.g., rates, percentages, densities) rather than raw counts
   - All layers should be in the same spatial reference system (CRS)

2. **Generate Bivariate Raster**
   - Open **Processing Toolbox** (`Ctrl+Alt+T`)
   - Navigate to **Scripts → Bivariate_Raster_Generator**
   - Configure parameters:
     - Select your first variable layer and field
     - Select your second variable layer and field
     - Choose classification method and number of classes (3x3 or 4x4)
     - Set output location
   - Run the algorithm
   - Output: Single raster layer with bivariate classifications

3. **Apply Bivariate Styling**
   - In **Processing Toolbox**, run **Scripts → Bivariate_Style_Generator**
   - Configure parameters:
     - Input: Bivariate raster from step 2
     - Select color scheme (sequential, diverging, or custom)
     - Choose number of classes to match step 2
   - Run the algorithm
   - Output: Styled layer with bivariate color scheme applied

4. **Create Legend**
   - In **Processing Toolbox**, run **Scripts → Bivariate_Legend_Box_Generator**
   - Configure parameters:
     - Input: Styled bivariate layer
     - Set variable names and labels
     - Choose legend dimensions and style
   - Run the algorithm
   - Output: Legend graphic layer for your map layout

5. **Compose Your Map**
   - Switch to **Print Layout**
   - Add your styled bivariate layer
   - Add the generated legend
   - Add labels, title, and other map elements

### Running from Python Console

You can also run these Processing scripts programmatically:

```python
import processing

# Example: Generate bivariate raster
result = processing.run("script:bivariate_raster_generator", {
    'INPUT1': 'path/to/layer1',
    'FIELD1': 'variable1_field',
    'INPUT2': 'path/to/layer2',
    'FIELD2': 'variable2_field',
    'CLASSES': 3,
    'OUTPUT': 'path/to/output.tif'
})
```

### Batch Processing

Use QGIS Batch Processing to create multiple bivariate maps:
- Right-click any script in Processing Toolbox
- Select **Execute as Batch Process...**
- Configure multiple runs with different input parameters

### Best Practices

- **Choose Related Variables**: Bivariate maps work best when there's a hypothesis about how variables relate
- **Normalize Data**: Always use rates or proportions, not raw counts
- **Limit Categories**: Stick to 3x3 or 4x4 classifications (9 or 16 categories maximum)
- **Select Appropriate Colors**: Use diverging or sequential color schemes that remain distinguishable
- **Label Clearly**: Ensure your legend explains what each color combination represents

## 🎨 Color Scheme Recommendations

Popular bivariate color schemes include:
- **Purple-Green**: Good for showing positive/negative relationships
- **Blue-Orange**: High contrast for clear distinction
- **Pink-Blue**: Effective for showing agreement/disagreement
- **Brown-Blue**: Natural-feeling scheme for environmental data

## 📚 Additional Resources

### Bivariate Mapping Tutorials
- [Joshua Stevens - Make a Bivariate Choropleth Map](https://www.joshuastevens.net/cartography/make-a-bivariate-choropleth-map/)
- [BNHR - Bivariate Choropleths in QGIS](https://bnhr.xyz/2019/09/15/bivariate-choropleths-in-qgis.html)
- [Geoawesome - Understanding Bivariate Maps](https://geoawesome.com/understanding-bivariate-maps-a-how-to-guide/)

### QGIS Plugins
- **Bivariate Legend Plugin**: Automated legend creation for bivariate maps
- **Bivariate Renderer**: Additional rendering options for bivariate data

### Processing Framework
- [QGIS Processing Framework Documentation](https://docs.qgis.org/latest/en/docs/user_manual/processing/intro.html)
- [Writing Processing Scripts](https://docs.qgis.org/latest/en/docs/user_manual/processing/scripts.html)
- [Processing Script Examples](https://github.com/qgis/QGIS/tree/master/python/plugins/processing/script)

## ⚙️ Technical Details

### Processing Script Framework

These scripts are built using the QGIS Processing framework, which provides:
- Standardized parameter handling and validation
- Integration with QGIS Model Designer
- Support for batch processing operations
- Automatic progress reporting and cancellation
- Compatibility with Processing algorithms from other plugins

### Script Requirements

Each script implements the `QgsProcessingAlgorithm` interface and includes:
- Parameter definitions (input layers, fields, options)
- Processing logic for bivariate calculations
- Output generation and styling
- Help documentation accessible from the Processing dialog

## 🤝 Contributing

Contributions are welcome! If you have improvements or additional scripts to add:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is open source. Please check individual script headers for specific licensing information.

## 👤 Author

**Heed725**
- GitHub: [@Heed725](https://github.com/Heed725)

## 🐛 Issues and Support

### Troubleshooting

**Scripts don't appear in Processing Toolbox:**
- Verify files are in the correct scripts folder
- Restart QGIS
- Check the QGIS Python console for any error messages
- Ensure scripts have `.py` extension

**Script fails to run:**
- Check that input layers have the required fields
- Verify your data is in a projected CRS (not geographic/WGS84)
- Ensure sufficient disk space for output files
- Review the Processing log for detailed error messages

**Colors don't look right:**
- Verify you're using the same number of classes in all three scripts
- Check that your input data is normalized (rates, not raw counts)
- Try a different color scheme option

### Getting Help

If you encounter issues or have questions:
- Open an issue in the [GitHub Issues](https://github.com/Heed725/Bivariate_QGIS_Scripts/issues) section
- Provide details about:
  - Your QGIS version
  - Data format and structure
  - Complete error messages from the Processing log
  - Steps to reproduce the problem

## 📖 Citation

If you use these scripts in your research or projects, please consider citing this repository:

```
Heed725. (2025). Bivariate QGIS Scripts. GitHub. https://github.com/Heed725/Bivariate_QGIS_Scripts
```

---

**Note**: These are QGIS Processing scripts designed for QGIS 3.x. They integrate directly into the Processing Toolbox for a seamless user experience.

## 🔄 Version History

- **Initial Release**: Core functionality for bivariate raster generation, styling, and legend creation
- Repository maintained and updated as needed

---

*Happy Mapping! 🗺️*
