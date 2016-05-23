#!/usr/bin/env python3
#coding=utf-8

SUBDIRECTORIO_HTML_AL="al"
SUBDIRECTORIO_HTML_TO="to"
TIPOS=["Piso", "Casa", "Chalet", "Dúplex", "Ático", "Estudio", "Finca"]
COLORES_TIPOS=["(142, 11, 11, 1)", "(2015,172,72, 1)", "(22, 22, 100, 1)",
               "(9,114,9, 1)", "(20, 22, 220, 1)", "(90,24, 190, 1)",
               "(205, 72, 72, 1)"]
FICHERO_BASE_AL="pagina_{0}.html"
FICHERO_BASE_TO="pagina_to_{0}.html"

TOTAL_PAGINAS_AL=68
TOTAL_PAGINAS_TO=40
URL_BASE_AL="http://www.idealista.com/"
URL_BASE_TO="http://www.fotocasa.es/"
URL_PAGINAS_TO=URL_BASE_TO+"comprar/casas/ciudad-real-capital/listado?crp={0}"
URL_PAGINAS_AL=URL_BASE_AL+"venta-viviendas/ciudad-real-ciudad-real/pagina-{0}.htm"


OBJETO_DATOS="""
                
                    label: \"{0}\",
                    fill: false,
                    lineTension: 0,
                    backgroundColor: \"rgba{2}\",
                    borderColor: \"rgba{2}\",
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
