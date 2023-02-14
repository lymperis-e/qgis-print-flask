import os, sys
from flask import Flask, request, jsonify, send_file
from qgis.core import QgsApplication, QgsProject, QgsRectangle, QgsLayoutExporter
from qgis.gui import QgsMapCanvas

from .proj import reproject

app = Flask(__name__)

# Instruct QT to not search for a screen
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Supply path to qgis install location
QgsApplication.setPrefixPath("/usr/bin/qgis", True)





@app.route('/getrender', methods=['GET'])
def getrender():
    project_dir=os.path.join("home/qgis_print_server","projects")
    data = {
        "project_name": "/home/qgis_print_server/projects/SERVER_RENDER.qgz",
        "layout_name": "IOANNINA",
        "format":"pdf",
        "xmin":  22.50878146720017,    #329907.4057676004,     
        "ymin":  37.65003529415282,    #4056551.255452606,     
        "xmax":  23.190124526380057,    #368004.1095487627,     
        "ymax":  38.35092957001984    #4105624.138518973      
    }
   
    try:
        # Reprojct points to Project CRS
        coord_min = reproject(data["xmin"], data["ymin"])
        coord_max = reproject(data["xmax"], data["ymax"])

        print(coord_min)
        print(coord_max)


        # Initialize QGIS
        qgs = QgsApplication([], False)
        qgs.initQgis()

        # Load the project
        project = QgsProject.instance()
        project.read(data['project_name'])


        # Set the map bounds
        canvas = QgsMapCanvas()
        rect = QgsRectangle(coord_min['x'], coord_min['y'], coord_max['x'], coord_max['y'])
        #rect = QgsRectangle(data['xmin'], data['ymin'], data['xmax'], data['ymax'])
        #canvas.setExtent(rect)
        canvas.refresh()

        

        # Print layout
        layout_manager = project.layoutManager()
        layout = layout_manager.layoutByName(data['layout_name'])



        # Get layout map -----------------
        #l_map = layout.referenceMap()
        l_map = layout.itemById('Map 1')
        l_map.zoomToExtent(rect)
        l_map.refresh()

        # Change Title Text
        #TODO
        title = layout.itemById('title')
        title.setText('KORINTHOS')

        #############################################

        exporter = QgsLayoutExporter(layout)
        if data['format'] == "pdf":
            outfile = "/home/qgis_print_server/exports/test.pdf"
            exporter.exportToPdf(outfile, QgsLayoutExporter.PdfExportSettings())
        else:
            outfile = "/home/qgis_print_server/exports/test.png"
            exporter.exportToImage(outfile, QgsLayoutExporter.ImageExportSettings())



        # Exit QGIS
        qgs.exitQgis()
        #return jsonify(status='success')
        return send_file(outfile)

    except Exception as e:
        # Exit QGIS
        qgs.exitQgis()
        return jsonify(status='error', message=str(e))




@app.route('/coordinates', methods=['POST'])
def coordinates():
    params = request.get_json()

    xmin = params['xmin'] #lng
    xmax = params['xmax'] 
    ymin = params['ymin'] #lat
    ymax = params['ymax']
    r_title = params['title']

    project_dir=os.path.join("home/qgis_print_server","projects")
    data = {
        "project_name": "/home/qgis_print_server/projects/SERVER_RENDER.qgz",
        "layout_name": "IOANNINA",
        "format":"pdf",
        "xmin":  xmin, #22.50878146720017,    #329907.4057676004,     
        "ymin":  ymin, #37.65003529415282,    #4056551.255452606,     
        "xmax":  xmax, #23.190124526380057,    #368004.1095487627,     
        "ymax":  ymax #38.35092957001984    #4105624.138518973      
    }
   
    try:
        # Reprojct points to Project CRS
        coord_min = reproject(data["xmin"], data["ymin"])
        coord_max = reproject(data["xmax"], data["ymax"])

        print(coord_min)
        print(coord_max)


        # Initialize QGIS
        qgs = QgsApplication([], False)
        qgs.initQgis()

        # Load the project
        project = QgsProject.instance()
        project.read(data['project_name'])


        # Set the map bounds
        canvas = QgsMapCanvas()
        rect = QgsRectangle(coord_min['x'], coord_min['y'], coord_max['x'], coord_max['y'])
        canvas.refresh()


        # Print layout
        layout_manager = project.layoutManager()
        layout = layout_manager.layoutByName(data['layout_name'])


        # Change layout map -----------------
        l_map = layout.itemById('Map 1')
        l_map.zoomToExtent(rect)
        l_map.refresh()

        # Change Title Text
        title = layout.itemById('title')
        title.setText(r_title)



        exporter = QgsLayoutExporter(layout)
        if data['format'] == "pdf":
            outfile = "/home/qgis_print_server/exports/test.pdf"
            exporter.exportToPdf(outfile, QgsLayoutExporter.PdfExportSettings())
        else:
            outfile = "/home/qgis_print_server/exports/test.png"
            exporter.exportToImage(outfile, QgsLayoutExporter.ImageExportSettings())



        # Exit QGIS
        qgs.exitQgis()
        #return jsonify(status='success')
        return send_file(outfile, mimetype='application/pdf')

    except Exception as e:
        # Exit QGIS
        qgs.exitQgis()
        return jsonify(status='error', message=str(e))






if __name__ == '__main__':
    app.run(debug=True)

























