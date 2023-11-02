import orthanc
import json
import os
import pprint
import csv
import pydicom

def OnStoredInstance(dicom, instanceId):
    PARSE_DATA = r"/var/lib/orthanc/parse_data"
    
    print('Received instance %s of size %d (transfer syntax %s, SOP class UID %s)' % (
        instanceId, dicom.GetInstanceSize(),
        dicom.GetInstanceMetadata('TransferSyntax'),
        dicom.GetInstanceMetadata('SopClassUid')))

    # Print the origin information
    if dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.DICOM_PROTOCOL:
        print('This instance was received through the DICOM protocol')
    elif dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.REST_API:
        print('This instance was received through the REST API')
        
    # Parse data
    tags = json.loads(dicom.GetInstanceSimplifiedJson())    

    try:
        pt_name = str(tags["PatientName"]).replace(" ","_")
    except (KeyError, AttributeError) as err:
        pt_name = "NA"

    try:
        pt_id = tags["PatientID"]
    except (KeyError, AttributeError) as err:
        pt_id = "NA"

    try:
        pt_sex = tags["PatientSex"]
    except (KeyError, AttributeError) as err:
        pt_sex = "NA"
    # get age info
    try:
        pt_age = tags["PatientAge"][1:3]
    except (KeyError, AttributeError) as err:
        pt_age = "NA"

    try:
        pt_birthdate = tags["PatientBirthDate"]
    except (KeyError, AttributeError) as err:
        pt_birthdate = "NA"
        
    try:
        pt_studydate = tags["StudyDate"]
    except (KeyError, AttributeError) as err:
        pt_studydate = "NA"

    try:
        pt_view = tags["ViewPosition"]
    except (KeyError, AttributeError) as err:
        pt_view = "NA"

    try:
        pt_laterality = tags["ImageLaterality"]
    except (KeyError, AttributeError) as err:
        pt_laterality = "NA"

    try:
        pt_breastimplant = tags["BreastImplantPresent"]
    except (KeyError, AttributeError) as err:
        pt_breastimplant = "NA"

    try:
        pt_institutionname = tags["InstitutionName"]
    except (KeyError, AttributeError) as err:
        pt_institutionname = "NA"

    try:
        pt_inst_address = tags["InstitutionAddress"]
    except (KeyError, AttributeError) as err:
        pt_inst_address = "NA"
    try:
        pt_ins_dep_name = tags["InstitutionalDepartmentName"]
    except (KeyError, AttributeError) as err:
        pt_ins_dep_name = "NA"

    try:
        pt_stationname = tags["Manufacturer"]
    except (KeyError, AttributeError) as err:
        pt_stationname = "NA"

    try:
        pt_photometric_interpretation = tags["PhotometricInterpretation"]
    except (KeyError, AttributeError) as err:
        pt_photometric_interpretation = "NA"
        
    # Create path
    patient_path = os.path.join(PARSE_DATA, pt_name + "_" + pt_id)
    dcm_path = os.path.join(patient_path,'dcm')
    png_path = os.path.join(patient_path,'png')
    
    if not os.path.exists(patient_path):
        os.makedirs(patient_path)
    if not os.path.exists(dcm_path):
        os.makedirs(dcm_path)
    if not os.path.exists(png_path):
        os.makedirs(png_path)
        
    png_image_key = os.path.join(png_path,pt_id+"_"+pt_studydate+"_"+pt_view+"_"+pt_laterality+".png")
    
    # Write CSV
    info = {
        "Name": pt_name,
        "ID": pt_id,
        "Gender": pt_sex,
        "Age": pt_age,
        "Date_of_birth": pt_birthdate,
        "Date_of_examination": pt_studydate,
        "Mammo_view": pt_view,
        "Image_path": png_image_key,
        "Breast_side": pt_laterality,
        "Breast_implant": pt_breastimplant,
        "Institution_name": pt_institutionname,
        "Institution_address": pt_inst_address,
        "Institution_department_name": pt_ins_dep_name,
        "Station_name": pt_stationname,
        "Monotype": pt_photometric_interpretation
    }
    with open(os.path.join(patient_path,"metadata.csv"),"w",newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, info.keys())
        w.writeheader()
        w.writerow(info)
        f.close()
        
    # Write DCM
    # Get the content of the DICOM file
    f = orthanc.GetDicomForInstance(instanceId)
    # Parse it using pydicom
    dicom_content = pydicom.dcmread(io.BytesIO(f))
    dicom_content.save_as(dcm_path + "/" + ds.SOPInstanceUID + ".dcm", write_like_original=False)


    
    orthanc.LogWarning("pt_name: " + pt_name)
    orthanc.LogWarning("pt_id: " + pt_id)
    orthanc.LogWarning("pt_sex: " + pt_sex)
    orthanc.LogWarning("pt_age: " + pt_age)
    orthanc.LogWarning("pt_birthdate: " + pt_birthdate)
            

    # Print the DICOM tags
    pprint.pprint(json.loads(dicom.GetInstanceSimplifiedJson()))


orthanc.RegisterOnStoredInstanceCallback(OnStoredInstance)