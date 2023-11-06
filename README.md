# 1. Quick start
### 1.1 Orthanc with Nginx (Backend server)
    cd dicom_research/docker
    docker-compose up
    
After running, we have:
- HTTP: http://localhost:8899
- DICOM: http://localhost:4242
- We can use the default Orthanc UI by going to: http://localhost:8899/app/explorer.html
 
### 1.2 OHIF Viewer (Client side)
    cd dicom_research/OHIF_Viewer
    yarn install
    yarn run dev:orthanc

After running, we have:
- A web client: http://localhost:3000
 
### 1.3 PACS (Pseudo hospital machine)
We use the Orthanc window version. Download here: https://www.orthanc-server.com/download-windows.php
After installation successfully, we will see an Orthanc service. If we update the config file, we need to restart this service.
The config file is: C:\Program Files\Orthanc Server\Configuration\orthanc.json

### 1.4 Custom server
The source code is in the "python_server" folder. Update the "dicom_storage_dir" path in web_server.py, and run the server to test.

### 1.5 Test data
The DCM test data is in the "test_data" folder. This data include the Dicoogle public dataset and the Pydicom sample DCM file.


# 2. Documents
- List of UID: https://pydicom.github.io/pydicom/stable/reference/uid.html
- SCP Example: https://pydicom.github.io/pynetdicom/stable/tutorials/create_scp.html
- SCU Example: https://pydicom.github.io/pynetdicom/stable/tutorials/create_scu.html
- DCM Sample (dicoogle dataset): https://pydicom.github.io/pydicom/stable/tutorials/dataset_basics.html
- DICOM web Rest API standard: https://www.dicomstandard.org/using/dicomweb	
- Python plugin for orthanc docker: https://book.orthanc-server.com/plugins/python.html#storage-commitment-scp-new-in-4-1
- OHIF Custom toolbar: https://docs.ohif.org/platform/extensions/modules/toolbar
- Config nginx: https://book.orthanc-server.com/faq/nginx.html
- Config nginx example: https://code.oak-tree.tech/oak-tree/medical-imaging/ohif-viewers/-/tree/issue-619/docker/Nginx-Orthanc
- OHIF custom service: https://docs.ohif.org/platform/services/ui/customization-service/#registering-customizable-modules-or-defining-customization-prototypes

# 3. Useful commands
### 3.1 Copy file from Docker to local:
	docker cp container_id:/etc/orthanc/orthanc.json orthanc_docker.json
container_id is a container ID, not an image ID.
Ref: https://stackoverflow.com/questions/22907231/how-to-copy-files-from-host-to-docker-container
	
	
