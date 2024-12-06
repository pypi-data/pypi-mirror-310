"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[1374],{

/***/ 41374:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ basic_dev_mode_src)
});

// EXTERNAL MODULE: ../../ui/src/index.js + 690 modules
var src = __webpack_require__(35647);
// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var core_src = __webpack_require__(29463);
;// CONCATENATED MODULE: ../../../modes/basic-dev-mode/src/toolbarButtons.js


const {
  windowLevelPresets
} = core_src/* defaults */.NT;
function _createWwwcPreset(preset, title, subtitle) {
  return {
    id: preset.toString(),
    title,
    subtitle,
    commands: [{
      commandName: 'setWindowLevel',
      commandOptions: {
        ...windowLevelPresets[preset]
      },
      context: 'CORNERSTONE'
    }]
  };
}
function _createSetToolActiveCommands(toolName, toolGroupIds = ['default', 'mpr']) {
  return toolGroupIds.map(toolGroupId => ({
    commandName: 'setToolActive',
    commandOptions: {
      toolGroupId,
      toolName
    },
    context: 'CORNERSTONE'
  }));
}
const toolbarButtons = [{
  id: 'MeasurementTools',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'MeasurementTools',
    evaluate: 'evaluate.group.promoteToPrimaryIfCornerstoneToolNotActiveInTheList',
    primary: core_src/* ToolbarService */.hx.createButton({
      id: 'Length',
      icon: 'tool-length',
      label: 'Length',
      tooltip: 'Length Tool',
      commands: _createSetToolActiveCommands('Length'),
      evaluate: 'evaluate.cornerstoneTool'
    }),
    secondary: {
      icon: 'chevron-down',
      tooltip: 'More Measure Tools'
    },
    items: [core_src/* ToolbarService */.hx.createButton({
      id: 'Bidirectional',
      icon: 'tool-bidirectional',
      label: 'Bidirectional',
      tooltip: 'Bidirectional Tool',
      commands: _createSetToolActiveCommands('Bidirectional'),
      evaluate: 'evaluate.cornerstoneTool'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'EllipticalROI',
      icon: 'tool-ellipse',
      label: 'Ellipse',
      tooltip: 'Ellipse ROI',
      commands: _createSetToolActiveCommands('EllipticalROI'),
      evaluate: 'evaluate.cornerstoneTool'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'CircleROI',
      icon: 'tool-circle',
      label: 'Circle',
      tooltip: 'Circle Tool',
      commands: _createSetToolActiveCommands('CircleROI'),
      evaluate: 'evaluate.cornerstoneTool'
    })]
  }
}, {
  id: 'Zoom',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-zoom',
    label: 'Zoom',
    commands: _createSetToolActiveCommands('Zoom'),
    evaluate: 'evaluate.cornerstoneTool'
  }
}, {
  id: 'WindowLevel',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'WindowLevel',
    primary: core_src/* ToolbarService */.hx.createButton({
      id: 'WindowLevel',
      icon: 'tool-window-level',
      label: 'Window Level',
      tooltip: 'Window Level',
      commands: _createSetToolActiveCommands('WindowLevel'),
      evaluate: 'evaluate.cornerstoneTool'
    }),
    secondary: {
      icon: 'chevron-down',
      tooltip: 'W/L Presets'
    },
    renderer: src/* WindowLevelMenuItem */.d4,
    items: [_createWwwcPreset(1, 'Soft tissue', '400 / 40'), _createWwwcPreset(2, 'Lung', '1500 / -600'), _createWwwcPreset(3, 'Liver', '150 / 90'), _createWwwcPreset(4, 'Bone', '2500 / 480'), _createWwwcPreset(5, 'Brain', '80 / 40')]
  }
}, {
  id: 'Pan',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-move',
    label: 'Pan',
    commands: _createSetToolActiveCommands('Pan'),
    evaluate: 'evaluate.cornerstoneTool'
  }
}, {
  id: 'Capture',
  uiType: 'ohif.radioGroup',
  props: {
    icon: 'tool-capture',
    label: 'Capture',
    commands: [{
      commandName: 'showDownloadViewportModal',
      context: 'CORNERSTONE'
    }],
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
    commands: [{
      commandName: 'setViewportGridLayout'
    }]
  }
}, {
  id: 'MoreTools',
  uiType: 'ohif.splitButton',
  props: {
    groupId: 'MoreTools',
    evaluate: 'evaluate.group.promoteToPrimaryIfCornerstoneToolNotActiveInTheList',
    primary: core_src/* ToolbarService */.hx.createButton({
      id: 'Reset',
      icon: 'tool-reset',
      label: 'Reset View',
      tooltip: 'Reset View',
      commands: [{
        commandName: 'resetViewport',
        context: 'CORNERSTONE'
      }],
      evaluate: 'evaluate.action'
    }),
    secondary: {
      icon: 'chevron-down',
      tooltip: 'More Tools'
    },
    items: [core_src/* ToolbarService */.hx.createButton({
      id: 'Reset',
      icon: 'tool-reset',
      label: 'Reset View',
      tooltip: 'Reset View',
      commands: [{
        commandName: 'resetViewport',
        context: 'CORNERSTONE'
      }],
      evaluate: 'evaluate.action'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'RotateRight',
      icon: 'tool-rotate-right',
      label: 'Rotate Right',
      tooltip: 'Rotate Right +90',
      commands: [{
        commandName: 'rotateViewportCW',
        context: 'CORNERSTONE'
      }],
      evaluate: 'evaluate.action'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'FlipHorizontal',
      icon: 'tool-flip-horizontal',
      label: 'Flip Horizontally',
      tooltip: 'Flip Horizontally',
      commands: [{
        commandName: 'flipViewportHorizontal',
        context: 'CORNERSTONE'
      }],
      evaluate: 'evaluate.action'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'StackScroll',
      icon: 'tool-stack-scroll',
      label: 'Stack Scroll',
      tooltip: 'Stack Scroll',
      commands: _createSetToolActiveCommands('StackScroll'),
      evaluate: 'evaluate.cornerstoneTool'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'Invert',
      icon: 'tool-invert',
      label: 'Invert Colors',
      tooltip: 'Invert Colors',
      commands: [{
        commandName: 'invertViewport',
        context: 'CORNERSTONE'
      }],
      evaluate: 'evaluate.action'
    }), core_src/* ToolbarService */.hx.createButton({
      id: 'CalibrationLine',
      icon: 'tool-calibration',
      label: 'Calibration Line',
      tooltip: 'Calibration Line',
      commands: _createSetToolActiveCommands('CalibrationLine'),
      evaluate: 'evaluate.cornerstoneTool'
    })]
  }
}];
/* harmony default export */ const src_toolbarButtons = (toolbarButtons);
;// CONCATENATED MODULE: ../../../modes/basic-dev-mode/package.json
const package_namespaceObject = /*#__PURE__*/JSON.parse('{"UU":"@ohif/mode-basic-dev-mode"}');
;// CONCATENATED MODULE: ../../../modes/basic-dev-mode/src/id.js

const id = package_namespaceObject.UU;

// EXTERNAL MODULE: ../../../node_modules/i18next/dist/esm/i18next.js
var i18next = __webpack_require__(40680);
;// CONCATENATED MODULE: ../../../modes/basic-dev-mode/src/index.ts




const configs = {
  Length: {}
  //
};
const ohif = {
  layout: '@ohif/extension-default.layoutTemplateModule.viewerLayout',
  sopClassHandler: '@ohif/extension-default.sopClassHandlerModule.stack',
  measurements: '@ohif/extension-default.panelModule.measure',
  thumbnailList: '@ohif/extension-default.panelModule.seriesList'
};
const cs3d = {
  viewport: '@ohif/extension-cornerstone.viewportModule.cornerstone'
};
const dicomsr = {
  sopClassHandler: '@ohif/extension-cornerstone-dicom-sr.sopClassHandlerModule.dicom-sr',
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
const extensionDependencies = {
  '@ohif/extension-default': '^3.0.0',
  '@ohif/extension-cornerstone': '^3.0.0',
  '@ohif/extension-cornerstone-dicom-sr': '^3.0.0',
  '@ohif/extension-dicom-pdf': '^3.0.1',
  '@ohif/extension-dicom-video': '^3.0.1'
};
function modeFactory({
  modeConfiguration
}) {
  return {
    id: id,
    routeName: 'dev',
    displayName: i18next/* default */.A.t('Modes:Basic Dev Viewer'),
    /**
     * Lifecycle hooks
     */
    onModeEnter: ({
      servicesManager,
      extensionManager
    }) => {
      const {
        toolbarService,
        toolGroupService
      } = servicesManager.services;
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
          toolName: toolNames.Bidirectional
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
          toolName: toolNames.CalibrationLine
        }],
        // enabled
        enabled: [{
          toolName: toolNames.ImageOverlayViewer
        }]
        // disabled
      };
      toolGroupService.createToolGroupAndAddTools('default', tools);
      toolbarService.addButtons(src_toolbarButtons);
      toolbarService.createButtonSection('primary', ['MeasurementTools', 'Zoom', 'WindowLevel', 'Pan', 'Layout', 'MoreTools']);
    },
    onModeExit: ({
      servicesManager
    }) => {
      const {
        toolGroupService,
        measurementService,
        toolbarService,
        uiDialogService,
        uiModalService
      } = servicesManager.services;
      uiDialogService.dismissAll();
      uiModalService.hide();
      toolGroupService.destroy();
    },
    validationTags: {
      study: [],
      series: []
    },
    isValidMode: ({
      modalities
    }) => {
      const modalities_list = modalities.split('\\');

      // Slide Microscopy modality not supported by basic mode yet
      return {
        valid: !modalities_list.includes('SM'),
        description: 'The mode does not support the following modalities: SM'
      };
    },
    routes: [{
      path: 'viewer-cs3d',
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
            // TODO: Should be optional, or required to pass empty array for slots?
            leftPanels: [ohif.thumbnailList],
            rightPanels: [ohif.measurements],
            viewports: [{
              namespace: cs3d.viewport,
              displaySetsToDisplay: [ohif.sopClassHandler]
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
    sopClassHandlers: [dicomvideo.sopClassHandler, ohif.sopClassHandler, dicompdf.sopClassHandler, dicomsr.sopClassHandler],
    hotkeys: [...core_src/* hotkeys */.ot.defaults.hotkeyBindings]
  };
}
const mode = {
  id: id,
  modeFactory,
  extensionDependencies
};
/* harmony default export */ const basic_dev_mode_src = (mode);

/***/ })

}]);