#!/usr/bin/env python3
#coding=utf-8

SUBDIRECTORIO_HTML_AL="al"
SUBDIRECTORIO_HTML_OT="OT"
TIPOS=["Piso", "Casa", "Chalet", "Dúplex", "Ático", "Estudio", "Finca"]
FICHERO_BASE_AL="pagina_{0}.html"

TOTAL_PAGINAS_AL=68
URL_BASE_AL="http://www.idealista.com/"
URL_PAGINAS_AL=URL_BASE_AL+"venta-viviendas/ciudad-real-ciudad-real/pagina-{0}.htm"


OBJETO_DATOS="""
                
                    label: \"{0}\",
                    fill: false,
                    lineTension: 0,
                    backgroundColor: \"rgba(75,192,192,0.4)\",
                    borderColor: \"rgba(75,192,192,1)\",
                    borderCapStyle: \"butt\",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: \"miter\",
                    pointBorderColor: \"rgba(75,192,192,1)\",
                    pointBackgroundColor: \"#fff\",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: \"rgba(75,192,192,1)\",
                    pointHoverBorderColor: \"rgba(220,220,220,1)\",
                    pointHoverBorderWidth: 2,
                    pointRadius: 10,
                    pointHitRadius: 20,
                    data: [{1}],
                
"""
