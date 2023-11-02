import os
from pydicom import dcmread, Dataset
from pydicom.uid import ExplicitVRLittleEndian, ExplicitVRBigEndian, ImplicitVRLittleEndian
from pynetdicom import AE, debug_logger, evt, StoragePresentationContexts

debug_logger()
SERVER_DATA = r"D:/SaigonMec/dicom_research/python_server/server_data/"

transfer = [ExplicitVRLittleEndian, ExplicitVRBigEndian, ImplicitVRLittleEndian]

# Define protocol
ae = AE()


ae.add_supported_context("1.2.840.10008.5.1.4.1.1.4", transfer)  # MRImageStorage
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.2", transfer)  # CTImageStorage

ae.add_supported_context("1.2.840.10008.5.1.4.1.2.1.1", transfer)  # PatientRootQueryRetrieveInformationModelFind
ae.add_supported_context("1.2.840.10008.5.1.4.1.2.1.3", transfer)  # PatientRootQueryRetrieveInformationModelGet
ae.add_supported_context("1.2.840.10008.5.1.4.1.2.1.2", transfer)  # PatientRootQueryRetrieveInformationModelMove

ae.add_supported_context("1.2.840.10008.5.1.4.1.2.2.1", transfer)  # StudyRootQueryRetrieveInformationModelFind
ae.add_supported_context("1.2.840.10008.5.1.4.1.2.2.3", transfer)  # StudyRootQueryRetrieveInformationModelGet
ae.add_supported_context("1.2.840.10008.5.1.4.1.2.2.2", transfer)  # StudyRootQueryRetrieveInformationModelMove

ae.add_supported_context("1.2.840.10008.5.1.4.31", transfer)  # ModalityWorklistInformationFind

ae.add_supported_context("1.2.840.10008.1.1", transfer)  # Verification Service Class - Test echo


# OHIF
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.1", transfer)
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.6", transfer)
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.4.1", transfer)
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.2.1", transfer)
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.7", transfer)
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.128", transfer)
ae.add_supported_context("1.2.840.10008.5.1.4.1.1.20", transfer)


def handle_store(event):
    """Handle EVT_C_STORE events."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.save_as(SERVER_DATA + ds.SOPInstanceUID + ".dcm", write_like_original=False)

    return 0x0000


def handle_find(event):
    """Handle a C-FIND request event."""
    ds = event.identifier

    # Import stored SOP Instances
    instances = []
    fdir = SERVER_DATA
    for fpath in os.listdir(fdir):
        instances.append(dcmread(os.path.join(fdir, fpath)))

    # if 'QueryRetrieveLevel' not in ds:
    #     # Failure
    #     yield 0xC000, None
    #     return
    #
    # if ds.QueryRetrieveLevel == 'PATIENT':
    #     if 'PatientName' in ds:
    #         if ds.PatientName not in ['*', '', '?']:
    #             matching = [inst for inst in instances if inst.PatientName == ds.PatientName]
    #         # Skip the other possible values...
    #     # Skip the other possible attributes...
    # # Skip the other QR levels...

    for instance in instances:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        # identifier = Dataset()
        identifier = instance
        # identifier.PatientName = instance.PatientName
        # identifier.QueryRetrieveLevel = ds.QueryRetrieveLevel

        # Pending
        yield (0xFF00, identifier)


# Implement the evt.EVT_C_MOVE handler
def handle_move(event):
    """Handle a C-MOVE request event."""
    ds = event.identifier

    if 'QueryRetrieveLevel' not in ds:
        # Failure
        yield 0xC000, None
        return

    # Check known_aet addr, port
    # known_aet_dict = get_known_aet()
    # try:
    #     (addr, port) = known_aet_dict[event.move_destination]
    # except KeyError:
    #     # Unknown destination AE
    #     yield (None, None)
    #     return
    #
    # # Yield the IP address and listen port of the destination AE
    # yield (addr, port)

    # (addr, port) = event.move_destination
    yield ("127.0.0.1", 8042)

    # Import stored SOP Instances
    instances = []
    matching = []
    fdir = SERVER_DATA
    for fpath in os.listdir(fdir):
        instances.append(dcmread(os.path.join(fdir, fpath)))

    # Yield the total number of C-STORE sub-operations required
    yield len(matching)

    # Yield the matching instances
    for instance in matching:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        # Pending
        yield (0xFF00, instance)


handlers = [(evt.EVT_C_MOVE, handle_move), (evt.EVT_C_STORE, handle_store), (evt.EVT_C_FIND, handle_find)]

ae.start_server(("localhost", 11112), block=True, evt_handlers=handlers)
