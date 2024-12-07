"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[4834],{

/***/ 44834:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  cornerstone: () => (/* binding */ cornerstone),
  "default": () => (/* binding */ microscopy_src)
});

// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var src = __webpack_require__(29463);
// EXTERNAL MODULE: ../../../node_modules/i18next/dist/esm/i18next.js
var i18next = __webpack_require__(40680);
;// CONCATENATED MODULE: ../../../modes/microscopy/package.json
const package_namespaceObject = /*#__PURE__*/JSON.parse('{"UU":"@ohif/mode-microscopy"}');
;// CONCATENATED MODULE: ../../../modes/microscopy/src/id.js

const id = package_namespaceObject.UU;

;// CONCATENATED MODULE: ../../../modes/microscopy/src/toolbarButtons.js

const toolbarButtons = [{
  id: 'MeasurementTools',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'MeasurementTools',
    // group evaluate to determine which item should move to the top
    evaluate: 'evaluate.group.promoteToPrimary',
    primary: src/* ToolbarService */.hx.createButton({
      id: 'line',
      icon: 'tool-length',
      label: 'Line',
      tooltip: 'Line',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'line'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }),
    secondary: {
      icon: 'chevron-down',
      tooltip: 'More Measure Tools'
    },
    items: [src/* ToolbarService */.hx.createButton({
      id: 'line',
      icon: 'tool-length',
      label: 'Line',
      tooltip: 'Line',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'line'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }), src/* ToolbarService */.hx.createButton({
      id: 'point',
      icon: 'tool-point',
      label: 'Point',
      tooltip: 'Point Tool',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'point'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }),
    // Point Tool was previously defined
    src/* ToolbarService */.hx.createButton({
      id: 'polygon',
      icon: 'tool-polygon',
      label: 'Polygon',
      tooltip: 'Polygon Tool',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'polygon'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }), src/* ToolbarService */.hx.createButton({
      id: 'circle',
      icon: 'tool-circle',
      label: 'Circle',
      tooltip: 'Circle Tool',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'circle'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }), src/* ToolbarService */.hx.createButton({
      id: 'box',
      icon: 'tool-rectangle',
      label: 'Box',
      tooltip: 'Box Tool',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'box'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }), src/* ToolbarService */.hx.createButton({
      id: 'freehandpolygon',
      icon: 'tool-freehand-polygon',
      label: 'Freehand Polygon',
      tooltip: 'Freehand Polygon Tool',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'freehandpolygon'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    }), src/* ToolbarService */.hx.createButton({
      id: 'freehandline',
      icon: 'tool-freehand-line',
      label: 'Freehand Line',
      tooltip: 'Freehand Line Tool',
      commands: [{
        commandName: 'setToolActive',
        commandOptions: {
          toolName: 'freehandline'
        },
        context: 'MICROSCOPY'
      }],
      evaluate: 'evaluate.microscopyTool'
    })]
  }
}, {
  id: 'dragPan',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-move',
    label: 'Pan',
    commands: [{
      commandName: 'setToolActive',
      commandOptions: {
        toolName: 'dragPan'
      },
      context: 'MICROSCOPY'
    }],
    evaluate: 'evaluate.microscopyTool'
  }
}, {
  id: 'TagBrowser',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'dicom-tag-browser',
    label: 'Dicom Tag Browser',
    commands: [{
      commandName: 'openDICOMTagViewer'
    }],
    evaluate: 'evaluate.action'
  }
}];
/* harmony default export */ const src_toolbarButtons = (toolbarButtons);
;// CONCATENATED MODULE: ../../../modes/microscopy/src/index.tsx




const ohif = {
  layout: '@ohif/extension-default.layoutTemplateModule.viewerLayout',
  sopClassHandler: '@ohif/extension-default.sopClassHandlerModule.stack',
  hangingProtocols: '@ohif/extension-default.hangingProtocolModule.default',
  leftPanel: '@ohif/extension-default.panelModule.seriesList',
  rightPanel: '@ohif/extension-default.panelModule.measure'
};
const cornerstone = {
  viewport: '@ohif/extension-cornerstone.viewportModule.cornerstone'
};
const dicomvideo = {
  sopClassHandler: '@ohif/extension-dicom-video.sopClassHandlerModule.dicom-video',
  viewport: '@ohif/extension-dicom-video.viewportModule.dicom-video'
};
const dicompdf = {
  sopClassHandler: '@ohif/extension-dicom-pdf.sopClassHandlerModule.dicom-pdf',
  viewport: '@ohif/extension-dicom-pdf.viewportModule.dicom-pdf'
};
const extensionDependencies = {
  // Can derive the versions at least process.env.from npm_package_version
  '@ohif/extension-default': '^3.0.0',
  '@ohif/extension-cornerstone': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-sr': '^3.0.0',
  '@ohif/extension-dicom-pdf': '^3.0.1',
  '@ohif/extension-dicom-video': '^3.0.1',
  '@ohif/extension-dicom-microscopy': '^3.0.0'
};
function modeFactory({
  modeConfiguration
}) {
  return {
    // TODO: We're using this as a route segment
    // We should not be.
    id: id,
    routeName: 'microscopy',
    displayName: i18next/* default */.A.t('Modes:Microscopy'),
    /**
     * Lifecycle hooks
     */
    onModeEnter: ({
      servicesManager,
      extensionManager,
      commandsManager
    }) => {
      const {
        toolbarService
      } = servicesManager.services;
      toolbarService.addButtons(src_toolbarButtons);
      toolbarService.createButtonSection('primary', ['MeasurementTools', 'dragPan', 'TagBrowser']);
    },
    onModeExit: ({
      servicesManager
    }) => {
      const {
        toolbarService,
        uiDialogService,
        uiModalService
      } = servicesManager.services;
      uiDialogService.dismissAll();
      uiModalService.hide();
      toolbarService.reset();
    },
    validationTags: {
      study: [],
      series: []
    },
    isValidMode: ({
      modalities
    }) => {
      const modalities_list = modalities.split('\\');
      return {
        valid: modalities_list.includes('SM'),
        description: 'Microscopy mode only supports the SM modality'
      };
    },
    routes: [{
      path: 'microscopy',
      /*init: ({ servicesManager, extensionManager }) => {
        //defaultViewerRouteInit
      },*/
      layoutTemplate: ({
        location,
        servicesManager
      }) => {
        return {
          id: ohif.layout,
          props: {
            leftPanels: [ohif.leftPanel],
            leftPanelClosed: true,
            // we have problem with rendering thumbnails for microscopy images
            rightPanelClosed: true,
            // we do not have the save microscopy measurements yet
            rightPanels: ['@ohif/extension-dicom-microscopy.panelModule.measure'],
            viewports: [{
              namespace: '@ohif/extension-dicom-microscopy.viewportModule.microscopy-dicom',
              displaySetsToDisplay: [
              // Share the sop class handler with cornerstone version of it
              '@ohif/extension-cornerstone.sopClassHandlerModule.DicomMicroscopySopClassHandler', '@ohif/extension-dicom-microscopy.sopClassHandlerModule.DicomMicroscopySRSopClassHandler']
            }, {
              namespace: dicomvideo.viewport,
              displaySetsToDisplay: [dicomvideo.sopClassHandler]
            }, {
              namespace: dicompdf.viewport,
              displaySetsToDisplay: [dicompdf.sopClassHandler]
            }]
          }
        };
      }
    }],
    extensions: extensionDependencies,
    hangingProtocol: 'default',
    sopClassHandlers: ['@ohif/extension-cornerstone.sopClassHandlerModule.DicomMicroscopySopClassHandler', '@ohif/extension-dicom-microscopy.sopClassHandlerModule.DicomMicroscopySRSopClassHandler', dicomvideo.sopClassHandler, dicompdf.sopClassHandler],
    hotkeys: [...src/* hotkeys */.ot.defaults.hotkeyBindings],
    ...modeConfiguration
  };
}
const mode = {
  id: id,
  modeFactory,
  extensionDependencies
};
/* harmony default export */ const microscopy_src = (mode);

/***/ })

}]);