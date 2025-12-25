## Bivariate Legend Box Generator (3x3 Grid Shapefile)
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterEnum,
    QgsProcessingParameterNumber, QgsProcessingParameterVectorDestination,
    QgsProcessingParameterString,
    QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsField,
    QgsVectorFileWriter, QgsCoordinateReferenceSystem, QgsFields,
    QgsFillSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer,
    QgsWkbTypes, QgsProcessingException
)
from qgis.PyQt.QtGui import QColor

# ---------- Color Palettes ----------
PALETTE_PURPLE_BLUE = {
    11: ('#E8E8E8', 'Low A, Low B'),
    12: ('#ADE2E5', 'Low A, Medium B'),
    13: ('#5AC8C9', 'Low A, High B'),
    21: ('#DEB0D5', 'Medium A, Low B'),
    22: ('#A4ADD1', 'Medium A, Medium B'),
    23: ('#5399B8', 'Medium A, High B'),
    31: ('#BE64AC', 'High A, Low B'),
    32: ('#8C62AA', 'High A, Medium B'),
    33: ('#3A4893', 'High A, High B'),
}

PALETTE_ORANGE_GREEN = {
    11: ('#D3D3D3', 'Low A, Low B'),
    12: ('#7FBBD2', 'Low A, Medium B'),
    13: ('#149ED0', 'Low A, High B'),
    21: ('#D9A386', 'Medium A, Low B'),
    22: ('#819084', 'Medium A, Medium B'),
    23: ('#147884', 'Medium A, High B'),
    31: ('#DE692A', 'High A, Low B'),
    32: ('#855E28', 'High A, Medium B'),
    33: ('#164E28', 'High A, High B'),
}

COLOR_PALETTES = {
    'purple_blue': PALETTE_PURPLE_BLUE,
    'orange_green': PALETTE_ORANGE_GREEN,
}


class BivariateLegendBoxGenerator(QgsProcessingAlgorithm):
    # Parameters
    PALETTE_CHOICE = 'PALETTE_CHOICE'
    CUSTOM_COLORS = 'CUSTOM_COLORS'
    BOX_SIZE = 'BOX_SIZE'
    SPACING = 'SPACING'
    OUTPUT = 'OUTPUT'

    def tr(self, text):
        return QCoreApplication.translate('BivariateLegendBoxGenerator', text)

    def createInstance(self):
        return BivariateLegendBoxGenerator()

    def name(self):
        return 'bivariate_legend_box_generator'

    def displayName(self):
        return self.tr('Bivariate Legend Box Generator (3×3)')

    def group(self):
        return self.tr('Vector – Bivariate')

    def groupId(self):
        return 'vector_bivariate'

    def shortHelpString(self):
        return self.tr(
            'Generates a 3×3 grid of square boxes as a shapefile for bivariate legend. '
            'Each box represents a combination of Low/Medium/High for two variables (A and B). '
            'Choose from different color palettes or provide custom colors.\n\n'
            'Custom Colors: Enter 9 hex codes separated by commas (from bottom-left to top-right, row by row).\n'
            'Order: 11, 12, 13, 21, 22, 23, 31, 32, 33\n'
            'Example: #E9E9EB, #A3C6DA, #55A5C7, #ECD088, #A6B37E, #579574, #F5B903, #AEA003, #5D8103'
        )

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterEnum(
            self.PALETTE_CHOICE,
            self.tr('Color Palette'),
            options=['Blue-Purple', 'Blue-Orange-Green', 'Custom (use hex codes below)'],
            defaultValue=0,
            optional=False
        ))

        self.addParameter(QgsProcessingParameterString(
            self.CUSTOM_COLORS,
            self.tr('Custom Colors (9 hex codes, comma-separated)'),
            defaultValue='#E9E9EB, #A3C6DA, #55A5C7, #ECD088, #A6B37E, #579574, #F5B903, #AEA003, #5D8103',
            optional=True,
            multiLine=False
        ))

        self.addParameter(QgsProcessingParameterNumber(
            self.BOX_SIZE,
            self.tr('Box Size (map units)'),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1.0,
            minValue=0.1
        ))

        self.addParameter(QgsProcessingParameterNumber(
            self.SPACING,
            self.tr('Spacing between boxes (map units)'),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.1,
            minValue=0.0
        ))

        self.addParameter(QgsProcessingParameterVectorDestination(
            self.OUTPUT,
            self.tr('Output Legend Boxes (Shapefile)'),
            type=QgsProcessing.TypeVectorPolygon
        ))

    def parse_custom_colors(self, color_string, feedback):
        """Parse comma-separated hex color codes and create a palette dictionary."""
        # Clean and split the input
        colors = [c.strip().upper() for c in color_string.split(',')]
        
        # Validate we have exactly 9 colors
        if len(colors) != 9:
            raise QgsProcessingException(
                f'Expected 9 hex codes, but got {len(colors)}. '
                'Please provide exactly 9 colors separated by commas.'
            )
        
        # Validate hex format
        for i, color in enumerate(colors):
            if not color.startswith('#'):
                color = '#' + color
                colors[i] = color
            
            if len(color) != 7:
                raise QgsProcessingException(
                    f'Invalid hex code: {color}. '
                    'Each color must be in format #RRGGBB (e.g., #E9E9EB)'
                )
            
            # Validate hex characters
            try:
                int(color[1:], 16)
            except ValueError:
                raise QgsProcessingException(
                    f'Invalid hex code: {color}. '
                    'Use only valid hexadecimal characters (0-9, A-F)'
                )
        
        # Map colors to bivariate codes (11-33)
        # Order: 11, 12, 13, 21, 22, 23, 31, 32, 33
        codes = [11, 12, 13, 21, 22, 23, 31, 32, 33]
        a_levels = ['Low', 'Medium', 'High']
        b_levels = ['Low', 'Medium', 'High']
        
        palette = {}
        for i, code in enumerate(codes):
            a_idx = (code // 10) - 1  # Get A level (1-3 -> 0-2)
            b_idx = (code % 10) - 1   # Get B level (1-3 -> 0-2)
            label = f'{a_levels[a_idx]} A, {b_levels[b_idx]} B'
            palette[code] = (colors[i], label)
            feedback.pushInfo(f'Code {code}: {colors[i]} - {label}')
        
        return palette

    def processAlgorithm(self, parameters, context, feedback):
        # Get parameters
        palette_index = self.parameterAsInt(parameters, self.PALETTE_CHOICE, context)
        custom_colors = self.parameterAsString(parameters, self.CUSTOM_COLORS, context)
        box_size = self.parameterAsDouble(parameters, self.BOX_SIZE, context)
        spacing = self.parameterAsDouble(parameters, self.SPACING, context)
        output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        # Select or create palette
        if palette_index == 2:  # Custom colors
            feedback.pushInfo('Using custom color palette...')
            if not custom_colors or custom_colors.strip() == '':
                raise QgsProcessingException(
                    'Custom colors option selected but no colors provided. '
                    'Please enter 9 hex codes separated by commas.'
                )
            selected_palette = self.parse_custom_colors(custom_colors, feedback)
        else:  # Predefined palettes
            palette_keys = ['purple_blue', 'orange_green']
            selected_palette = COLOR_PALETTES[palette_keys[palette_index]]
            feedback.pushInfo(f'Using {palette_keys[palette_index]} palette')

        # Create fields for the legend layer
        fields = QgsFields()
        fields.append(QgsField('code', QVariant.Int))
        fields.append(QgsField('label', QVariant.String))
        fields.append(QgsField('color', QVariant.String))
        fields.append(QgsField('a_class', QVariant.String))
        fields.append(QgsField('b_class', QVariant.String))

        # Create vector file writer
        crs = QgsCoordinateReferenceSystem('EPSG:4326')  # Default CRS
        
        # Determine file format from output path
        if output_path.lower().endswith('.gpkg'):
            driver_name = 'GPKG'
        elif output_path.lower().endswith('.shp'):
            driver_name = 'ESRI Shapefile'
        else:
            driver_name = 'GPKG'  # Default to GeoPackage
        
        writer = QgsVectorFileWriter(
            output_path,
            'UTF-8',
            fields,
            QgsWkbTypes.Polygon,
            crs,
            driver_name
        )

        if writer.hasError() != QgsVectorFileWriter.NoError:
            raise QgsProcessingException(f'Error creating vector file: {writer.errorMessage()}')

        # Generate 3x3 grid
        step = box_size + spacing
        a_levels = ['Low', 'Medium', 'High']
        b_levels = ['Low', 'Medium', 'High']

        feedback.pushInfo('Generating 3×3 legend boxes...')

        for row in range(3):  # B axis (bottom to top)
            for col in range(3):  # A axis (left to right)
                # Calculate bivariate code: A=1-3 (col), B=1-3 (row)
                a_val = col + 1
                b_val = row + 1
                code = a_val * 10 + b_val

                # Get color and label from palette
                if code not in selected_palette:
                    continue

                color_hex, default_label = selected_palette[code]

                # Calculate box coordinates (origin at 0,0, B increases upward)
                x_min = col * step
                y_min = row * step
                x_max = x_min + box_size
                y_max = y_min + box_size

                # Create square polygon
                points = [
                    QgsPointXY(x_min, y_min),
                    QgsPointXY(x_max, y_min),
                    QgsPointXY(x_max, y_max),
                    QgsPointXY(x_min, y_max),
                    QgsPointXY(x_min, y_min)  # Close the polygon
                ]
                geometry = QgsGeometry.fromPolygonXY([points])

                # Create feature
                feature = QgsFeature(fields)
                feature.setGeometry(geometry)
                feature.setAttribute('code', code)
                feature.setAttribute('label', default_label)
                feature.setAttribute('color', color_hex)
                feature.setAttribute('a_class', a_levels[col])
                feature.setAttribute('b_class', b_levels[row])

                writer.addFeature(feature)

        del writer  # Close the file

        feedback.pushInfo(f'Successfully created 3×3 legend with {len(selected_palette)} boxes')
        feedback.pushInfo(f'Output saved to: {output_path}')

        # Try to load and style the layer
        try:
            layer = QgsVectorLayer(output_path, 'Bivariate Legend', 'ogr')
            if layer.isValid():
                # Create categorized renderer based on the 'code' field
                categories = []
                for code, (color_hex, label) in selected_palette.items():
                    symbol = QgsFillSymbol.createSimple({
                        'color': color_hex,
                        'outline_color': '#000000',
                        'outline_width': '0.2'
                    })
                    category = QgsRendererCategory(code, symbol, label)
                    categories.append(category)

                renderer = QgsCategorizedSymbolRenderer('code', categories)
                layer.setRenderer(renderer)
                
                # Add layer to project
                from qgis.core import QgsProject
                QgsProject.instance().addMapLayer(layer)
                feedback.pushInfo('Layer added to project with categorized styling')
        except Exception as e:
            feedback.pushWarning(f'Could not auto-style layer: {str(e)}')

        return {self.OUTPUT: output_path}


def classFactory(iface=None):
    return BivariateLegendBoxGenerator()
