"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[2068],{

/***/ 2068:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ monai_label_src)
});

// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var src = __webpack_require__(29463);
;// CONCATENATED MODULE: ../../../../modes/monai-label/package.json
const package_namespaceObject = /*#__PURE__*/JSON.parse('{"UU":"@ohif/mode-monai-label"}');
;// CONCATENATED MODULE: ../../../../modes/monai-label/src/id.js

const id = package_namespaceObject.UU;

;// CONCATENATED MODULE: ../../../../modes/monai-label/src/toolbarButtons.js

const {
  createButton
} = src/* ToolbarService */.hx;
const ReferenceLinesListeners = [{
  commandName: 'setSourceViewportForReferenceLinesTool',
  context: 'CORNERSTONE'
}];
const setToolActiveToolbar = {
  commandName: 'setToolActiveToolbar',
  commandOptions: {
    toolGroupIds: ['default', 'mpr', 'SRToolGroup', 'volume3d']
  }
};
const toolbarButtons = [{
  id: 'Zoom',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-zoom',
    label: 'Zoom',
    commands: setToolActiveToolbar,
    evaluate: 'evaluate.cornerstoneTool'
  }
}, {
  id: 'WindowLevel',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-window-level',
    label: 'Window Level',
    commands: setToolActiveToolbar,
    evaluate: 'evaluate.cornerstoneTool'
  }
}, {
  id: 'Pan',
  uiType: 'ohif.radioGroup',
  props: {
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
    evaluate: 'evaluate.action',
    commands: 'setViewportGridLayout'
  }
}, {
  id: 'Crosshairs',
  uiType: 'ohif.radioGroup',
  props: {
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
}, {
  id: 'MoreTools',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'MoreTools',
    evaluate: 'evaluate.group.promoteToPrimaryIfCornerstoneToolNotActiveInTheList',
    primary: createButton({
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
    items: [createButton({
      id: 'Reset',
      icon: 'tool-reset',
      label: 'Reset View',
      tooltip: 'Reset View',
      commands: 'resetViewport',
      evaluate: 'evaluate.action'
    }), createButton({
      id: 'rotate-right',
      icon: 'tool-rotate-right',
      label: 'Rotate Right',
      tooltip: 'Rotate +90',
      commands: 'rotateViewportCW',
      evaluate: 'evaluate.action'
    }), createButton({
      id: 'flipHorizontal',
      icon: 'tool-flip-horizontal',
      label: 'Flip Horizontal',
      tooltip: 'Flip Horizontally',
      commands: 'flipViewportHorizontal',
      evaluate: ['evaluate.viewportProperties.toggle', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['volume3d']
      }]
    }), createButton({
      id: 'ReferenceLines',
      icon: 'tool-referenceLines',
      label: 'Reference Lines',
      tooltip: 'Show Reference Lines',
      commands: 'toggleEnabledDisabledToolbar',
      listeners: {
        [src/* ViewportGridService */.sI.EVENTS.ACTIVE_VIEWPORT_ID_CHANGED]: ReferenceLinesListeners,
        [src/* ViewportGridService */.sI.EVENTS.VIEWPORTS_READY]: ReferenceLinesListeners
      },
      evaluate: 'evaluate.cornerstoneTool.toggle'
    }), createButton({
      id: 'ImageOverlayViewer',
      icon: 'toggle-dicom-overlay',
      label: 'Image Overlay',
      tooltip: 'Toggle Image Overlay',
      commands: 'toggleEnabledDisabledToolbar',
      evaluate: 'evaluate.cornerstoneTool.toggle'
    }), createButton({
      id: 'StackScroll',
      icon: 'tool-stack-scroll',
      label: 'Stack Scroll',
      tooltip: 'Stack Scroll',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'invert',
      icon: 'tool-invert',
      label: 'Invert',
      tooltip: 'Invert Colors',
      commands: 'invertViewport',
      evaluate: 'evaluate.viewportProperties.toggle'
    }), createButton({
      id: 'Probe',
      icon: 'tool-probe',
      label: 'Probe',
      tooltip: 'Probe',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'Cine',
      icon: 'tool-cine',
      label: 'Cine',
      tooltip: 'Cine',
      commands: 'toggleCine',
      evaluate: ['evaluate.cine', {
        name: 'evaluate.viewport.supported',
        unsupportedViewportTypes: ['volume3d']
      }]
    }), createButton({
      id: 'Angle',
      icon: 'tool-angle',
      label: 'Angle',
      tooltip: 'Angle',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'Magnify',
      icon: 'tool-magnify',
      label: 'Zoom-in',
      tooltip: 'Zoom-in',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'RectangleROI',
      icon: 'tool-rectangle',
      label: 'Rectangle',
      tooltip: 'Rectangle',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'CalibrationLine',
      icon: 'tool-calibration',
      label: 'Calibration',
      tooltip: 'Calibration Line',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    }), createButton({
      id: 'TagBrowser',
      icon: 'dicom-tag-browser',
      label: 'Dicom Tag Browser',
      tooltip: 'Dicom Tag Browser',
      commands: 'openDICOMTagViewer'
    }), createButton({
      id: 'AdvancedMagnify',
      icon: 'icon-tool-loupe',
      label: 'Magnify Probe',
      tooltip: 'Magnify Probe',
      commands: 'toggleActiveDisabledToolbar',
      evaluate: 'evaluate.cornerstoneTool.toggle.ifStrictlyDisabled'
    }), createButton({
      id: 'UltrasoundDirectionalTool',
      icon: 'icon-tool-ultrasound-bidirectional',
      label: 'Ultrasound Directional',
      tooltip: 'Ultrasound Directional',
      commands: setToolActiveToolbar,
      evaluate: ['evaluate.cornerstoneTool', {
        name: 'evaluate.modality.supported',
        supportedModalities: ['US']
      }]
    }), createButton({
      id: 'WindowLevelRegion',
      icon: 'icon-tool-window-region',
      label: 'Window Level Region',
      tooltip: 'Window Level Region',
      commands: setToolActiveToolbar,
      evaluate: 'evaluate.cornerstoneTool'
    })]
  }
}];
/* harmony default export */ const src_toolbarButtons = (toolbarButtons);
;// CONCATENATED MODULE: ../../../../modes/monai-label/src/initToolGroups.js
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
function createTools(utilityModule) {
  const {
    toolNames,
    Enums
  } = utilityModule.exports;
  return {
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
      toolName: 'CircularBrush',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'FILL_INSIDE_CIRCLE'
      }
    }, {
      toolName: 'CircularEraser',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'ERASE_INSIDE_CIRCLE'
      }
    }, {
      toolName: 'SphereBrush',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'FILL_INSIDE_SPHERE'
      }
    }, {
      toolName: 'SphereEraser',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'ERASE_INSIDE_SPHERE'
      }
    }, {
      toolName: 'ThresholdCircularBrush',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'THRESHOLD_INSIDE_CIRCLE'
      }
    }, {
      toolName: 'ThresholdSphereBrush',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'THRESHOLD_INSIDE_SPHERE'
      }
    }, {
      toolName: 'ThresholdCircularBrushDynamic',
      parentTool: 'Brush',
      configuration: {
        activeStrategy: 'THRESHOLD_INSIDE_CIRCLE',
        // preview: {
        //   enabled: true,
        // },
        strategySpecificConfiguration: {
          // to use the use the center segment index to determine
          // if inside -> same segment, if outside -> eraser
          // useCenterSegmentIndex: true,
          THRESHOLD: {
            isDynamic: true,
            dynamicRadius: 3
          }
        }
      }
    }, {
      toolName: toolNames.CircleScissors
    }, {
      toolName: toolNames.RectangleScissors
    }, {
      toolName: toolNames.SphereScissors
    }, {
      toolName: toolNames.StackScroll
    }, {
      toolName: toolNames.Magnify
    }, {
      toolName: toolNames.WindowLevelRegion
    }, {
      toolName: toolNames.UltrasoundDirectional
    }, {
      toolName: 'ProbeMONAILabel'
    }],
    disabled: [{
      toolName: toolNames.ReferenceLines
    }, {
      toolName: toolNames.AdvancedMagnify
    }]
  };
}
function initDefaultToolGroup(extensionManager, toolGroupService, commandsManager, toolGroupId) {
  const utilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.tools');
  const tools = createTools(utilityModule);
  toolGroupService.createToolGroupAndAddTools(toolGroupId, tools);
}
function initMPRToolGroup(extensionManager, toolGroupService, commandsManager) {
  const utilityModule = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.tools');
  const servicesManager = extensionManager._servicesManager;
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const tools = createTools(utilityModule);
  tools.disabled.push({
    toolName: utilityModule.exports.toolNames.Crosshairs,
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
    toolName: utilityModule.exports.toolNames.ReferenceLines
  });
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
function initToolGroups(extensionManager, toolGroupService, commandsManager) {
  initDefaultToolGroup(extensionManager, toolGroupService, commandsManager, 'default');
  initMPRToolGroup(extensionManager, toolGroupService, commandsManager);
  initVolume3DToolGroup(extensionManager, toolGroupService);
}
/* harmony default export */ const src_initToolGroups = (initToolGroups);
;// CONCATENATED MODULE: ../../../../modes/monai-label/src/index.tsx




const monailabel = {
  monaiLabel: '@ohif/extension-monai-label.panelModule.monailabel'
};
const ohif = {
  layout: '@ohif/extension-default.layoutTemplateModule.viewerLayout',
  sopClassHandler: '@ohif/extension-default.sopClassHandlerModule.stack',
  hangingProtocol: '@ohif/extension-default.hangingProtocolModule.default',
  leftPanel: '@ohif/extension-default.panelModule.seriesList',
  rightPanel: '@ohif/extension-default.panelModule.measure'
};
const cornerstone = {
  viewport: '@ohif/extension-cornerstone.viewportModule.cornerstone',
  panelTool: '@ohif/extension-cornerstone.panelModule.panelSegmentationWithTools'
};
const segmentation = {
  sopClassHandler: '@ohif/extension-cornerstone-dicom-seg.sopClassHandlerModule.dicom-seg',
  viewport: '@ohif/extension-cornerstone-dicom-seg.viewportModule.dicom-seg'
};

/**
 * Just two dependencies to be able to render a viewport with panels in order
 * to make sure that the mode is working.
 */
const extensionDependencies = {
  '@ohif/extension-default': '^3.0.0',
  '@ohif/extension-cornerstone': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-seg': '^3.0.0',
  '@ohif/extension-monai-label': '^3.0.0'
};
function modeFactory({
  modeConfiguration
}) {
  return {
    /**
     * Mode ID, which should be unique among modes used by the viewer. This ID
     * is used to identify the mode in the viewer's state.
     */
    id: id,
    routeName: 'monai-label',
    /**
     * Mode name, which is displayed in the viewer's UI in the workList, for the
     * user to select the mode.
     */
    displayName: 'MONAI Label',
    /**
     * Runs when the Mode Route is mounted to the DOM. Usually used to initialize
     * Services and other resources.
     */
    onModeEnter: ({
      servicesManager,
      extensionManager,
      commandsManager
    }) => {
      const {
        measurementService,
        toolbarService,
        toolGroupService
      } = servicesManager.services;
      measurementService.clearMeasurements();

      // Init Default and SR ToolGroups
      src_initToolGroups(extensionManager, toolGroupService, commandsManager);
      toolbarService.addButtons(src_toolbarButtons);
      // toolbarService.addButtons(segmentationButtons);

      toolbarService.createButtonSection('primary', ['WindowLevel', 'Pan', 'Zoom', 'TrackballRotate', 'Capture', 'Layout', 'MPR', 'Crosshairs', 'MoreTools']);
      toolbarService.createButtonSection('segmentationToolbox', ['BrushTools', 'Shapes']);
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
      uiDialogService.dismissAll();
      uiModalService.hide();
      toolGroupService.destroy();
      syncGroupService.destroy();
      segmentationService.destroy();
      cornerstoneViewportService.destroy();
    },
    /** */
    validationTags: {
      study: [],
      series: []
    },
    /**
     * A boolean return value that indicates whether the mode is valid for the
     * modalities of the selected studies. Currently we don't have stack viewport
     * segmentations and we should exclude them
     */
    isValidMode: ({
      modalities
    }) => {
      // Don't show the mode if the selected studies have only one modality
      // that is not supported by the mode
      const modalitiesArray = modalities.split('\\');
      return {
        valid: modalitiesArray.includes('CT') || modalitiesArray.includes('MR'),
        description: 'The mode does not support studies that ONLY include the following modalities: SM, OT, DOC'
      };
    },
    /**
     * Mode Routes are used to define the mode's behavior. A list of Mode Route
     * that includes the mode's path and the layout to be used. The layout will
     * include the components that are used in the layout. For instance, if the
     * default layoutTemplate is used (id: '@ohif/extension-default.layoutTemplateModule.viewerLayout')
     * it will include the leftPanels, rightPanels, and viewports. However, if
     * you define another layoutTemplate that includes a Footer for instance,
     * you should provide the Footer component here too. Note: We use Strings
     * to reference the component's ID as they are registered in the internal
     * ExtensionManager. The template for the string is:
     * `${extensionId}.{moduleType}.${componentId}`.
     */
    routes: [{
      path: 'monai-label',
      layoutTemplate: ({
        location,
        servicesManager
      }) => {
        return {
          id: ohif.layout,
          props: {
            rightPanelDefaultClosed: false,
            /* leftPanelDefaultClosed: true, */
            leftPanels: [ohif.leftPanel],
            rightPanels: [monailabel.monaiLabel],
            viewports: [{
              namespace: cornerstone.viewport,
              displaySetsToDisplay: [ohif.sopClassHandler]
            }, {
              namespace: segmentation.viewport,
              displaySetsToDisplay: [segmentation.sopClassHandler]
            }]
          }
        };
      }
    }],
    /** List of extensions that are used by the mode */
    extensions: extensionDependencies,
    /** HangingProtocol used by the mode */
    hangingProtocol: 'mpr',
    // hangingProtocol: [''],
    /** SopClassHandlers used by the mode */
    sopClassHandlers: [ohif.sopClassHandler, segmentation.sopClassHandler],
    /** hotkeys for mode */
    hotkeys: [...src/* hotkeys */.ot.defaults.hotkeyBindings]
  };
}
const mode = {
  id: id,
  modeFactory,
  extensionDependencies
};
/* harmony default export */ const monai_label_src = (mode);

/***/ })

}]);