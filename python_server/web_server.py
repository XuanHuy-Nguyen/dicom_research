from flask import request, Response, app, Flask, jsonify
import os
import pydicom

dicom_storage_dir = r"D:/SaigonMec/dicom_research/python_server/server_data/"
app = Flask(__name__)

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
def qido_rs():
    # Extract query parameters from the URL
    study_instance_uid = request.args.get('StudyInstanceUID')
    patient_id = request.args.get('PatientID')

    # Perform the query based on the provided parameters
    results = perform_qido_query(study_instance_uid, patient_id)

    if results:
        # Construct the JSON response based on the query results
        json_response = []
        for result in results:
            dicom_dataset = pydicom.dcmread(result['file_path'])
            dicom_attributes = {}

            for element in dicom_dataset:
                tag = str(element.tag)
                value = element.value
                vr = element.VR
                # Convert MultiValue objects to Python lists
                if isinstance(value, pydicom.multival.MultiValue):
                    value = list(value)

                # Ignore PersonName type
                if vr is "PN" and (not isinstance(value, str)):
                    continue
                # Ignore PersonName type
                if isinstance(value, pydicom.Dataset) or isinstance(value, bytes) or vr is'SQ':
                    continue
                dicom_attributes[tag] = {
                    "Value": value,
                    "vr": vr
                }

            json_response.append(dicom_attributes)

        return jsonify(json_response)
    else:
        return Response(status=404)


def perform_qido_query(study_instance_uid, patient_id):
    # Initialize an empty list to store the query results
    query_results = []

    # Iterate over stored DICOM instances and apply the query criteria
    for root, dirs, files in os.walk(dicom_storage_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            dcm = pydicom.dcmread(filepath)

            if (
                (study_instance_uid is None or dcm.get('StudyInstanceUID') == study_instance_uid) and
                (patient_id is None or dcm.get('PatientID') == patient_id)
            ):
                # DICOM instance matches the query criteria
                query_results.append({
                    'file_path': filepath
                })

    return query_results


if __name__ == "__main__":
    app.run(host="localhost", port=11112, debug=True)