window.config = {
  routerBasename: '/ohif',
  showStudyList: true,
  showBackButton: false,
  extensions: [],
  modes: [],
  // below flag is for performance reasons, but it might not work for all servers
  showWarningMessageForCrossOrigin: false,
  showCPUFallbackMessage: true,
  showLoadingIndicator: true,
  strictZSpacingForVolumeViewport: true,
  defaultDataSourceName: 'dicomjson',
  customizationService: {
    dicomUploadComponent:
      '@ohif/extension-cornerstone.customizationModule.cornerstoneDicomUploadComponent',
  },
  dataSources: [
    {
      namespace: '@ohif/extension-default.dataSourcesModule.dicomweb',
      sourceName: 'dicomweb',
      configuration: {
        friendlyName: 'Orthanc Server',
        name: 'Orthanc',
        orthancUrl: 'https://dev-emr-api.saigonmec.org/oc-dcweb',
        wadoUriRoot: 'https://dev-emr-api.saigonmec.org/oc-dcweb/wado',
        qidoRoot: 'https://dev-emr-api.saigonmec.org/oc-dcweb/dicom-web',
        wadoRoot: 'https://dev-emr-api.saigonmec.org/oc-dcweb/dicom-web',
        qidoSupportsIncludeField: false,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        omitQuotationForMultipartRequest: true,
        dicomUploadEnabled: true,
      },
    },
	{
		namespace: "@ohif/extension-default.dataSourcesModule.dicomjson",
		sourceName: "dicomjson",
		configuration: {
			friendlyName: "dicom json",
			name: "json"
		}
	}
  ],
};
