window.config = {
  routerBasename: '/ohif',
  showStudyList: true,
  showBackButton: false,
  extensions: [],
  modes: [],
  // below flag is for performance reasons, but it might not work for all servers
  showWarningMessageForCrossOrigin: true,
  showCPUFallbackMessage: true,
  showLoadingIndicator: true,
  strictZSpacingForVolumeViewport: true,
  defaultDataSourceName: 'dicomweb',
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
        orthancUrl: 'https://emr-api.saigonmec.org/oc-dcweb',
        wadoUriRoot: 'https://emr-api.saigonmec.org/oc-dcweb/wado',
        qidoRoot: 'https://emr-api.saigonmec.org/oc-dcweb/dicom-web',
        wadoRoot: 'https://emr-api.saigonmec.org/oc-dcweb/dicom-web',
        qidoSupportsIncludeField: false,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        omitQuotationForMultipartRequest: true,
        dicomUploadEnabled: true,
      },
    }
  ],
};
