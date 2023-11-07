from flask import request, Response, app, Flask, jsonify
from flask_cors import CORS, cross_origin
import os
import pydicom

dicom_storage_dir = r"D:/SaigonMec/dicom_research/python_server/server_data/"
app = Flask(__name__)

RETURN_LIST_FIELDS = ["00080005", "00080020", "00080030", "00080050", "00080060", "00080061", "00080090", "00081030", "00081190",
                      "00100010", "00100020", "00100030", "00100040", "0020000D", "00200010", "00201206", "00201208"]


@app.route('/dicom-web/stow', methods=['POST'])
def stow_rs():
    # Check if the request has DICOM data
    if request.mimetype == 'application/dicom':
        try:
            dicom_instance = pydicom.read_file(request.stream)
            # Generate a unique filename for the DICOM instance
            filename = os.path.join(dicom_storage_dir, f"{dicom_instance.SOPInstanceUID}.dcm")
            with open(filename, 'wb') as file:
                # Save the DICOM instance to the storage directory
                file.write(request.stream.read())
            return Response(status=200)
        except Exception as e:
            # Handle any errors that may occur during storage
            return Response(status=500)
    else:
        # Handle requests without DICOM data
        return Response(status=400)


@app.route('/dicom-web/wado', methods=['GET'])
def wado_rs():
    study_uid = request.args.get('studyUID')
    series_uid = request.args.get('seriesUID')
    sop_instance_uid = request.args.get('objectUID')

    if study_uid and series_uid and sop_instance_uid:
        filename = os.path.join(dicom_storage_dir, f"{sop_instance_uid}.dcm")
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                # Read the DICOM instance and return it
                return Response(file.read(), content_type='application/dicom')

    return Response(status=404)


@app.route('/dicom-web/studies', methods=['GET'])
@cross_origin(origin='*')
def qido_rs():
    json_response = []
    for root, dirs, files in os.walk(dicom_storage_dir):
        for filename in files:
            if not filename.endswith('dcm'):
                continue
            filepath = os.path.join(root, filename)
            dicom_dataset = pydicom.dcmread(filepath)
            dicom_attributes = {}

            for element in dicom_dataset:
                tag = str(element.tag)
                tag_string = f"{element.tag.group:04X}{element.tag.elem:04X}"
                value = element.value
                vr = element.VR

                if tag_string in RETURN_LIST_FIELDS:
                    # Convert MultiValue objects to Python lists
                    # if isinstance(value, pydicom.multival.MultiValue):
                    #     value = list(value)

                    # Check PersonName type
                    if vr == "PN":
                        value = {
                            "Alphabetic": value.alphabetic
                        }

                    dicom_attributes[tag_string] = {
                        "Value": [value],
                        "vr": vr
                    }

            json_response.append(dicom_attributes)

        return jsonify(json_response)
    else:
        return Response(status=404)


if __name__ == "__main__":
    app.run(host="localhost", port=11112, debug=True)