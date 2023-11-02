Some notes



UID: https://pydicom.github.io/pydicom/stable/reference/uid.html
SCP: https://pydicom.github.io/pynetdicom/stable/tutorials/create_scp.html
SCU: https://pydicom.github.io/pynetdicom/stable/tutorials/create_scu.html
dicoogle dataset basic: https://pydicom.github.io/pydicom/stable/tutorials/dataset_basics.html




Copy file from Docker to local:
	docker cp container_id:/etc/orthanc/orthanc.json orthanc_docker.json
container_id is a container ID, not an image ID.
Ref: https://stackoverflow.com/questions/22907231/how-to-copy-files-from-host-to-docker-container
	
	
	
	
DICOM web Rest API standard: https://www.dicomstandard.org/using/dicomweb	
	

	
Python plugin for orthanc docker: https://book.orthanc-server.com/plugins/python.html#storage-commitment-scp-new-in-4-1


OHIF custom service: https://docs.ohif.org/platform/services/ui/customization-service/#registering-customizable-modules-or-defining-customization-prototypes



Add buttons toolbar:
	- Mode: longitudinal
	- In toolbarButtons.ts, add buttons in const toolbarButtons: Button[]
	- In index.js, add buttons id in toolbarService.createButtonSection('primary', [...]);
Ref: OHIF Custom toolbar: https://docs.ohif.org/platform/extensions/modules/toolbar
	
	
	
Config nginx: https://code.oak-tree.tech/oak-tree/medical-imaging/ohif-viewers/-/tree/issue-619/docker/Nginx-Orthanc