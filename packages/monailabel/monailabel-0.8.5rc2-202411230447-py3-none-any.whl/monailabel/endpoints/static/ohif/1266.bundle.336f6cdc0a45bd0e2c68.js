"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[1266,2591,4182,1801],{

/***/ 35589:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ longitudinal_src),
  initToolGroups: () => (/* reexport */ src_initToolGroups),
  moreTools: () => (/* reexport */ src_moreTools),
  toolbarButtons: () => (/* reexport */ src_toolbarButtons)
});

// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var src = __webpack_require__(29463);
// EXTERNAL MODULE: ../../../node_modules/i18next/dist/esm/i18next.js
var i18next = __webpack_require__(40680);
;// CONCATENATED MODULE: ../../../modes/longitudinal/package.json
const package_namespaceObject = /*#__PURE__*/JSON.parse('{"UU":"@ohif/mode-longitudinal"}');
;// CONCATENATED MODULE: ../../../modes/longitudinal/src/id.js

const id = package_namespaceObject.UU;

// EXTERNAL MODULE: ../../../extensions/cornerstone-dicom-sr/src/index.tsx + 16 modules
var cornerstone_dicom_sr_src = __webpack_require__(85687);
;// CONCATENATED MODULE: ../../../modes/longitudinal/src/initToolGroups.js

const colours = {
  'viewport-0': 'rgb(200, 0, 0)',
  'viewport-1': 'rgb(200, 200, 0)',
  'viewport-2': 'rgb(0, 200, 0)'
};
const colorsByOrientation = {
  axial: 'rgb(200, 0, 0)',
  sagittal: 'rgb(200, 200, 0)',
  coronal: 'rgb(0, 200, 0)'
};
function initDefaultToolGroup(extensionManager, toolGroupService, commandsManager, toolGroupId, modeLabelConfig) {
  const utilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.tools');
  const {
    toolNames,
    Enums
  } = utilityModule.exports;
  const tools = {
    active: [{
      toolName: toolNames.WindowLevel,
      bindings: [{
        mouseButton: Enums.MouseBindings.Primary
      }]
    }, {
      toolName: toolNames.Pan,
      bindings: [{
        mouseButton: Enums.MouseBindings.Auxiliary
      }]
    }, {
      toolName: toolNames.Zoom,
      bindings: [{
        mouseButton: Enums.MouseBindings.Secondary
      }]
    }, {
      toolName: toolNames.StackScroll,
      bindings: [{
        mouseButton: Enums.MouseBindings.Wheel
      }]
    }],
    passive: [{
      toolName: toolNames.Length
    }, {
      toolName: toolNames.ArrowAnnotate,
      configuration: {
        getTextCallback: (callback, eventDetails) => {
          if (modeLabelConfig) {
            callback(' ');
          } else {
            commandsManager.runCommand('arrowTextCallback', {
              callback,
              eventDetails
            });
          }
        },
        changeTextCallback: (data, eventDetails, callback) => {
          if (modeLabelConfig === undefined) {
            commandsManager.runCommand('arrowTextCallback', {
              callback,
              data,
              eventDetails
            });
          }
        }
      }
    }, {
      toolName: toolNames.Bidirectional
    }, {
      toolName: toolNames.DragProbe
    }, {
      toolName: toolNames.Probe
    }, {
      toolName: toolNames.EllipticalROI
    }, {
      toolName: toolNames.CircleROI
    }, {
      toolName: toolNames.RectangleROI
    }, {
      toolName: toolNames.StackScroll
    }, {
      toolName: toolNames.Angle
    }, {
      toolName: toolNames.CobbAngle
    }, {
      toolName: toolNames.Magnify
    }, {
      toolName: toolNames.CalibrationLine
    }, {
      toolName: toolNames.PlanarFreehandContourSegmentation,
      configuration: {
        displayOnePointAsCrosshairs: true
      }
    }, {
      toolName: toolNames.UltrasoundDirectional
    }, {
      toolName: toolNames.PlanarFreehandROI
    }, {
      toolName: toolNames.SplineROI
    }, {
      toolName: toolNames.LivewireContour
    }, {
      toolName: toolNames.WindowLevelRegion
    }],
    enabled: [{
      toolName: toolNames.ImageOverlayViewer
    }, {
      toolName: toolNames.ReferenceLines
    }, {
      toolName: cornerstone_dicom_sr_src.toolNames.SRSCOORD3DPoint
    }],
    disabled: [{
      toolName: toolNames.AdvancedMagnify
    }]
  };
  toolGroupService.createToolGroupAndAddTools(toolGroupId, tools);
}
function initSRToolGroup(extensionManager, toolGroupService) {
  const SRUtilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone-dicom-sr.utilityModule.tools');
  if (!SRUtilityModule) {
    return;
  }
  const CS3DUtilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.tools');
  const {
    toolNames: SRToolNames
  } = SRUtilityModule.exports;
  const {
    toolNames,
    Enums
  } = CS3DUtilityModule.exports;
  const tools = {
    active: [{
      toolName: toolNames.WindowLevel,
      bindings: [{
        mouseButton: Enums.MouseBindings.Primary
      }]
    }, {
      toolName: toolNames.Pan,
      bindings: [{
        mouseButton: Enums.MouseBindings.Auxiliary
      }]
    }, {
      toolName: toolNames.Zoom,
      bindings: [{
        mouseButton: Enums.MouseBindings.Secondary
      }]
    }, {
      toolName: toolNames.StackScroll,
      bindings: [{
        mouseButton: Enums.MouseBindings.Wheel
      }]
    }],
    passive: [{
      toolName: SRToolNames.SRLength
    }, {
      toolName: SRToolNames.SRArrowAnnotate
    }, {
      toolName: SRToolNames.SRBidirectional
    }, {
      toolName: SRToolNames.SREllipticalROI
    }, {
      toolName: SRToolNames.SRCircleROI
    }, {
      toolName: SRToolNames.SRPlanarFreehandROI
    }, {
      toolName: SRToolNames.SRRectangleROI
    }, {
      toolName: toolNames.WindowLevelRegion
    }],
    enabled: [{
      toolName: SRToolNames.DICOMSRDisplay
    }]
    // disabled
  };
  const toolGroupId = 'SRToolGroup';
  toolGroupService.createToolGroupAndAddTools(toolGroupId, tools);
}
function initMPRToolGroup(extensionManager, toolGroupService, commandsManager, modeLabelConfig) {
  const utilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.tools');
  const serviceManager = extensionManager._servicesManager;
  const {
    cornerstoneViewportService
  } = serviceManager.services;
  const {
    toolNames,
    Enums
  } = utilityModule.exports;
  const tools = {
    active: [{
      toolName: toolNames.WindowLevel,
      bindings: [{
        mouseButton: Enums.MouseBindings.Primary
      }]
    }, {
      toolName: toolNames.Pan,
      bindings: [{
        mouseButton: Enums.MouseBindings.Auxiliary
      }]
    }, {
      toolName: toolNames.Zoom,
      bindings: [{
        mouseButton: Enums.MouseBindings.Secondary
      }]
    }, {
      toolName: toolNames.StackScroll,
      bindings: [{
        mouseButton: Enums.MouseBindings.Wheel
      }]
    }],
    passive: [{
      toolName: toolNames.Length
    }, {
      toolName: toolNames.ArrowAnnotate,
      configuration: {
        getTextCallback: (callback, eventDetails) => {
          if (modeLabelConfig) {
            callback('');
          } else {
            commandsManager.runCommand('arrowTextCallback', {
              callback,
              eventDetails
            });
          }
        },
        changeTextCallback: (data, eventDetails, callback) => {
          if (modeLabelConfig === undefined) {
            commandsManager.runCommand('arrowTextCallback', {
              callback,
              data,
              eventDetails
            });
          }
        }
      }
    }, {
      toolName: toolNames.Bidirectional
    }, {
      toolName: toolNames.DragProbe
    }, {
      toolName: toolNames.Probe
    }, {
      toolName: toolNames.EllipticalROI
    }, {
      toolName: toolNames.CircleROI
    }, {
      toolName: toolNames.RectangleROI
    }, {
      toolName: toolNames.StackScroll
    }, {
      toolName: toolNames.Angle
    }, {
      toolName: toolNames.CobbAngle
    }, {
      toolName: toolNames.PlanarFreehandROI
    }, {
      toolName: toolNames.WindowLevelRegion
    }, {
      toolName: toolNames.PlanarFreehandContourSegmentation,
      configuration: {
        displayOnePointAsCrosshairs: true
      }
    }],
    disabled: [{
      toolName: toolNames.Crosshairs,
      configuration: {
        viewportIndicators: true,
        viewportIndicatorsConfig: {
          circleRadius: 5,
          xOffset: 0.95,
          yOffset: 0.05
        },
        disableOnPassive: true,
        autoPan: {
          enabled: false,
          panSize: 10
        },
        getReferenceLineColor: viewportId => {
          const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
          const viewportOptions = viewportInfo?.viewportOptions;
          if (viewportOptions) {
            return colours[viewportOptions.id] || colorsByOrientation[viewportOptions.orientation] || '#0c0';
          } else {
            console.warn('missing viewport?', viewportId);
            return '#0c0';
          }
        }
      }
    }, {
      toolName: toolNames.AdvancedMagnify
    }, {
      toolName: toolNames.ReferenceLines
    }]
  };
  toolGroupService.createToolGroupAndAddTools('mpr', tools);
}
function initVolume3DToolGroup(extensionManager, toolGroupService) {
  const utilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.tools');
  const {
    toolNames,
    Enums
  } = utilityModule.exports;
  const tools = {
    active: [{
      toolName: toolNames.TrackballRotateTool,
      bindings: [{
        mouseButton: Enums.MouseBindings.Primary
      }]
    }, {
      toolName: toolNames.Zoom,
      bindings: [{
        mouseButton: Enums.MouseBindings.Secondary
      }]
    }, {
      toolName: toolNames.Pan,
      bindings: [{
        mouseButton: Enums.MouseBindings.Auxiliary
      }]
    }]
  };
  toolGroupService.createToolGroupAndAddTools('volume3d', tools);
}
function initToolGroups(extensionManager, toolGroupService, commandsManager, modeLabelConfig) {
  initDefaultToolGroup(extensionManager, toolGroupService, commandsManager, 'default', modeLabelConfig);
  initSRToolGroup(extensionManager, toolGroupService, commandsManager);
  initMPRToolGroup(extensionManager, toolGroupService, commandsManager, modeLabelConfig);
  initVolume3DToolGroup(extensionManager, toolGroupService);
}
/* harmony default export */ const src_initToolGroups = (initToolGroups);
;// CONCATENATED MODULE: ../../../modes/longitudinal/src/toolbarButtons.ts
// TODO: torn, can either bake this here; or have to create a whole new button type
// Only ways that you can pass in a custom React component for render :l

const {
  createButton
} = src/* ToolbarService */.hx;
const setToolActiveToolbar = {
  commandName: 'setToolActiveToolbar',
  commandOptions: {
    toolGroupIds: ['default', 'mpr', 'SRToolGroup', 'volume3d']
  }
};
const toolbarButtons = [{
  id: 'MeasurementTools',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'MeasurementTools',
    // group evaluate to determine which item should move to the top
    evaluate: 'evaluate.group.promoteToPrimaryIfCornerstoneToolNotActiveInTheList',
    primary: createButton({
      id: 'Length',
      icon: 'tool-length',
      label: 'Length',
      tooltip: 'Length Tool',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }),
    secondary: {
      icon: 'chevron-down',
      tooltip: 'More Measure Tools'
    },
    items: [createButton({
      id: 'Length',
      icon: 'tool-length',
      label: 'Length',
      tooltip: 'Length Tool',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'Bidirectional',
      icon: 'tool-bidirectional',
      label: 'Bidirectional',
      tooltip: 'Bidirectional Tool',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'ArrowAnnotate',
      icon: 'tool-annotate',
      label: 'Annotation',
      tooltip: 'Arrow Annotate',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'EllipticalROI',
      icon: 'tool-ellipse',
      label: 'Ellipse',
      tooltip: 'Ellipse ROI',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'RectangleROI',
      icon: 'tool-rectangle',
      label: 'Rectangle',
      tooltip: 'Rectangle ROI',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'CircleROI',
      icon: 'tool-circle',
      label: 'Circle',
      tooltip: 'Circle Tool',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'PlanarFreehandROI',
      icon: 'icon-tool-freehand-roi',
      label: 'Freehand ROI',
      tooltip: 'Freehand ROI',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'SplineROI',
      icon: 'icon-tool-spline-roi',
      label: 'Spline ROI',
      tooltip: 'Spline ROI',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'LivewireContour',
      icon: 'icon-tool-livewire',
      label: 'Livewire tool',
      tooltip: 'Livewire tool',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    })]
  }
}, {
  id: 'Zoom',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-zoom',
    label: 'Zoom',
    commands: setToolActiveToolbar,
    evaluate: 'evaluate.cornerstoneTool'
  }
},
// Window Level
{
  id: 'WindowLevel',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-window-level',
    label: 'Window Level',
    commands: setToolActiveToolbar,
    evaluate: ['evaluate.cornerstoneTool', {
      name: 'evaluate.viewport.supported',
      unsupportedViewportTypes: ['wholeSlide']
    }]
  }
},
// Pan...
{
  id: 'Pan',
  uiType: 'ohif.radioGroup',
  props: {
    type: 'tool',
    icon: 'tool-move',
    label: 'Pan',
    commands: setToolActiveToolbar,
    evaluate: 'evaluate.cornerstoneTool'
  }
}, {
  id: 'TrackballRotate',
  uiType: 'ohif.radioGroup',
  props: {
    type: 'tool',
    icon: 'tool-3d-rotate',
    label: '3D Rotate',
    commands: setToolActiveToolbar,
    evaluate: {
      name: 'evaluate.cornerstoneTool',
      disabledText: 'Select a 3D viewport to enable this tool'
    }
  }
}, {
  id: 'Capture',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-capture',
    label: 'Capture',
    commands: 'showDownloadViewportModal',
    evaluate: ['evaluate.action', {
      name: 'evaluate.viewport.supported',
      unsupportedViewportTypes: ['video', 'wholeSlide']
    }]
  }
}, {
  id: 'Layout',
  uiType: 'ohif.layoutSelector',
  props: {
    rows: 3,
    columns: 4,
    evaluate: 'evaluate.action'
  }
}, {
  id: 'Crosshairs',
  uiType: 'ohif.radioGroup',
  props: {
    type: 'tool',
    icon: 'tool-crosshair',
    label: 'Crosshairs',
    commands: {
      commandName: 'setToolActiveToolbar',
      commandOptions: {
        toolGroupIds: ['mpr']
      }
    },
    evaluate: {
      name: 'evaluate.cornerstoneTool',
      disabledText: 'Select an MPR viewport to enable this tool'
    }
  }
}];
/* harmony default export */ const src_toolbarButtons = (toolbarButtons);
// EXTERNAL MODULE: ../../../node_modules/@cornerstonejs/core/dist/esm/index.js
var esm = __webpack_require__(81985);
;// CONCATENATED MODULE: ../../../modes/longitudinal/src/moreTools.ts



const {
  createButton: moreTools_createButton
} = src/* ToolbarService */.hx;
const ReferenceLinesListeners = [{
  commandName: 'setSourceViewportForReferenceLinesTool',
  context: 'CORNERSTONE'
}];
const moreTools = [{
  id: 'MoreTools',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'MoreTools',
    evaluate: 'evaluate.group.promoteToPrimaryIfCornerstoneToolNotActiveInTheList',
    primary: moreTools_createButton({
      id: 'Reset',
      icon: 'tool-reset',
      tooltip: 'Reset View',
      label: 'Reset',
      commands: 'resetViewport',
      evaluate: 'evaluate.action'
    }),
    secondary: {
      icon: 'chevron-down',
      label: '',
      tooltip: 'More Tools'
    },
    items: [moreTools_createButton({
      id: 'Reset',
      icon: 'tool-reset',
      label: 'Reset View',
      tooltip: 'Reset View',
      commands: 'resetViewport',
      evaluate: 'evaluate.action'
    }), moreTools_createButton({
      id: 'rotate-right',
      icon: 'tool-rotate-right',
      label: 'Rotate Right',
      tooltip: 'Rotate +90',
      commands: 'rotateViewportCW',
      evaluate: ['evaluate.action', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'flipHorizontal',
      icon: 'tool-flip-horizontal',
      label: 'Flip Horizontal',
      tooltip: 'Flip Horizontally',
      commands: 'flipViewportHorizontal',
      evaluate: ['evaluate.viewportProperties.toggle', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video', 'volume3d']
      }]
    }), moreTools_createButton({
      id: 'ImageSliceSync',
      icon: 'link',
      label: 'Image Slice Sync',
      tooltip: 'Enable position synchronization on stack viewports',
      commands: {
        commandName: 'toggleSynchronizer',
        commandOptions: {
          type: 'imageSlice'
        }
      },
      listeners: {
        [esm.EVENTS.VIEWPORT_NEW_IMAGE_SET]: {
          commandName: 'toggleImageSliceSync',
          commandOptions: {
            toggledState: true
          }
        }
      },
      evaluate: ['evaluate.cornerstone.synchronizer', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video', 'volume3d']
      }]
    }), moreTools_createButton({
      id: 'ReferenceLines',
      icon: 'tool-referenceLines',
      label: 'Reference Lines',
      tooltip: 'Show Reference Lines',
      commands: 'toggleEnabledDisabledToolbar',
      listeners: {
        [src/* ViewportGridService */.sI.EVENTS.ACTIVE_VIEWPORT_ID_CHANGED]: ReferenceLinesListeners,
        [src/* ViewportGridService */.sI.EVENTS.VIEWPORTS_READY]: ReferenceLinesListeners
      },
      evaluate: ['evaluate.cornerstoneTool.toggle', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'ImageOverlayViewer',
      icon: 'toggle-dicom-overlay',
      label: 'Image Overlay',
      tooltip: 'Toggle Image Overlay',
      commands: 'toggleEnabledDisabledToolbar',
      evaluate: ['evaluate.cornerstoneTool.toggle', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'StackScroll',
      icon: 'tool-stack-scroll',
      label: 'Stack Scroll',
      tooltip: 'Stack Scroll',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), moreTools_createButton({
      id: 'invert',
      icon: 'tool-invert',
      label: 'Invert',
      tooltip: 'Invert Colors',
      commands: 'invertViewport',
      evaluate: ['evaluate.viewportProperties.toggle', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'Probe',
      icon: 'tool-probe',
      label: 'Probe',
      tooltip: 'Probe',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), moreTools_createButton({
      id: 'Cine',
      icon: 'tool-cine',
      label: 'Cine',
      tooltip: 'Cine',
      commands: 'toggleCine',
      evaluate: ['evaluate.cine', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['volume3d']
      }]
    }), moreTools_createButton({
      id: 'Angle',
      icon: 'tool-angle',
      label: 'Angle',
      tooltip: 'Angle',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), moreTools_createButton({
      id: 'CobbAngle',
      icon: 'icon-tool-cobb-angle',
      label: 'Cobb Angle',
      tooltip: 'Cobb Angle',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), moreTools_createButton({
      id: 'Magnify',
      icon: 'tool-magnify',
      label: 'Zoom-in',
      tooltip: 'Zoom-in',
      commands: setToolActiveToolbar,
      evaluate: ['evaluate.cornerstoneTool', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'CalibrationLine',
      icon: 'tool-calibration',
      label: 'Calibration',
      tooltip: 'Calibration Line',
      commands: setToolActiveToolbar,
      evaluate: ['evaluate.cornerstoneTool', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'TagBrowser',
      icon: 'dicom-tag-browser',
      label: 'Dicom Tag Browser',
      tooltip: 'Dicom Tag Browser',
      commands: 'openDICOMTagViewer'
    }), moreTools_createButton({
      id: 'AdvancedMagnify',
      icon: 'icon-tool-loupe',
      label: 'Magnify Probe',
      tooltip: 'Magnify Probe',
      commands: 'toggleActiveDisabledToolbar',
      evaluate: ['evaluate.cornerstoneTool.toggle.ifStrictlyDisabled', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    }), moreTools_createButton({
      id: 'UltrasoundDirectionalTool',
      icon: 'icon-tool-ultrasound-bidirectional',
      label: 'Ultrasound Directional',
      tooltip: 'Ultrasound Directional',
      commands: setToolActiveToolbar,
      evaluate: ['evaluate.cornerstoneTool', {
        name: 'evaluate.modality.supported',
        supportedModalities: ['US']
      }]
    }), moreTools_createButton({
      id: 'WindowLevelRegion',
      icon: 'icon-tool-window-region',
      label: 'Window Level Region',
      tooltip: 'Window Level Region',
      commands: setToolActiveToolbar,
      evaluate: ['evaluate.cornerstoneTool', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['video']
      }]
    })]
  }
}];
/* harmony default export */ const src_moreTools = (moreTools);
;// CONCATENATED MODULE: ../../../modes/longitudinal/src/customizations.tsx
const performCustomizations = customizationService => {
  // Set the custom SegmentationTable
  customizationService.addModeCustomizations([
  // To disable editing in the SegmentationTable
  {
    id: 'PanelSegmentation.disableEditing',
    disableEditing: true
  }
  // To disable editing in the MeasurementTable
  // {
  //   id: 'PanelMeasurement.disableEditing',
  //   disableEditing: true,
  // },
  //   {
  //     id: 'measurementLabels',
  //     labelOnMeasure: true,
  //     exclusive: true,
  //     items: [
  //       { value: 'Head', label: 'Head' },
  //       { value: 'Shoulder', label: 'Shoulder' },
  //       { value: 'Knee', label: 'Knee' },
  //       { value: 'Toe', label: 'Toe' },
  //     ],
  //   },
  ]);
};
;// CONCATENATED MODULE: ../../../modes/longitudinal/src/index.ts








// Allow this mode by excluding non-imaging modalities such as SR, SEG
// Also, SM is not a simple imaging modalities, so exclude it.
const NON_IMAGE_MODALITIES = ['ECG', 'SEG', 'RTSTRUCT', 'RTPLAN', 'PR'];
const ohif = {
  layout: '@ohif/extension-default.layoutTemplateModule.viewerLayout',
  sopClassHandler: '@ohif/extension-default.sopClassHandlerModule.stack',
  thumbnailList: '@ohif/extension-default.panelModule.seriesList',
  wsiSopClassHandler: '@ohif/extension-cornerstone.sopClassHandlerModule.DicomMicroscopySopClassHandler'
};
const cornerstone = {
  measurements: '@ohif/extension-cornerstone.panelModule.panelMeasurement',
  segmentation: '@ohif/extension-cornerstone.panelModule.panelSegmentation'
};
const tracked = {
  measurements: '@ohif/extension-measurement-tracking.panelModule.trackedMeasurements',
  thumbnailList: '@ohif/extension-measurement-tracking.panelModule.seriesList',
  viewport: '@ohif/extension-measurement-tracking.viewportModule.cornerstone-tracked'
};
const dicomsr = {
  sopClassHandler: '@ohif/extension-cornerstone-dicom-sr.sopClassHandlerModule.dicom-sr',
  sopClassHandler3D: '@ohif/extension-cornerstone-dicom-sr.sopClassHandlerModule.dicom-sr-3d',
  viewport: '@ohif/extension-cornerstone-dicom-sr.viewportModule.dicom-sr'
};
const dicomvideo = {
  sopClassHandler: '@ohif/extension-dicom-video.sopClassHandlerModule.dicom-video',
  viewport: '@ohif/extension-dicom-video.viewportModule.dicom-video'
};
const dicompdf = {
  sopClassHandler: '@ohif/extension-dicom-pdf.sopClassHandlerModule.dicom-pdf',
  viewport: '@ohif/extension-dicom-pdf.viewportModule.dicom-pdf'
};
const dicomSeg = {
  sopClassHandler: '@ohif/extension-cornerstone-dicom-seg.sopClassHandlerModule.dicom-seg',
  viewport: '@ohif/extension-cornerstone-dicom-seg.viewportModule.dicom-seg'
};
const dicomPmap = {
  sopClassHandler: '@ohif/extension-cornerstone-dicom-pmap.sopClassHandlerModule.dicom-pmap',
  viewport: '@ohif/extension-cornerstone-dicom-pmap.viewportModule.dicom-pmap'
};
const dicomRT = {
  viewport: '@ohif/extension-cornerstone-dicom-rt.viewportModule.dicom-rt',
  sopClassHandler: '@ohif/extension-cornerstone-dicom-rt.sopClassHandlerModule.dicom-rt'
};
const extensionDependencies = {
  // Can derive the versions at least process.env.from npm_package_version
  '@ohif/extension-default': '^3.0.0',
  '@ohif/extension-cornerstone': '^3.0.0',
  '@ohif/extension-measurement-tracking': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-sr': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-seg': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-pmap': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-rt': '^3.0.0',
  '@ohif/extension-dicom-pdf': '^3.0.1',
  '@ohif/extension-dicom-video': '^3.0.1'
};
function modeFactory({
  modeConfiguration
}) {
  let _activatePanelTriggersSubscriptions = [];
  return {
    // TODO: We're using this as a route segment
    // We should not be.
    id: id,
    routeName: 'viewer',
    displayName: i18next/* default */.A.t('Modes:Basic Viewer'),
    /**
     * Lifecycle hooks
     */
    onModeEnter: function ({
      servicesManager,
      extensionManager,
      commandsManager
    }) {
      const {
        measurementService,
        toolbarService,
        toolGroupService,
        customizationService,
        panelService,
        segmentationService
      } = servicesManager.services;
      measurementService.clearMeasurements();
      performCustomizations(customizationService);

      // Init Default and SR ToolGroups
      src_initToolGroups(extensionManager, toolGroupService, commandsManager, this.labelConfig);
      toolbarService.addButtons([...src_toolbarButtons, ...src_moreTools]);
      toolbarService.createButtonSection('primary', ['MeasurementTools', 'Zoom', 'Pan', 'TrackballRotate', 'WindowLevel', 'Capture', 'Layout', 'Crosshairs', 'MoreTools']);

      // // ActivatePanel event trigger for when a segmentation or measurement is added.
      // // Do not force activation so as to respect the state the user may have left the UI in.
      _activatePanelTriggersSubscriptions = [...panelService.addActivatePanelTriggers(cornerstone.segmentation, [{
        sourcePubSubService: segmentationService,
        sourceEvents: [segmentationService.EVENTS.SEGMENTATION_ADDED]
      }]), ...panelService.addActivatePanelTriggers(tracked.measurements, [{
        sourcePubSubService: measurementService,
        sourceEvents: [measurementService.EVENTS.MEASUREMENT_ADDED, measurementService.EVENTS.RAW_MEASUREMENT_ADDED]
      }])];
    },
    onModeExit: ({
      servicesManager
    }) => {
      const {
        toolGroupService,
        syncGroupService,
        segmentationService,
        cornerstoneViewportService,
        uiDialogService,
        uiModalService
      } = servicesManager.services;
      _activatePanelTriggersSubscriptions.forEach(sub => sub.unsubscribe());
      _activatePanelTriggersSubscriptions = [];
      uiDialogService.dismissAll();
      uiModalService.hide();
      toolGroupService.destroy();
      syncGroupService.destroy();
      segmentationService.destroy();
      cornerstoneViewportService.destroy();
    },
    validationTags: {
      study: [],
      series: []
    },
    isValidMode: function ({
      modalities
    }) {
      const modalities_list = modalities.split('\\');

      // Exclude non-image modalities
      return {
        valid: !!modalities_list.filter(modality => NON_IMAGE_MODALITIES.indexOf(modality) === -1).length,
        description: 'The mode does not support studies that ONLY include the following modalities: SM, ECG, SEG, RTSTRUCT'
      };
    },
    routes: [{
      path: 'longitudinal',
      /*init: ({ servicesManager, extensionManager }) => {
        //defaultViewerRouteInit
      },*/
      layoutTemplate: () => {
        return {
          id: ohif.layout,
          props: {
            leftPanels: [tracked.thumbnailList],
            rightPanels: [cornerstone.segmentation, tracked.measurements],
            rightPanelClosed: true,
            viewports: [{
              namespace: tracked.viewport,
              displaySetsToDisplay: [ohif.sopClassHandler, dicomvideo.sopClassHandler, dicomsr.sopClassHandler3D, ohif.wsiSopClassHandler]
            }, {
              namespace: dicomsr.viewport,
              displaySetsToDisplay: [dicomsr.sopClassHandler]
            }, {
              namespace: dicompdf.viewport,
              displaySetsToDisplay: [dicompdf.sopClassHandler]
            }, {
              namespace: dicomSeg.viewport,
              displaySetsToDisplay: [dicomSeg.sopClassHandler]
            }, {
              namespace: dicomPmap.viewport,
              displaySetsToDisplay: [dicomPmap.sopClassHandler]
            }, {
              namespace: dicomRT.viewport,
              displaySetsToDisplay: [dicomRT.sopClassHandler]
            }]
          }
        };
      }
    }],
    extensions: extensionDependencies,
    // Default protocol gets self-registered by default in the init
    hangingProtocol: 'default',
    // Order is important in sop class handlers when two handlers both use
    // the same sop class under different situations.  In that case, the more
    // general handler needs to come last.  For this case, the dicomvideo must
    // come first to remove video transfer syntax before ohif uses images
    sopClassHandlers: [dicomvideo.sopClassHandler, dicomSeg.sopClassHandler, dicomPmap.sopClassHandler, ohif.sopClassHandler, ohif.wsiSopClassHandler, dicompdf.sopClassHandler, dicomsr.sopClassHandler3D, dicomsr.sopClassHandler, dicomRT.sopClassHandler],
    hotkeys: [...src/* hotkeys */.ot.defaults.hotkeyBindings],
    ...modeConfiguration
  };
}
const mode = {
  id: id,
  modeFactory,
  extensionDependencies
};
/* harmony default export */ const longitudinal_src = (mode);


/***/ })

}]);