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
from .chart_axis_x_supplier import ChartAxisXSupplier as ChartAxisXSupplier_a950e4d
from .chart_statistics import ChartStatistics as ChartStatistics_e2190d37
from .chart_two_axis_y_supplier import ChartTwoAxisYSupplier as ChartTwoAxisYSupplier_380d0f88
from .diagram import Diagram as Diagram_844409cf
from .x_statistic_display import XStatisticDisplay as XStatisticDisplay_fdf40e00

class StockDiagram(ChartAxisXSupplier_a950e4d, ChartStatistics_e2190d37, ChartTwoAxisYSupplier_380d0f88, Diagram_844409cf, XStatisticDisplay_fdf40e00):
    """
    Service Class

    specifies a diagram which can be used for presenting stock quotes.
    
    Note that the data must have a specific structure for stock diagrams. Let us assume that data is interpreted, such that series are taken from columns (see property Diagram.DataRowSource). Then you need tables of the following structures for different types:
    
    StockDiagram.Volume is FALSE
    StockDiagram.UpDown is FALSE
    
    StockDiagram.Volume is TRUE
    StockDiagram.UpDown is FALSE
    
    StockDiagram.Volume is FALSE
    StockDiagram.UpDown is TRUE
    
    StockDiagram.Volume is TRUE
    StockDiagram.UpDown is TRUE

    See Also:
        `API StockDiagram <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1chart_1_1StockDiagram.html>`_
    """
    @property
    def UpDown(self) -> bool:
        """
        indicates if a stock chart contains data representing the value of stocks on the opening and closing date.
        
        The difference will be indicated by bars. The color of the bar will be significant for positive or negative differences between open and closed data.
        
        If this property is FALSE, the values of the first series (or second if StockDiagram.Volume is TRUE) of the chart data are interpreted as the day's lowest value. The next series is interpreted as the day's highest value, and the last series is interpreted as the closing value.
        
        If this property is set to TRUE, one additional series is needed with the opening value of the stocks. It is assumed as the series before the series with the day's lowest value.
        """
    @property
    def Volume(self) -> bool:
        """
        indicates if a stock chart contains data representing the volume of stocks.
        
        The values of the volume are represented as columns like those of a BarDiagram.
        
        If this property is set to TRUE, the values of the first series of the chart data are interpreted as volume.
        """


