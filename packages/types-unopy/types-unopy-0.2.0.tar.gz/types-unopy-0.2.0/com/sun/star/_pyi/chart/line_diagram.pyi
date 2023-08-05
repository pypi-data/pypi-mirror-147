# coding: utf-8
#
# Copyright 2022 :Barry-Thomas-Paul: Moss
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Service Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.chart
import typing
from .chart_axis_x_supplier import ChartAxisXSupplier as ChartAxisXSupplier_a950e4d
from .chart_axis_z_supplier import ChartAxisZSupplier as ChartAxisZSupplier_aa70e4f
from .chart_statistics import ChartStatistics as ChartStatistics_e2190d37
from .chart_two_axis_y_supplier import ChartTwoAxisYSupplier as ChartTwoAxisYSupplier_380d0f88
from .diagram import Diagram as Diagram_844409cf
from .dim3_d_diagram import Dim3DDiagram as Dim3DDiagram_b7a60b60
from .stackable_diagram import StackableDiagram as StackableDiagram_ee760d59
if typing.TYPE_CHECKING:
    from ..awt.size import Size as Size_576707ef
    from ..graphic.x_graphic import XGraphic as XGraphic_a4da0afc

class LineDiagram(ChartAxisXSupplier_a950e4d, ChartAxisZSupplier_aa70e4f, ChartStatistics_e2190d37, ChartTwoAxisYSupplier_380d0f88, Diagram_844409cf, Dim3DDiagram_b7a60b60, StackableDiagram_ee760d59):
    """
    Service Class

    specifies line, spline and symbol diagrams.
    
    **since**
    
        LibreOffice 6.1

    See Also:
        `API LineDiagram <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1chart_1_1LineDiagram.html>`_
    """
    @property
    def Lines(self) -> bool:
        """
        determines if the chart type has lines connecting the data points or contains just symbols.
        """
    @property
    def SplineOrder(self) -> int:
        """
        specifies the power of the polynomials used for spline calculation
        
        This property is only valid for B-splines
        """
    @property
    def SplineResolution(self) -> int:
        """
        determines the number of sampling points of a spline
        """
    @property
    def SplineType(self) -> int:
        """
        determines if the chart is a spline-chart type and specifies the type of splines.
        
        You can set the following values:
        """
    @property
    def SymbolBitmap(self) -> 'XGraphic_a4da0afc':
        """
        Set this property to a graphic object which is then used as symbol for all series.
        
        **since**
        
            LibreOffice 6.1
        """
    @property
    def SymbolBitmapURL(self) -> str:
        """
        Set this property to any valid URL that points to a graphic file.
        
        This graphic is then used as symbol for all series.
        
        When you query this value you get an internal URL of the embedded graphic.
        """
    @property
    def SymbolSize(self) -> 'Size_576707ef':
        """
        specifies the size of symbols in 1/100th of a millimeter.
        """
    @property
    def SymbolType(self) -> int:
        """
        determines which type of symbols are displayed.
        
        In this interface, only the two values ChartSymbolType.NONE and ChartSymbolType.AUTO are supported. Later versions may support the selection of the symbols shape.
        
        If you set this property to ChartSymbolType.AUTO, you can change the symbol shape for objects supporting the service ChartDataPointProperties or ChartDataRowProperties.
        """


