import os

from pydicom.uid import ImplicitVRLittleEndian, ExplicitVRLittleEndian
from pynetdicom import AE, debug_logger
from pydicom import dcmread
from pydicom.data import get_testdata_file

debug_logger()

ae = AE()
ae.add_requested_context('1.2.840.10008.5.1.4.1.1.4', [ImplicitVRLittleEndian, ExplicitVRLittleEndian]) # MRImageStorage
assoc = ae.associate("127.0.0.1", 4242)
if assoc.is_established:
    print('Association established with Echo SCP!')

    # Read dcm file
    file_path = r"D:/SaigonMec/dicom_research/test_data/dicoogle_dataset/FELIX/" + "IM-0001-0074.dcmfe2f32c2-0564-45a2-9aa7-6c71c6a6913d.dcm"
    ds = dcmread(file_path)

    assoc.send_c_store(ds)
    assoc.release()
else:
    # Association rejected, aborted or never connected
    print('Failed to associate')