"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[3200,2591,4182,1801],{

/***/ 79044:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  A: () => (/* binding */ src_getContextModule),
  B: () => (/* reexport */ useTrackedMeasurements)
});

// EXTERNAL MODULE: ../../../node_modules/react/index.js
var react = __webpack_require__(86326);
// EXTERNAL MODULE: ../../../node_modules/prop-types/index.js
var prop_types = __webpack_require__(97598);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);
// EXTERNAL MODULE: ../../../node_modules/xstate/es/index.js + 22 modules
var es = __webpack_require__(70574);
// EXTERNAL MODULE: ../../../node_modules/@xstate/react/es/index.js + 8 modules
var react_es = __webpack_require__(95261);
// EXTERNAL MODULE: ../../ui/src/index.js + 690 modules
var src = __webpack_require__(35647);
// EXTERNAL MODULE: ../../../extensions/default/src/index.ts + 114 modules
var default_src = __webpack_require__(71520);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/measurementTrackingMachine.js

const RESPONSE = {
  NO_NEVER: -1,
  CANCEL: 0,
  CREATE_REPORT: 1,
  ADD_SERIES: 2,
  SET_STUDY_AND_SERIES: 3,
  NO_NOT_FOR_SERIES: 4,
  HYDRATE_REPORT: 5
};
const machineConfiguration = {
  id: 'measurementTracking',
  initial: 'idle',
  context: {
    activeViewportId: null,
    trackedStudy: '',
    trackedSeries: [],
    ignoredSeries: [],
    //
    prevTrackedStudy: '',
    prevTrackedSeries: [],
    prevIgnoredSeries: [],
    //
    ignoredSRSeriesForHydration: [],
    isDirty: false
  },
  states: {
    off: {
      type: 'final'
    },
    labellingOnly: {
      on: {
        TRACK_SERIES: [{
          target: 'promptLabelAnnotation',
          actions: ['setPreviousState']
        }, {
          target: 'off'
        }]
      }
    },
    idle: {
      entry: 'clearContext',
      on: {
        TRACK_SERIES: [{
          target: 'promptLabelAnnotation',
          cond: 'isLabelOnMeasure',
          actions: ['setPreviousState']
        }, {
          target: 'promptBeginTracking',
          actions: ['setPreviousState']
        }],
        // Unused? We may only do PROMPT_HYDRATE_SR now?
        SET_TRACKED_SERIES: [{
          target: 'tracking',
          actions: ['setTrackedStudyAndMultipleSeries', 'setIsDirtyToClean']
        }],
        PROMPT_HYDRATE_SR: {
          target: 'promptHydrateStructuredReport',
          cond: 'hasNotIgnoredSRSeriesForHydration'
        },
        RESTORE_PROMPT_HYDRATE_SR: 'promptHydrateStructuredReport',
        HYDRATE_SR: 'hydrateStructuredReport',
        UPDATE_ACTIVE_VIEWPORT_ID: {
          actions: (0,es/* assign */.kp)({
            activeViewportId: (_, event) => event.activeViewportId
          })
        }
      }
    },
    promptBeginTracking: {
      invoke: {
        src: 'promptBeginTracking',
        onDone: [{
          target: 'tracking',
          actions: ['setTrackedStudyAndSeries', 'setIsDirty'],
          cond: 'shouldSetStudyAndSeries'
        }, {
          target: 'labellingOnly',
          cond: 'isLabelOnMeasureAndShouldKillMachine'
        }, {
          target: 'off',
          cond: 'shouldKillMachine'
        }, {
          target: 'idle'
        }],
        onError: {
          target: 'idle'
        }
      }
    },
    tracking: {
      on: {
        TRACK_SERIES: [{
          target: 'promptLabelAnnotation',
          cond: 'isLabelOnMeasure',
          actions: ['setPreviousState']
        }, {
          target: 'promptTrackNewStudy',
          cond: 'isNewStudy'
        }, {
          target: 'promptTrackNewSeries',
          cond: 'isNewSeries'
        }],
        UNTRACK_SERIES: [{
          target: 'tracking',
          actions: ['removeTrackedSeries', 'setIsDirty'],
          cond: 'hasRemainingTrackedSeries'
        }, {
          target: 'idle'
        }],
        SET_TRACKED_SERIES: [{
          target: 'tracking',
          actions: ['setTrackedStudyAndMultipleSeries']
        }],
        SAVE_REPORT: 'promptSaveReport',
        SET_DIRTY: [{
          target: 'tracking',
          actions: ['setIsDirty'],
          cond: 'shouldSetDirty'
        }, {
          target: 'tracking'
        }]
      }
    },
    promptTrackNewSeries: {
      invoke: {
        src: 'promptTrackNewSeries',
        onDone: [{
          target: 'tracking',
          actions: ['addTrackedSeries', 'setIsDirty'],
          cond: 'shouldAddSeries'
        }, {
          target: 'tracking',
          actions: ['discardPreviouslyTrackedMeasurements', 'setTrackedStudyAndSeries', 'setIsDirty'],
          cond: 'shouldSetStudyAndSeries'
        }, {
          target: 'promptSaveReport',
          cond: 'shouldPromptSaveReport'
        }, {
          target: 'tracking'
        }],
        onError: {
          target: 'idle'
        }
      }
    },
    promptTrackNewStudy: {
      invoke: {
        src: 'promptTrackNewStudy',
        onDone: [{
          target: 'tracking',
          actions: ['discardPreviouslyTrackedMeasurements', 'setTrackedStudyAndSeries', 'setIsDirty'],
          cond: 'shouldSetStudyAndSeries'
        }, {
          target: 'tracking',
          actions: ['ignoreSeries'],
          cond: 'shouldAddIgnoredSeries'
        }, {
          target: 'promptSaveReport',
          cond: 'shouldPromptSaveReport'
        }, {
          target: 'tracking'
        }],
        onError: {
          target: 'idle'
        }
      }
    },
    promptSaveReport: {
      invoke: {
        src: 'promptSaveReport',
        onDone: [
        // "clicked the save button"
        // - should clear all measurements
        // - show DICOM SR
        {
          target: 'idle',
          actions: ['clearAllMeasurements', 'showStructuredReportDisplaySetInActiveViewport'],
          cond: 'shouldSaveAndContinueWithSameReport'
        },
        // "starting a new report"
        // - remove "just saved" measurements
        // - start tracking a new study + report
        {
          target: 'tracking',
          actions: ['discardPreviouslyTrackedMeasurements', 'setTrackedStudyAndSeries'],
          cond: 'shouldSaveAndStartNewReport'
        },
        // Cancel, back to tracking
        {
          target: 'tracking'
        }],
        onError: {
          target: 'idle'
        }
      }
    },
    promptHydrateStructuredReport: {
      invoke: {
        src: 'promptHydrateStructuredReport',
        onDone: [{
          target: 'tracking',
          actions: ['setTrackedStudyAndMultipleSeries', 'jumpToSameImageInActiveViewport', 'setIsDirtyToClean'],
          cond: 'shouldHydrateStructuredReport'
        }, {
          target: 'idle',
          actions: ['ignoreHydrationForSRSeries'],
          cond: 'shouldIgnoreHydrationForSR'
        }],
        onError: {
          target: 'idle'
        }
      }
    },
    hydrateStructuredReport: {
      invoke: {
        src: 'hydrateStructuredReport',
        onDone: [{
          target: 'tracking',
          actions: ['setTrackedStudyAndMultipleSeries', 'jumpToSameImageInActiveViewport', 'setIsDirtyToClean']
        }],
        onError: {
          target: 'idle'
        }
      }
    },
    promptLabelAnnotation: {
      invoke: {
        src: 'promptLabelAnnotation',
        onDone: [{
          target: 'labellingOnly',
          cond: 'wasLabellingOnly'
        }, {
          target: 'promptBeginTracking',
          cond: 'wasIdle'
        }, {
          target: 'promptTrackNewStudy',
          cond: 'wasTrackingAndIsNewStudy'
        }, {
          target: 'promptTrackNewSeries',
          cond: 'wasTrackingAndIsNewSeries'
        }, {
          target: 'tracking',
          cond: 'wasTracking'
        }, {
          target: 'off'
        }]
      }
    }
  },
  strict: true
};
const defaultOptions = {
  services: {
    promptBeginTracking: (ctx, evt) => {
      // return { userResponse, StudyInstanceUID, SeriesInstanceUID }
    },
    promptTrackNewStudy: (ctx, evt) => {
      // return { userResponse, StudyInstanceUID, SeriesInstanceUID }
    },
    promptTrackNewSeries: (ctx, evt) => {
      // return { userResponse, StudyInstanceUID, SeriesInstanceUID }
    }
  },
  actions: {
    discardPreviouslyTrackedMeasurements: (ctx, evt) => {
      console.log('discardPreviouslyTrackedMeasurements: not implemented');
    },
    clearAllMeasurements: (ctx, evt) => {
      console.log('clearAllMeasurements: not implemented');
    },
    jumpToFirstMeasurementInActiveViewport: (ctx, evt) => {
      console.warn('jumpToFirstMeasurementInActiveViewport: not implemented');
    },
    showStructuredReportDisplaySetInActiveViewport: (ctx, evt) => {
      console.warn('showStructuredReportDisplaySetInActiveViewport: not implemented');
    },
    clearContext: (0,es/* assign */.kp)({
      trackedStudy: '',
      trackedSeries: [],
      ignoredSeries: [],
      prevTrackedStudy: '',
      prevTrackedSeries: [],
      prevIgnoredSeries: []
    }),
    // Promise resolves w/ `evt.data.*`
    setTrackedStudyAndSeries: (0,es/* assign */.kp)((ctx, evt) => ({
      prevTrackedStudy: ctx.trackedStudy,
      prevTrackedSeries: ctx.trackedSeries.slice(),
      prevIgnoredSeries: ctx.ignoredSeries.slice(),
      //
      trackedStudy: evt.data.StudyInstanceUID,
      trackedSeries: [evt.data.SeriesInstanceUID],
      ignoredSeries: []
    })),
    setTrackedStudyAndMultipleSeries: (0,es/* assign */.kp)((ctx, evt) => {
      const studyInstanceUID = evt.StudyInstanceUID || evt.data.StudyInstanceUID;
      const seriesInstanceUIDs = evt.SeriesInstanceUIDs || evt.data.SeriesInstanceUIDs;
      return {
        prevTrackedStudy: ctx.trackedStudy,
        prevTrackedSeries: ctx.trackedSeries.slice(),
        prevIgnoredSeries: ctx.ignoredSeries.slice(),
        //
        trackedStudy: studyInstanceUID,
        trackedSeries: [...ctx.trackedSeries, ...seriesInstanceUIDs],
        ignoredSeries: []
      };
    }),
    setIsDirtyToClean: (0,es/* assign */.kp)((ctx, evt) => ({
      isDirty: false
    })),
    setIsDirty: (0,es/* assign */.kp)((ctx, evt) => ({
      isDirty: true
    })),
    ignoreSeries: (0,es/* assign */.kp)((ctx, evt) => ({
      prevIgnoredSeries: [...ctx.ignoredSeries],
      ignoredSeries: [...ctx.ignoredSeries, evt.data.SeriesInstanceUID]
    })),
    ignoreHydrationForSRSeries: (0,es/* assign */.kp)((ctx, evt) => ({
      ignoredSRSeriesForHydration: [...ctx.ignoredSRSeriesForHydration, evt.data.srSeriesInstanceUID]
    })),
    addTrackedSeries: (0,es/* assign */.kp)((ctx, evt) => ({
      prevTrackedSeries: [...ctx.trackedSeries],
      trackedSeries: [...ctx.trackedSeries, evt.data.SeriesInstanceUID]
    })),
    removeTrackedSeries: (0,es/* assign */.kp)((ctx, evt) => ({
      prevTrackedSeries: ctx.trackedSeries.slice().filter(ser => ser !== evt.SeriesInstanceUID),
      trackedSeries: ctx.trackedSeries.slice().filter(ser => ser !== evt.SeriesInstanceUID)
    })),
    setPreviousState: (0,es/* assign */.kp)((ctx, evt, meta) => {
      return {
        prevState: meta.state.value
      };
    })
  },
  guards: {
    // We set dirty any time we performan an action that:
    // - Tracks a new study
    // - Tracks a new series
    // - Adds a measurement to an already tracked study/series
    //
    // We set clean any time we restore from an SR
    //
    // This guard/condition is specific to "new measurements"
    // to make sure we only track dirty when the new measurement is specific
    // to a series we're already tracking
    //
    // tl;dr
    // Any report change, that is not a hydration of an existing report, should
    // result in a "dirty" report
    //
    // Where dirty means there would be "loss of data" if we blew away measurements
    // without creating a new SR.
    shouldSetDirty: (ctx, evt) => {
      return (
        // When would this happen?
        evt.SeriesInstanceUID === undefined || ctx.trackedSeries.includes(evt.SeriesInstanceUID)
      );
    },
    wasLabellingOnly: (ctx, evt, condMeta) => {
      return ctx.prevState === 'labellingOnly';
    },
    wasIdle: (ctx, evt, condMeta) => {
      return ctx.prevState === 'idle';
    },
    wasTracking: (ctx, evt, condMeta) => {
      return ctx.prevState === 'tracking';
    },
    wasTrackingAndIsNewStudy: (ctx, evt, condMeta) => {
      return ctx.prevState === 'tracking' && !ctx.ignoredSeries.includes(evt.data.SeriesInstanceUID) && ctx.trackedStudy !== evt.data.StudyInstanceUID;
    },
    wasTrackingAndIsNewSeries: (ctx, evt, condMeta) => {
      return ctx.prevState === 'tracking' && !ctx.ignoredSeries.includes(evt.data.SeriesInstanceUID) && !ctx.trackedSeries.includes(evt.data.SeriesInstanceUID);
    },
    shouldKillMachine: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.NO_NEVER,
    shouldAddSeries: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.ADD_SERIES,
    shouldSetStudyAndSeries: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.SET_STUDY_AND_SERIES,
    shouldAddIgnoredSeries: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.NO_NOT_FOR_SERIES,
    shouldPromptSaveReport: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.CREATE_REPORT,
    shouldIgnoreHydrationForSR: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.CANCEL,
    shouldSaveAndContinueWithSameReport: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.CREATE_REPORT && evt.data.isBackupSave === true,
    shouldSaveAndStartNewReport: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.CREATE_REPORT && evt.data.isBackupSave === false,
    shouldHydrateStructuredReport: (ctx, evt) => evt.data && evt.data.userResponse === RESPONSE.HYDRATE_REPORT,
    // Has more than 1, or SeriesInstanceUID is not in list
    // --> Post removal would have non-empty trackedSeries array
    hasRemainingTrackedSeries: (ctx, evt) => ctx.trackedSeries.length > 1 || !ctx.trackedSeries.includes(evt.SeriesInstanceUID),
    hasNotIgnoredSRSeriesForHydration: (ctx, evt) => {
      return !ctx.ignoredSRSeriesForHydration.includes(evt.SeriesInstanceUID);
    },
    isNewStudy: (ctx, evt) => !ctx.ignoredSeries.includes(evt.SeriesInstanceUID) && ctx.trackedStudy !== evt.StudyInstanceUID,
    isNewSeries: (ctx, evt) => !ctx.ignoredSeries.includes(evt.SeriesInstanceUID) && !ctx.trackedSeries.includes(evt.SeriesInstanceUID)
  }
};

// EXTERNAL MODULE: ../../../node_modules/i18next/dist/esm/i18next.js
var i18next = __webpack_require__(40680);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/promptBeginTracking.js


const promptBeginTracking_RESPONSE = {
  NO_NEVER: -1,
  CANCEL: 0,
  CREATE_REPORT: 1,
  ADD_SERIES: 2,
  SET_STUDY_AND_SERIES: 3
};
function promptBeginTracking({
  servicesManager,
  extensionManager
}, ctx, evt) {
  const {
    uiViewportDialogService
  } = servicesManager.services;
  const appConfig = extensionManager._appConfig;
  // When the state change happens after a promise, the state machine sends the retult in evt.data;
  // In case of direct transition to the state, the state machine sends the data in evt;
  const {
    viewportId,
    StudyInstanceUID,
    SeriesInstanceUID
  } = evt.data || evt;
  return new Promise(async function (resolve, reject) {
    let promptResult = appConfig?.disableConfirmationPrompts ? promptBeginTracking_RESPONSE.SET_STUDY_AND_SERIES : await _askTrackMeasurements(uiViewportDialogService, viewportId);
    resolve({
      userResponse: promptResult,
      StudyInstanceUID,
      SeriesInstanceUID,
      viewportId
    });
  });
}
function _askTrackMeasurements(uiViewportDialogService, viewportId) {
  return new Promise(function (resolve, reject) {
    const message = i18next/* default */.A.t('MeasurementTable:Track measurements for this series?');
    const actions = [{
      id: 'prompt-begin-tracking-cancel',
      type: src/* ButtonEnums.type */.Ny.NW.secondary,
      text: i18next/* default */.A.t('Common:No'),
      value: promptBeginTracking_RESPONSE.CANCEL
    }, {
      id: 'prompt-begin-tracking-no-do-not-ask-again',
      type: src/* ButtonEnums.type */.Ny.NW.secondary,
      text: i18next/* default */.A.t('MeasurementTable:No, do not ask again'),
      value: promptBeginTracking_RESPONSE.NO_NEVER
    }, {
      id: 'prompt-begin-tracking-yes',
      type: src/* ButtonEnums.type */.Ny.NW.primary,
      text: i18next/* default */.A.t('Common:Yes'),
      value: promptBeginTracking_RESPONSE.SET_STUDY_AND_SERIES
    }];
    const onSubmit = result => {
      uiViewportDialogService.hide();
      resolve(result);
    };
    uiViewportDialogService.show({
      viewportId,
      id: 'measurement-tracking-prompt-begin-tracking',
      type: 'info',
      message,
      actions,
      onSubmit,
      onOutsideClick: () => {
        uiViewportDialogService.hide();
        resolve(promptBeginTracking_RESPONSE.CANCEL);
      },
      onKeyPress: event => {
        if (event.key === 'Enter') {
          const action = actions.find(action => action.id === 'prompt-begin-tracking-yes');
          onSubmit(action.value);
        }
      }
    });
  });
}
/* harmony default export */ const TrackedMeasurementsContext_promptBeginTracking = (promptBeginTracking);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/promptTrackNewSeries.js

const promptTrackNewSeries_RESPONSE = {
  NO_NEVER: -1,
  CANCEL: 0,
  CREATE_REPORT: 1,
  ADD_SERIES: 2,
  SET_STUDY_AND_SERIES: 3,
  NO_NOT_FOR_SERIES: 4
};
function promptTrackNewSeries({
  servicesManager,
  extensionManager
}, ctx, evt) {
  const {
    UIViewportDialogService
  } = servicesManager.services;
  // When the state change happens after a promise, the state machine sends the retult in evt.data;
  // In case of direct transition to the state, the state machine sends the data in evt;
  const {
    viewportId,
    StudyInstanceUID,
    SeriesInstanceUID
  } = evt.data || evt;
  return new Promise(async function (resolve, reject) {
    let promptResult = await _askShouldAddMeasurements(UIViewportDialogService, viewportId);
    if (promptResult === promptTrackNewSeries_RESPONSE.CREATE_REPORT) {
      promptResult = ctx.isDirty ? await _askSaveDiscardOrCancel(UIViewportDialogService, viewportId) : promptTrackNewSeries_RESPONSE.SET_STUDY_AND_SERIES;
    }
    resolve({
      userResponse: promptResult,
      StudyInstanceUID,
      SeriesInstanceUID,
      viewportId,
      isBackupSave: false
    });
  });
}
function _askShouldAddMeasurements(uiViewportDialogService, viewportId) {
  return new Promise(function (resolve, reject) {
    const message = 'Do you want to add this measurement to the existing report?';
    const actions = [{
      type: src/* ButtonEnums.type */.Ny.NW.secondary,
      text: 'Cancel',
      value: promptTrackNewSeries_RESPONSE.CANCEL
    }, {
      type: src/* ButtonEnums.type */.Ny.NW.primary,
      text: 'Create new report',
      value: promptTrackNewSeries_RESPONSE.CREATE_REPORT
    }, {
      type: src/* ButtonEnums.type */.Ny.NW.primary,
      text: 'Add to existing report',
      value: promptTrackNewSeries_RESPONSE.ADD_SERIES
    }];
    const onSubmit = result => {
      uiViewportDialogService.hide();
      resolve(result);
    };
    uiViewportDialogService.show({
      viewportId,
      type: 'info',
      message,
      actions,
      onSubmit,
      onOutsideClick: () => {
        uiViewportDialogService.hide();
        resolve(promptTrackNewSeries_RESPONSE.CANCEL);
      }
    });
  });
}
function _askSaveDiscardOrCancel(UIViewportDialogService, viewportId) {
  return new Promise(function (resolve, reject) {
    const message = 'You have existing tracked measurements. What would you like to do with your existing tracked measurements?';
    const actions = [{
      type: 'cancel',
      text: 'Cancel',
      value: promptTrackNewSeries_RESPONSE.CANCEL
    }, {
      type: 'secondary',
      text: 'Save',
      value: promptTrackNewSeries_RESPONSE.CREATE_REPORT
    }, {
      type: 'primary',
      text: 'Discard',
      value: promptTrackNewSeries_RESPONSE.SET_STUDY_AND_SERIES
    }];
    const onSubmit = result => {
      UIViewportDialogService.hide();
      resolve(result);
    };
    UIViewportDialogService.show({
      viewportId,
      type: 'warning',
      message,
      actions,
      onSubmit,
      onOutsideClick: () => {
        UIViewportDialogService.hide();
        resolve(promptTrackNewSeries_RESPONSE.CANCEL);
      }
    });
  });
}
/* harmony default export */ const TrackedMeasurementsContext_promptTrackNewSeries = (promptTrackNewSeries);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/promptTrackNewStudy.ts

const promptTrackNewStudy_RESPONSE = {
  NO_NEVER: -1,
  CANCEL: 0,
  CREATE_REPORT: 1,
  ADD_SERIES: 2,
  SET_STUDY_AND_SERIES: 3,
  NO_NOT_FOR_SERIES: 4
};
function promptTrackNewStudy({
  servicesManager,
  extensionManager
}, ctx, evt) {
  const {
    uiViewportDialogService
  } = servicesManager.services;
  // When the state change happens after a promise, the state machine sends the retult in evt.data;
  // In case of direct transition to the state, the state machine sends the data in evt;
  const {
    viewportId,
    StudyInstanceUID,
    SeriesInstanceUID
  } = evt.data || evt;
  return new Promise(async function (resolve, reject) {
    let promptResult = await promptTrackNewStudy_askTrackMeasurements(uiViewportDialogService, viewportId);
    if (promptResult === promptTrackNewStudy_RESPONSE.SET_STUDY_AND_SERIES) {
      promptResult = ctx.isDirty ? await promptTrackNewStudy_askSaveDiscardOrCancel(uiViewportDialogService, viewportId) : promptTrackNewStudy_RESPONSE.SET_STUDY_AND_SERIES;
    }
    resolve({
      userResponse: promptResult,
      StudyInstanceUID,
      SeriesInstanceUID,
      viewportId,
      isBackupSave: false
    });
  });
}
function promptTrackNewStudy_askTrackMeasurements(UIViewportDialogService, viewportId) {
  return new Promise(function (resolve, reject) {
    const message = i18next/* default */.A.t('MeasurementTable:Track measurements for this series?');
    const actions = [{
      type: 'cancel',
      text: i18next/* default */.A.t('MeasurementTable:No'),
      value: promptTrackNewStudy_RESPONSE.CANCEL
    }, {
      type: 'secondary',
      text: i18next/* default */.A.t('MeasurementTable:No, do not ask again'),
      value: promptTrackNewStudy_RESPONSE.NO_NOT_FOR_SERIES
    }, {
      type: 'primary',
      text: i18next/* default */.A.t('MeasurementTable:Yes'),
      value: promptTrackNewStudy_RESPONSE.SET_STUDY_AND_SERIES
    }];
    const onSubmit = result => {
      UIViewportDialogService.hide();
      resolve(result);
    };
    UIViewportDialogService.show({
      viewportId,
      type: 'info',
      message,
      actions,
      onSubmit,
      onOutsideClick: () => {
        UIViewportDialogService.hide();
        resolve(promptTrackNewStudy_RESPONSE.CANCEL);
      },
      onKeyPress: event => {
        if (event.key === 'Enter') {
          const action = actions.find(action => action.value === promptTrackNewStudy_RESPONSE.SET_STUDY_AND_SERIES);
          onSubmit(action.value);
        }
      }
    });
  });
}
function promptTrackNewStudy_askSaveDiscardOrCancel(UIViewportDialogService, viewportId) {
  return new Promise(function (resolve, reject) {
    const message = 'Measurements cannot span across multiple studies. Do you want to save your tracked measurements?';
    const actions = [{
      type: 'cancel',
      text: 'Cancel',
      value: promptTrackNewStudy_RESPONSE.CANCEL
    }, {
      type: 'secondary',
      text: 'No, discard previously tracked series & measurements',
      value: promptTrackNewStudy_RESPONSE.SET_STUDY_AND_SERIES
    }, {
      type: 'primary',
      text: 'Yes',
      value: promptTrackNewStudy_RESPONSE.CREATE_REPORT
    }];
    const onSubmit = result => {
      UIViewportDialogService.hide();
      resolve(result);
    };
    UIViewportDialogService.show({
      viewportId,
      type: 'warning',
      message,
      actions,
      onSubmit,
      onOutsideClick: () => {
        UIViewportDialogService.hide();
        resolve(promptTrackNewStudy_RESPONSE.CANCEL);
      }
    });
  });
}
/* harmony default export */ const TrackedMeasurementsContext_promptTrackNewStudy = (promptTrackNewStudy);
// EXTERNAL MODULE: ../../../extensions/cornerstone-dicom-sr/src/index.tsx + 16 modules
var cornerstone_dicom_sr_src = __webpack_require__(85687);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/promptHydrateStructuredReport.js


const promptHydrateStructuredReport_RESPONSE = {
  NO_NEVER: -1,
  CANCEL: 0,
  CREATE_REPORT: 1,
  ADD_SERIES: 2,
  SET_STUDY_AND_SERIES: 3,
  NO_NOT_FOR_SERIES: 4,
  HYDRATE_REPORT: 5
};
function promptHydrateStructuredReport({
  servicesManager,
  extensionManager,
  appConfig
}, ctx, evt) {
  const {
    uiViewportDialogService,
    displaySetService
  } = servicesManager.services;
  const {
    viewportId,
    displaySetInstanceUID
  } = evt;
  const srDisplaySet = displaySetService.getDisplaySetByUID(displaySetInstanceUID);
  return new Promise(async function (resolve, reject) {
    const promptResult = appConfig?.disableConfirmationPrompts ? promptHydrateStructuredReport_RESPONSE.HYDRATE_REPORT : await promptHydrateStructuredReport_askTrackMeasurements(uiViewportDialogService, viewportId);

    // Need to do action here... So we can set state...
    let StudyInstanceUID, SeriesInstanceUIDs;
    if (promptResult === promptHydrateStructuredReport_RESPONSE.HYDRATE_REPORT) {
      console.warn('!! HYDRATING STRUCTURED REPORT');
      const hydrationResult = (0,cornerstone_dicom_sr_src.hydrateStructuredReport)({
        servicesManager,
        extensionManager,
        appConfig
      }, displaySetInstanceUID);
      StudyInstanceUID = hydrationResult.StudyInstanceUID;
      SeriesInstanceUIDs = hydrationResult.SeriesInstanceUIDs;
    }
    resolve({
      userResponse: promptResult,
      displaySetInstanceUID: evt.displaySetInstanceUID,
      srSeriesInstanceUID: srDisplaySet.SeriesInstanceUID,
      viewportId,
      StudyInstanceUID,
      SeriesInstanceUIDs
    });
  });
}
function promptHydrateStructuredReport_askTrackMeasurements(uiViewportDialogService, viewportId) {
  return new Promise(function (resolve, reject) {
    const message = 'Do you want to continue tracking measurements for this study?';
    const actions = [{
      id: 'no-hydrate',
      type: src/* ButtonEnums.type */.Ny.NW.secondary,
      text: 'No',
      value: promptHydrateStructuredReport_RESPONSE.CANCEL
    }, {
      id: 'yes-hydrate',
      type: src/* ButtonEnums.type */.Ny.NW.primary,
      text: 'Yes',
      value: promptHydrateStructuredReport_RESPONSE.HYDRATE_REPORT
    }];
    const onSubmit = result => {
      uiViewportDialogService.hide();
      resolve(result);
    };
    uiViewportDialogService.show({
      viewportId,
      type: 'info',
      message,
      actions,
      onSubmit,
      onOutsideClick: () => {
        uiViewportDialogService.hide();
        resolve(promptHydrateStructuredReport_RESPONSE.CANCEL);
      },
      onKeyPress: event => {
        if (event.key === 'Enter') {
          const action = actions.find(action => action.value === promptHydrateStructuredReport_RESPONSE.HYDRATE_REPORT);
          onSubmit(action.value);
        }
      }
    });
  });
}
/* harmony default export */ const TrackedMeasurementsContext_promptHydrateStructuredReport = (promptHydrateStructuredReport);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/hydrateStructuredReport.tsx

function hydrateStructuredReport({
  servicesManager,
  extensionManager,
  appConfig
}, ctx, evt) {
  const {
    displaySetService
  } = servicesManager.services;
  const {
    viewportId,
    displaySetInstanceUID
  } = evt;
  const srDisplaySet = displaySetService.getDisplaySetByUID(displaySetInstanceUID);
  return new Promise((resolve, reject) => {
    const hydrationResult = (0,cornerstone_dicom_sr_src.hydrateStructuredReport)({
      servicesManager,
      extensionManager,
      appConfig
    }, displaySetInstanceUID);
    const StudyInstanceUID = hydrationResult.StudyInstanceUID;
    const SeriesInstanceUIDs = hydrationResult.SeriesInstanceUIDs;
    resolve({
      displaySetInstanceUID: evt.displaySetInstanceUID,
      srSeriesInstanceUID: srDisplaySet.SeriesInstanceUID,
      viewportId,
      StudyInstanceUID,
      SeriesInstanceUIDs
    });
  });
}
/* harmony default export */ const TrackedMeasurementsContext_hydrateStructuredReport = (hydrateStructuredReport);
// EXTERNAL MODULE: ./state/index.js + 1 modules
var state = __webpack_require__(45981);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/TrackedMeasurementsContext.tsx













const TrackedMeasurementsContext = /*#__PURE__*/react.createContext();
TrackedMeasurementsContext.displayName = 'TrackedMeasurementsContext';
const useTrackedMeasurements = () => (0,react.useContext)(TrackedMeasurementsContext);
const SR_SOPCLASSHANDLERID = '@ohif/extension-cornerstone-dicom-sr.sopClassHandlerModule.dicom-sr';

/**
 *
 * @param {*} param0
 */
function TrackedMeasurementsContextProvider({
  servicesManager,
  commandsManager,
  extensionManager
},
// Bound by consumer
{
  children
} // Component props
) {
  const [appConfig] = (0,state/* useAppConfig */.r)();
  const [viewportGrid, viewportGridService] = (0,src/* useViewportGrid */.ih)();
  const {
    activeViewportId,
    viewports
  } = viewportGrid;
  const {
    measurementService,
    displaySetService,
    customizationService
  } = servicesManager.services;
  const machineOptions = Object.assign({}, defaultOptions);
  machineOptions.actions = Object.assign({}, machineOptions.actions, {
    jumpToFirstMeasurementInActiveViewport: (ctx, evt) => {
      const {
        trackedStudy,
        trackedSeries,
        activeViewportId
      } = ctx;
      const measurements = measurementService.getMeasurements();
      const trackedMeasurements = measurements.filter(m => trackedStudy === m.referenceStudyUID && trackedSeries.includes(m.referenceSeriesUID));
      console.log('jumping to measurement reset viewport', activeViewportId, trackedMeasurements[0]);
      const referencedDisplaySetUID = trackedMeasurements[0].displaySetInstanceUID;
      const referencedDisplaySet = displaySetService.getDisplaySetByUID(referencedDisplaySetUID);
      const referencedImages = referencedDisplaySet.images;
      const isVolumeIdReferenced = referencedImages[0].imageId.startsWith('volumeId');
      const measurementData = trackedMeasurements[0].data;
      let imageIndex = 0;
      if (!isVolumeIdReferenced && measurementData) {
        // if it is imageId referenced find the index of the imageId, we don't have
        // support for volumeId referenced images yet
        imageIndex = referencedImages.findIndex(image => {
          const imageIdToUse = Object.keys(measurementData)[0].substring(8);
          return image.imageId === imageIdToUse;
        });
        if (imageIndex === -1) {
          console.warn('Could not find image index for tracked measurement, using 0');
          imageIndex = 0;
        }
      }
      viewportGridService.setDisplaySetsForViewport({
        viewportId: activeViewportId,
        displaySetInstanceUIDs: [referencedDisplaySetUID],
        viewportOptions: {
          initialImageOptions: {
            index: imageIndex
          }
        }
      });
    },
    jumpToSameImageInActiveViewport: (ctx, evt) => {
      const {
        trackedStudy,
        trackedSeries,
        activeViewportId
      } = ctx;
      const measurements = measurementService.getMeasurements();
      const trackedMeasurements = measurements.filter(m => trackedStudy === m.referenceStudyUID && trackedSeries.includes(m.referenceSeriesUID));
      const trackedMeasurement = trackedMeasurements[0];
      const referencedDisplaySetUID = trackedMeasurement.displaySetInstanceUID;

      // update the previously stored positionPresentation with the new viewportId
      // presentation so that when we put the referencedDisplaySet back in the viewport
      // it will be in the correct position zoom and pan
      commandsManager.runCommand('updateStoredPositionPresentation', {
        viewportId: activeViewportId,
        displaySetInstanceUID: referencedDisplaySetUID
      });
      viewportGridService.setDisplaySetsForViewport({
        viewportId: activeViewportId,
        displaySetInstanceUIDs: [referencedDisplaySetUID]
      });
    },
    showStructuredReportDisplaySetInActiveViewport: (ctx, evt) => {
      if (evt.data.createdDisplaySetInstanceUIDs.length > 0) {
        const StructuredReportDisplaySetInstanceUID = evt.data.createdDisplaySetInstanceUIDs[0];
        viewportGridService.setDisplaySetsForViewport({
          viewportId: evt.data.viewportId,
          displaySetInstanceUIDs: [StructuredReportDisplaySetInstanceUID]
        });
      }
    },
    discardPreviouslyTrackedMeasurements: (ctx, evt) => {
      const measurements = measurementService.getMeasurements();
      const filteredMeasurements = measurements.filter(ms => ctx.prevTrackedSeries.includes(ms.referenceSeriesUID));
      const measurementIds = filteredMeasurements.map(fm => fm.id);
      for (let i = 0; i < measurementIds.length; i++) {
        measurementService.remove(measurementIds[i]);
      }
    },
    clearAllMeasurements: (ctx, evt) => {
      const measurements = measurementService.getMeasurements();
      const measurementIds = measurements.map(fm => fm.uid);
      for (let i = 0; i < measurementIds.length; i++) {
        measurementService.remove(measurementIds[i]);
      }
    }
  });
  machineOptions.services = Object.assign({}, machineOptions.services, {
    promptBeginTracking: TrackedMeasurementsContext_promptBeginTracking.bind(null, {
      servicesManager,
      extensionManager,
      appConfig
    }),
    promptTrackNewSeries: TrackedMeasurementsContext_promptTrackNewSeries.bind(null, {
      servicesManager,
      extensionManager,
      appConfig
    }),
    promptTrackNewStudy: TrackedMeasurementsContext_promptTrackNewStudy.bind(null, {
      servicesManager,
      extensionManager,
      appConfig
    }),
    promptSaveReport: default_src.promptSaveReport.bind(null, {
      servicesManager,
      commandsManager,
      extensionManager,
      appConfig
    }),
    promptHydrateStructuredReport: TrackedMeasurementsContext_promptHydrateStructuredReport.bind(null, {
      servicesManager,
      extensionManager,
      appConfig
    }),
    hydrateStructuredReport: TrackedMeasurementsContext_hydrateStructuredReport.bind(null, {
      servicesManager,
      extensionManager,
      appConfig
    }),
    promptLabelAnnotation: default_src.promptLabelAnnotation.bind(null, {
      servicesManager,
      extensionManager
    })
  });
  machineOptions.guards = Object.assign({}, machineOptions.guards, {
    isLabelOnMeasure: (ctx, evt, condMeta) => {
      const labelConfig = customizationService.get('measurementLabels');
      return labelConfig?.labelOnMeasure;
    },
    isLabelOnMeasureAndShouldKillMachine: (ctx, evt, condMeta) => {
      const labelConfig = customizationService.get('measurementLabels');
      return evt.data && evt.data.userResponse === RESPONSE.NO_NEVER && labelConfig?.labelOnMeasure;
    }
  });

  // TODO: IMPROVE
  // - Add measurement_updated to cornerstone; debounced? (ext side, or consumption?)
  // - Friendlier transition/api in front of measurementTracking machine?
  // - Blocked: viewport overlay shouldn't clip when resized
  // TODO: PRIORITY
  // - Fix "ellipses" series description dynamic truncate length
  // - Fix viewport border resize
  // - created/destroyed hooks for extensions (cornerstone measurement subscriptions in it's `init`)

  const measurementTrackingMachine = (0,react.useMemo)(() => {
    return (0,es/* Machine */.u5)(machineConfiguration, machineOptions);
  }, []); // Empty dependency array ensures this is only created once

  const [trackedMeasurements, sendTrackedMeasurementsEvent] = (0,react_es/* useMachine */.zl)(measurementTrackingMachine);
  (0,react.useEffect)(() => {
    // Update the state machine with the active viewport ID
    sendTrackedMeasurementsEvent('UPDATE_ACTIVE_VIEWPORT_ID', {
      activeViewportId
    });
  }, [activeViewportId, sendTrackedMeasurementsEvent]);

  // ~~ Listen for changes to ViewportGrid for potential SRs hung in panes when idle
  (0,react.useEffect)(() => {
    const triggerPromptHydrateFlow = async () => {
      if (viewports.size > 0) {
        const activeViewport = viewports.get(activeViewportId);
        if (!activeViewport || !activeViewport?.displaySetInstanceUIDs?.length) {
          return;
        }

        // Todo: Getting the first displaySetInstanceUID is wrong, but we don't have
        // tracking fusion viewports yet. This should change when we do.
        const {
          displaySetService
        } = servicesManager.services;
        const displaySet = displaySetService.getDisplaySetByUID(activeViewport.displaySetInstanceUIDs[0]);
        if (!displaySet) {
          return;
        }

        // If this is an SR produced by our SR SOPClassHandler,
        // and it hasn't been loaded yet, do that now so we
        // can check if it can be rehydrated or not.
        //
        // Note: This happens:
        // - If the viewport is not currently an OHIFCornerstoneSRViewport
        // - If the displaySet has never been hung
        //
        // Otherwise, the displaySet will be loaded by the useEffect handler
        // listening to displaySet changes inside OHIFCornerstoneSRViewport.
        // The issue here is that this handler in TrackedMeasurementsContext
        // ends up occurring before the Viewport is created, so the displaySet
        // is not loaded yet, and isRehydratable is undefined unless we call load().
        if (displaySet.SOPClassHandlerId === SR_SOPCLASSHANDLERID && !displaySet.isLoaded && displaySet.load) {
          await displaySet.load();
        }

        // Magic string
        // load function added by our sopClassHandler module
        if (displaySet.SOPClassHandlerId === SR_SOPCLASSHANDLERID && displaySet.isRehydratable === true) {
          console.log('sending event...', trackedMeasurements);
          sendTrackedMeasurementsEvent('PROMPT_HYDRATE_SR', {
            displaySetInstanceUID: displaySet.displaySetInstanceUID,
            SeriesInstanceUID: displaySet.SeriesInstanceUID,
            viewportId: activeViewportId
          });
        }
      }
    };
    triggerPromptHydrateFlow();
  }, [trackedMeasurements, activeViewportId, sendTrackedMeasurementsEvent, servicesManager.services, viewports]);
  return /*#__PURE__*/react.createElement(TrackedMeasurementsContext.Provider, {
    value: [trackedMeasurements, sendTrackedMeasurementsEvent]
  }, children);
}
TrackedMeasurementsContextProvider.propTypes = {
  children: prop_types_default().oneOf([(prop_types_default()).func, (prop_types_default()).node]),
  servicesManager: (prop_types_default()).object.isRequired,
  commandsManager: (prop_types_default()).object.isRequired,
  extensionManager: (prop_types_default()).object.isRequired,
  appConfig: (prop_types_default()).object
};

;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/TrackedMeasurementsContext/index.js

;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/contexts/index.js

;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/getContextModule.tsx

function getContextModule({
  servicesManager,
  extensionManager,
  commandsManager
}) {
  const BoundTrackedMeasurementsContextProvider = TrackedMeasurementsContextProvider.bind(null, {
    servicesManager,
    extensionManager,
    commandsManager
  });
  return [{
    name: 'TrackedMeasurementsContext',
    context: TrackedMeasurementsContext,
    provider: BoundTrackedMeasurementsContextProvider
  }];
}

/* harmony default export */ const src_getContextModule = (getContextModule);

/***/ }),

/***/ 71903:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ measurement_tracking_src)
});

// EXTERNAL MODULE: ../../../extensions/measurement-tracking/src/getContextModule.tsx + 9 modules
var getContextModule = __webpack_require__(79044);
// EXTERNAL MODULE: ../../../node_modules/react/index.js
var react = __webpack_require__(86326);
// EXTERNAL MODULE: ../../../node_modules/prop-types/index.js
var prop_types = __webpack_require__(97598);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);
// EXTERNAL MODULE: ../node_modules/react-router-dom/dist/index.js
var dist = __webpack_require__(49348);
// EXTERNAL MODULE: ../../../node_modules/react-i18next/dist/es/index.js + 15 modules
var es = __webpack_require__(99993);
// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var src = __webpack_require__(29463);
// EXTERNAL MODULE: ../../ui/src/index.js + 690 modules
var ui_src = __webpack_require__(35647);
// EXTERNAL MODULE: ../../ui-next/src/index.ts + 2483 modules
var ui_next_src = __webpack_require__(35570);
// EXTERNAL MODULE: ../../../extensions/default/src/index.ts + 114 modules
var default_src = __webpack_require__(71520);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/constants/actionIcons.ts
const defaultActionIcons = [{
  id: 'settings',
  iconName: 'Settings',
  value: false
}];

;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/constants/viewPresets.ts
const defaultViewPresets = [{
  id: 'list',
  iconName: 'ListView',
  selected: false
}, {
  id: 'thumbnails',
  iconName: 'ThumbnailView',
  selected: true
}];

;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/constants/index.ts



;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/PanelStudyBrowserTracking.tsx











const {
  formatDate,
  createStudyBrowserTabs
} = src/* utils */.Wp;
const thumbnailNoImageModalities = ['SR', 'SEG', 'SM', 'RTSTRUCT', 'RTPLAN', 'RTDOSE', 'DOC', 'OT', 'PMAP'];
/**
 *
 * @param {*} param0
 */
function PanelStudyBrowserTracking({
  servicesManager,
  getImageSrc,
  getStudiesForPatientByMRN,
  requestDisplaySetCreationForStudy,
  dataSource,
  commandsManager
}) {
  const {
    displaySetService,
    uiDialogService,
    hangingProtocolService,
    uiNotificationService,
    measurementService,
    studyPrefetcherService,
    customizationService
  } = servicesManager.services;
  const navigate = (0,dist/* useNavigate */.Zp)();
  const {
    t
  } = (0,es/* useTranslation */.Bd)('Common');

  // Normally you nest the components so the tree isn't so deep, and the data
  // doesn't have to have such an intense shape. This works well enough for now.
  // Tabs --> Studies --> DisplaySets --> Thumbnails
  const {
    StudyInstanceUIDs
  } = (0,ui_src/* useImageViewer */.Bz)();
  const [{
    activeViewportId,
    viewports,
    isHangingProtocolLayout
  }, viewportGridService] = (0,ui_src/* useViewportGrid */.ih)();
  const [trackedMeasurements, sendTrackedMeasurementsEvent] = (0,getContextModule/* useTrackedMeasurements */.B)();
  const [activeTabName, setActiveTabName] = (0,react.useState)('all');
  const [expandedStudyInstanceUIDs, setExpandedStudyInstanceUIDs] = (0,react.useState)([...StudyInstanceUIDs]);
  const [studyDisplayList, setStudyDisplayList] = (0,react.useState)([]);
  const [hasLoadedViewports, setHasLoadedViewports] = (0,react.useState)(false);
  const [displaySets, setDisplaySets] = (0,react.useState)([]);
  const [displaySetsLoadingState, setDisplaySetsLoadingState] = (0,react.useState)({});
  const [thumbnailImageSrcMap, setThumbnailImageSrcMap] = (0,react.useState)({});
  const [jumpToDisplaySet, setJumpToDisplaySet] = (0,react.useState)(null);
  const [viewPresets, setViewPresets] = (0,react.useState)(customizationService.getCustomization('studyBrowser.viewPresets')?.value || defaultViewPresets);
  const [actionIcons, setActionIcons] = (0,react.useState)(defaultActionIcons);
  const updateActionIconValue = actionIcon => {
    actionIcon.value = !actionIcon.value;
    const newActionIcons = [...actionIcons];
    setActionIcons(newActionIcons);
  };
  const updateViewPresetValue = viewPreset => {
    if (!viewPreset) {
      return;
    }
    const newViewPresets = viewPresets.map(preset => {
      preset.selected = preset.id === viewPreset.id;
      return preset;
    });
    setViewPresets(newViewPresets);
  };
  const onDoubleClickThumbnailHandler = displaySetInstanceUID => {
    let updatedViewports = [];
    const viewportId = activeViewportId;
    try {
      updatedViewports = hangingProtocolService.getViewportsRequireUpdate(viewportId, displaySetInstanceUID, isHangingProtocolLayout);
    } catch (error) {
      console.warn(error);
      uiNotificationService.show({
        title: 'Thumbnail Double Click',
        message: 'The selected display sets could not be added to the viewport due to a mismatch in the Hanging Protocol rules.',
        type: 'error',
        duration: 3000
      });
    }
    viewportGridService.setDisplaySetsForViewports(updatedViewports);
  };
  const activeViewportDisplaySetInstanceUIDs = viewports.get(activeViewportId)?.displaySetInstanceUIDs;
  const {
    trackedSeries
  } = trackedMeasurements.context;

  // ~~ studyDisplayList
  (0,react.useEffect)(() => {
    // Fetch all studies for the patient in each primary study
    async function fetchStudiesForPatient(StudyInstanceUID) {
      // current study qido
      const qidoForStudyUID = await dataSource.query.studies.search({
        studyInstanceUid: StudyInstanceUID
      });
      if (!qidoForStudyUID?.length) {
        navigate('/notfoundstudy', '_self');
        throw new Error('Invalid study URL');
      }
      let qidoStudiesForPatient = qidoForStudyUID;

      // try to fetch the prior studies based on the patientID if the
      // server can respond.
      try {
        qidoStudiesForPatient = await getStudiesForPatientByMRN(qidoForStudyUID);
      } catch (error) {
        console.warn(error);
      }
      const mappedStudies = _mapDataSourceStudies(qidoStudiesForPatient);
      const actuallyMappedStudies = mappedStudies.map(qidoStudy => {
        return {
          studyInstanceUid: qidoStudy.StudyInstanceUID,
          date: formatDate(qidoStudy.StudyDate) || t('NoStudyDate'),
          description: qidoStudy.StudyDescription,
          modalities: qidoStudy.ModalitiesInStudy,
          numInstances: qidoStudy.NumInstances
        };
      });
      setStudyDisplayList(prevArray => {
        const ret = [...prevArray];
        for (const study of actuallyMappedStudies) {
          if (!prevArray.find(it => it.studyInstanceUid === study.studyInstanceUid)) {
            ret.push(study);
          }
        }
        return ret;
      });
    }
    StudyInstanceUIDs.forEach(sid => fetchStudiesForPatient(sid));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [StudyInstanceUIDs, getStudiesForPatientByMRN]);

  // ~~ Initial Thumbnails
  (0,react.useEffect)(() => {
    if (!hasLoadedViewports) {
      if (activeViewportId) {
        // Once there is an active viewport id, it means the layout is ready
        // so wait a bit of time to allow the viewports preferential loading
        // which improves user experience of responsiveness significantly on slower
        // systems.
        window.setTimeout(() => setHasLoadedViewports(true), 250);
      }
      return;
    }
    let currentDisplaySets = displaySetService.activeDisplaySets;
    // filter non based on the list of modalities that are supported by cornerstone
    currentDisplaySets = currentDisplaySets.filter(ds => !thumbnailNoImageModalities.includes(ds.Modality));
    if (!currentDisplaySets.length) {
      return;
    }
    currentDisplaySets.forEach(async dSet => {
      const newImageSrcEntry = {};
      const displaySet = displaySetService.getDisplaySetByUID(dSet.displaySetInstanceUID);
      const imageIds = dataSource.getImageIdsForDisplaySet(displaySet);
      const imageId = getImageIdForThumbnail(displaySet, imageIds);

      // TODO: Is it okay that imageIds are not returned here for SR displaySets?
      if (!imageId || displaySet?.unsupported) {
        return;
      }
      // When the image arrives, render it and store the result in the thumbnailImgSrcMap
      newImageSrcEntry[dSet.displaySetInstanceUID] = await getImageSrc(imageId);
      setThumbnailImageSrcMap(prevState => {
        return {
          ...prevState,
          ...newImageSrcEntry
        };
      });
    });
  }, [displaySetService, dataSource, getImageSrc, activeViewportId, hasLoadedViewports]);

  // ~~ displaySets
  (0,react.useEffect)(() => {
    const currentDisplaySets = displaySetService.activeDisplaySets;
    if (!currentDisplaySets.length) {
      return;
    }
    const mappedDisplaySets = _mapDisplaySets(currentDisplaySets, displaySetsLoadingState, thumbnailImageSrcMap, trackedSeries, viewports, viewportGridService, dataSource, displaySetService, uiDialogService, uiNotificationService);
    setDisplaySets(mappedDisplaySets);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [displaySetService.activeDisplaySets, displaySetsLoadingState, trackedSeries, viewports, dataSource, thumbnailImageSrcMap]);

  // -- displaySetsLoadingState
  (0,react.useEffect)(() => {
    const {
      unsubscribe
    } = studyPrefetcherService.subscribe(studyPrefetcherService.EVENTS.DISPLAYSET_LOAD_PROGRESS, updatedDisplaySetLoadingState => {
      const {
        displaySetInstanceUID,
        loadingProgress
      } = updatedDisplaySetLoadingState;
      setDisplaySetsLoadingState(prevState => ({
        ...prevState,
        [displaySetInstanceUID]: loadingProgress
      }));
    });
    return () => unsubscribe();
  }, [studyPrefetcherService]);

  // ~~ subscriptions --> displaySets
  (0,react.useEffect)(() => {
    // DISPLAY_SETS_ADDED returns an array of DisplaySets that were added
    const SubscriptionDisplaySetsAdded = displaySetService.subscribe(displaySetService.EVENTS.DISPLAY_SETS_ADDED, data => {
      if (!hasLoadedViewports) {
        return;
      }
      const {
        displaySetsAdded,
        options
      } = data;
      displaySetsAdded.forEach(async dSet => {
        const displaySetInstanceUID = dSet.displaySetInstanceUID;
        const newImageSrcEntry = {};
        const displaySet = displaySetService.getDisplaySetByUID(displaySetInstanceUID);
        if (displaySet?.unsupported) {
          return;
        }
        if (options.madeInClient) {
          setJumpToDisplaySet(displaySetInstanceUID);
        }
        const imageIds = dataSource.getImageIdsForDisplaySet(displaySet);
        const imageId = getImageIdForThumbnail(displaySet, imageIds);

        // TODO: Is it okay that imageIds are not returned here for SR displaysets?
        if (!imageId) {
          return;
        }

        // When the image arrives, render it and store the result in the thumbnailImgSrcMap
        newImageSrcEntry[displaySetInstanceUID] = await getImageSrc(imageId);
        setThumbnailImageSrcMap(prevState => {
          return {
            ...prevState,
            ...newImageSrcEntry
          };
        });
      });
    });
    return () => {
      SubscriptionDisplaySetsAdded.unsubscribe();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [displaySetService, dataSource, getImageSrc, thumbnailImageSrcMap, trackedSeries, viewports]);
  (0,react.useEffect)(() => {
    // TODO: Will this always hold _all_ the displaySets we care about?
    // DISPLAY_SETS_CHANGED returns `DisplaySerService.activeDisplaySets`
    const SubscriptionDisplaySetsChanged = displaySetService.subscribe(displaySetService.EVENTS.DISPLAY_SETS_CHANGED, changedDisplaySets => {
      const mappedDisplaySets = _mapDisplaySets(changedDisplaySets, displaySetsLoadingState, thumbnailImageSrcMap, trackedSeries, viewports, viewportGridService, dataSource, displaySetService, uiDialogService, uiNotificationService);
      setDisplaySets(mappedDisplaySets);
    });
    const SubscriptionDisplaySetMetaDataInvalidated = displaySetService.subscribe(displaySetService.EVENTS.DISPLAY_SET_SERIES_METADATA_INVALIDATED, () => {
      const mappedDisplaySets = _mapDisplaySets(displaySetService.getActiveDisplaySets(), displaySetsLoadingState, thumbnailImageSrcMap, trackedSeries, viewports, viewportGridService, dataSource, displaySetService, uiDialogService, uiNotificationService);
      setDisplaySets(mappedDisplaySets);
    });
    return () => {
      SubscriptionDisplaySetsChanged.unsubscribe();
      SubscriptionDisplaySetMetaDataInvalidated.unsubscribe();
    };
  }, [displaySetsLoadingState, thumbnailImageSrcMap, trackedSeries, viewports, dataSource, displaySetService]);
  const tabs = createStudyBrowserTabs(StudyInstanceUIDs, studyDisplayList, displaySets);

  // TODO: Should not fire this on "close"
  function _handleStudyClick(StudyInstanceUID) {
    const shouldCollapseStudy = expandedStudyInstanceUIDs.includes(StudyInstanceUID);
    const updatedExpandedStudyInstanceUIDs = shouldCollapseStudy ? [...expandedStudyInstanceUIDs.filter(stdyUid => stdyUid !== StudyInstanceUID)] : [...expandedStudyInstanceUIDs, StudyInstanceUID];
    setExpandedStudyInstanceUIDs(updatedExpandedStudyInstanceUIDs);
    if (!shouldCollapseStudy) {
      const madeInClient = true;
      requestDisplaySetCreationForStudy(displaySetService, StudyInstanceUID, madeInClient);
    }
  }
  (0,react.useEffect)(() => {
    if (jumpToDisplaySet) {
      // Get element by displaySetInstanceUID
      const displaySetInstanceUID = jumpToDisplaySet;
      const element = document.getElementById(`thumbnail-${displaySetInstanceUID}`);
      if (element && typeof element.scrollIntoView === 'function') {
        // TODO: Any way to support IE here?
        element.scrollIntoView({
          behavior: 'smooth'
        });
        setJumpToDisplaySet(null);
      }
    }
  }, [jumpToDisplaySet, expandedStudyInstanceUIDs, activeTabName]);
  (0,react.useEffect)(() => {
    if (!jumpToDisplaySet) {
      return;
    }
    const displaySetInstanceUID = jumpToDisplaySet;
    // Set the activeTabName and expand the study
    const thumbnailLocation = _findTabAndStudyOfDisplaySet(displaySetInstanceUID, tabs);
    if (!thumbnailLocation) {
      console.warn('jumpToThumbnail: displaySet thumbnail not found.');
      return;
    }
    const {
      tabName,
      StudyInstanceUID
    } = thumbnailLocation;
    setActiveTabName(tabName);
    const studyExpanded = expandedStudyInstanceUIDs.includes(StudyInstanceUID);
    if (!studyExpanded) {
      const updatedExpandedStudyInstanceUIDs = [...expandedStudyInstanceUIDs, StudyInstanceUID];
      setExpandedStudyInstanceUIDs(updatedExpandedStudyInstanceUIDs);
    }
  }, [expandedStudyInstanceUIDs, jumpToDisplaySet, tabs]);
  const onClickUntrack = displaySetInstanceUID => {
    const onConfirm = () => {
      const displaySet = displaySetService.getDisplaySetByUID(displaySetInstanceUID);
      sendTrackedMeasurementsEvent('UNTRACK_SERIES', {
        SeriesInstanceUID: displaySet.SeriesInstanceUID
      });
      const measurements = measurementService.getMeasurements();
      measurements.forEach(m => {
        if (m.referenceSeriesUID === displaySet.SeriesInstanceUID) {
          measurementService.remove(m.uid);
        }
      });
    };
    uiDialogService.create({
      id: 'untrack-series',
      centralize: true,
      isDraggable: false,
      showOverlay: true,
      content: ui_src/* Dialog */.lG,
      contentProps: {
        title: 'Untrack Series',
        body: () => /*#__PURE__*/react.createElement("div", {
          className: "bg-primary-dark p-4 text-white"
        }, /*#__PURE__*/react.createElement("p", null, "Are you sure you want to untrack this series?"), /*#__PURE__*/react.createElement("p", {
          className: "mt-2"
        }, "This action cannot be undone and will delete all your existing measurements.")),
        actions: [{
          id: 'cancel',
          text: 'Cancel',
          type: ui_src/* ButtonEnums.type */.Ny.NW.secondary
        }, {
          id: 'yes',
          text: 'Yes',
          type: ui_src/* ButtonEnums.type */.Ny.NW.primary,
          classes: ['untrack-yes-button']
        }],
        onClose: () => uiDialogService.dismiss({
          id: 'untrack-series'
        }),
        onSubmit: async ({
          action
        }) => {
          switch (action.id) {
            case 'yes':
              onConfirm();
              uiDialogService.dismiss({
                id: 'untrack-series'
              });
              break;
            case 'cancel':
              uiDialogService.dismiss({
                id: 'untrack-series'
              });
              break;
          }
        }
      }
    });
  };
  const onThumbnailContextMenu = (commandName, options) => {
    commandsManager.runCommand(commandName, options);
  };
  return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement(default_src.PanelStudyBrowserHeader, {
    viewPresets: viewPresets,
    updateViewPresetValue: updateViewPresetValue,
    actionIcons: actionIcons,
    updateActionIconValue: updateActionIconValue
  }), /*#__PURE__*/react.createElement(ui_next_src/* Separator */.wv, {
    orientation: "horizontal",
    className: "bg-black",
    thickness: "2px"
  })), /*#__PURE__*/react.createElement(ui_next_src/* StudyBrowser */.M4, {
    tabs: tabs,
    servicesManager: servicesManager,
    activeTabName: activeTabName,
    expandedStudyInstanceUIDs: expandedStudyInstanceUIDs,
    onClickStudy: _handleStudyClick,
    onClickTab: clickedTabName => {
      setActiveTabName(clickedTabName);
    },
    onClickUntrack: displaySetInstanceUID => {
      onClickUntrack(displaySetInstanceUID);
    },
    onClickThumbnail: () => {},
    onDoubleClickThumbnail: onDoubleClickThumbnailHandler,
    activeDisplaySetInstanceUIDs: activeViewportDisplaySetInstanceUIDs,
    showSettings: actionIcons.find(icon => icon.id === 'settings').value,
    viewPresets: viewPresets,
    onThumbnailContextMenu: onThumbnailContextMenu
  }));
}
PanelStudyBrowserTracking.propTypes = {
  servicesManager: (prop_types_default()).object.isRequired,
  dataSource: prop_types_default().shape({
    getImageIdsForDisplaySet: (prop_types_default()).func.isRequired
  }).isRequired,
  getImageSrc: (prop_types_default()).func.isRequired,
  getStudiesForPatientByMRN: (prop_types_default()).func.isRequired,
  requestDisplaySetCreationForStudy: (prop_types_default()).func.isRequired
};
/* harmony default export */ const PanelStudyBrowserTracking_PanelStudyBrowserTracking = (PanelStudyBrowserTracking);
function getImageIdForThumbnail(displaySet, imageIds) {
  let imageId;
  if (displaySet.isDynamicVolume) {
    const timePoints = displaySet.dynamicVolumeInfo.timePoints;
    const middleIndex = Math.floor(timePoints.length / 2);
    const middleTimePointImageIds = timePoints[middleIndex];
    imageId = middleTimePointImageIds[Math.floor(middleTimePointImageIds.length / 2)];
  } else {
    imageId = imageIds[Math.floor(imageIds.length / 2)];
  }
  return imageId;
}

/**
 * Maps from the DataSource's format to a naturalized object
 *
 * @param {*} studies
 */
function _mapDataSourceStudies(studies) {
  return studies.map(study => {
    // TODO: Why does the data source return in this format?
    return {
      AccessionNumber: study.accession,
      StudyDate: study.date,
      StudyDescription: study.description,
      NumInstances: study.instances,
      ModalitiesInStudy: study.modalities,
      PatientID: study.mrn,
      PatientName: study.patientName,
      StudyInstanceUID: study.studyInstanceUid,
      StudyTime: study.time
    };
  });
}
function _mapDisplaySets(displaySets, displaySetLoadingState, thumbnailImageSrcMap, trackedSeriesInstanceUIDs, viewports,
// TODO: make array of `displaySetInstanceUIDs`?
viewportGridService, dataSource, displaySetService, uiDialogService, uiNotificationService) {
  const thumbnailDisplaySets = [];
  const thumbnailNoImageDisplaySets = [];
  displaySets.filter(ds => !ds.excludeFromThumbnailBrowser).forEach(ds => {
    const imageSrc = thumbnailImageSrcMap[ds.displaySetInstanceUID];
    const componentType = _getComponentType(ds);
    const numPanes = viewportGridService.getNumViewportPanes();
    const array = componentType === 'thumbnailTracked' ? thumbnailDisplaySets : thumbnailNoImageDisplaySets;
    const {
      displaySetInstanceUID
    } = ds;
    const loadingProgress = displaySetLoadingState?.[displaySetInstanceUID];
    const thumbnailProps = {
      displaySetInstanceUID,
      description: ds.SeriesDescription,
      seriesNumber: ds.SeriesNumber,
      modality: ds.Modality,
      seriesDate: formatDate(ds.SeriesDate),
      numInstances: ds.numImageFrames,
      loadingProgress,
      countIcon: ds.countIcon,
      messages: ds.messages,
      StudyInstanceUID: ds.StudyInstanceUID,
      componentType,
      imageSrc,
      dragData: {
        type: 'displayset',
        displaySetInstanceUID
        // .. Any other data to pass
      },
      isTracked: trackedSeriesInstanceUIDs.includes(ds.SeriesInstanceUID),
      isHydratedForDerivedDisplaySet: ds.isHydrated
    };
    if (componentType === 'thumbnailNoImage') {
      if (dataSource.reject && dataSource.reject.series) {
        thumbnailProps.canReject = !ds?.unsupported;
        thumbnailProps.onReject = () => {
          uiDialogService.create({
            id: 'ds-reject-sr',
            centralize: true,
            isDraggable: false,
            showOverlay: true,
            content: ui_src/* Dialog */.lG,
            contentProps: {
              title: 'Delete Report',
              body: () => /*#__PURE__*/react.createElement("div", {
                className: "bg-primary-dark p-4 text-white"
              }, /*#__PURE__*/react.createElement("p", null, "Are you sure you want to delete this report?"), /*#__PURE__*/react.createElement("p", {
                className: "mt-2"
              }, "This action cannot be undone.")),
              actions: [{
                id: 'cancel',
                text: 'Cancel',
                type: ui_src/* ButtonEnums.type */.Ny.NW.secondary
              }, {
                id: 'yes',
                text: 'Yes',
                type: ui_src/* ButtonEnums.type */.Ny.NW.primary,
                classes: ['reject-yes-button']
              }],
              onClose: () => uiDialogService.dismiss({
                id: 'ds-reject-sr'
              }),
              onShow: () => {
                const yesButton = document.querySelector('.reject-yes-button');
                yesButton.focus();
              },
              onSubmit: async ({
                action
              }) => {
                switch (action.id) {
                  case 'yes':
                    try {
                      await dataSource.reject.series(ds.StudyInstanceUID, ds.SeriesInstanceUID);
                      displaySetService.deleteDisplaySet(displaySetInstanceUID);
                      uiDialogService.dismiss({
                        id: 'ds-reject-sr'
                      });
                      uiNotificationService.show({
                        title: 'Delete Report',
                        message: 'Report deleted successfully',
                        type: 'success'
                      });
                    } catch (error) {
                      uiDialogService.dismiss({
                        id: 'ds-reject-sr'
                      });
                      uiNotificationService.show({
                        title: 'Delete Report',
                        message: 'Failed to delete report',
                        type: 'error'
                      });
                    }
                    break;
                  case 'cancel':
                    uiDialogService.dismiss({
                      id: 'ds-reject-sr'
                    });
                    break;
                }
              }
            }
          });
        };
      } else {
        thumbnailProps.canReject = false;
      }
    }
    array.push(thumbnailProps);
  });
  return [...thumbnailDisplaySets, ...thumbnailNoImageDisplaySets];
}
function _getComponentType(ds) {
  if (thumbnailNoImageModalities.includes(ds.Modality) || ds?.unsupported) {
    return 'thumbnailNoImage';
  }
  return 'thumbnailTracked';
}
function _findTabAndStudyOfDisplaySet(displaySetInstanceUID, tabs) {
  for (let t = 0; t < tabs.length; t++) {
    const {
      studies
    } = tabs[t];
    for (let s = 0; s < studies.length; s++) {
      const {
        displaySets
      } = studies[s];
      for (let d = 0; d < displaySets.length; d++) {
        const displaySet = displaySets[d];
        if (displaySet.displaySetInstanceUID === displaySetInstanceUID) {
          return {
            tabName: tabs[t].name,
            StudyInstanceUID: studies[s].studyInstanceUid
          };
        }
      }
    }
  }
}
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/getImageSrcFromImageId.js
/**
 * @param {*} cornerstone
 * @param {*} imageId
 */
function getImageSrcFromImageId(cornerstone, imageId) {
  return new Promise((resolve, reject) => {
    const canvas = document.createElement('canvas');
    cornerstone.utilities.loadImageToCanvas({
      canvas,
      imageId,
      thumbnail: true
    }).then(imageId => {
      resolve(canvas.toDataURL());
    }).catch(reject);
  });
}
/* harmony default export */ const PanelStudyBrowserTracking_getImageSrcFromImageId = (getImageSrcFromImageId);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/requestDisplaySetCreationForStudy.js
function requestDisplaySetCreationForStudy(dataSource, displaySetService, StudyInstanceUID, madeInClient) {
  if (displaySetService.activeDisplaySets.some(displaySet => displaySet.StudyInstanceUID === StudyInstanceUID)) {
    return;
  }
  dataSource.retrieve.series.metadata({
    StudyInstanceUID,
    madeInClient
  });
}
/* harmony default export */ const PanelStudyBrowserTracking_requestDisplaySetCreationForStudy = (requestDisplaySetCreationForStudy);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelStudyBrowserTracking/index.tsx


//



function _getStudyForPatientUtility(extensionManager) {
  const utilityModule = extensionManager.getModuleEntry('@ohif/extension-default.utilityModule.common');
  const {
    getStudiesForPatientByMRN
  } = utilityModule.exports;
  return getStudiesForPatientByMRN;
}

/**
 * Wraps the PanelStudyBrowser and provides features afforded by managers/services
 *
 * @param {object} params
 * @param {object} commandsManager
 * @param {object} extensionManager
 */
function WrappedPanelStudyBrowserTracking({
  commandsManager,
  extensionManager,
  servicesManager
}) {
  const dataSource = extensionManager.getActiveDataSource()[0];
  const getStudiesForPatientByMRN = _getStudyForPatientUtility(extensionManager);
  const _getStudiesForPatientByMRN = getStudiesForPatientByMRN.bind(null, dataSource);
  const _getImageSrcFromImageId = (0,react.useCallback)(_createGetImageSrcFromImageIdFn(extensionManager), []);
  const _requestDisplaySetCreationForStudy = PanelStudyBrowserTracking_requestDisplaySetCreationForStudy.bind(null, dataSource);
  return /*#__PURE__*/react.createElement(PanelStudyBrowserTracking_PanelStudyBrowserTracking, {
    servicesManager: servicesManager,
    commandsManager: commandsManager,
    dataSource: dataSource,
    getImageSrc: _getImageSrcFromImageId,
    getStudiesForPatientByMRN: _getStudiesForPatientByMRN,
    requestDisplaySetCreationForStudy: _requestDisplaySetCreationForStudy
  });
}

/**
 * Grabs cornerstone library reference using a dependent command from
 * the @ohif/extension-cornerstone extension. Then creates a helper function
 * that can take an imageId and return an image src.
 *
 * @param {func} getCommand - CommandManager's getCommand method
 * @returns {func} getImageSrcFromImageId - A utility function powered by
 * cornerstone
 */
function _createGetImageSrcFromImageIdFn(extensionManager) {
  const utilities = extensionManager.getModuleEntry('@ohif/extension-cornerstone.utilityModule.common');
  try {
    const {
      cornerstone
    } = utilities.exports.getCornerstoneLibraries();
    return PanelStudyBrowserTracking_getImageSrcFromImageId.bind(null, cornerstone);
  } catch (ex) {
    throw new Error('Required command not found');
  }
}
WrappedPanelStudyBrowserTracking.propTypes = {
  commandsManager: (prop_types_default()).object.isRequired,
  extensionManager: (prop_types_default()).object.isRequired,
  servicesManager: (prop_types_default()).object.isRequired
};
/* harmony default export */ const panels_PanelStudyBrowserTracking = (WrappedPanelStudyBrowserTracking);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/index.tsx + 105 modules
var cornerstone_src = __webpack_require__(11185);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/PanelMeasurementTableTracking.tsx








const {
  downloadCSVReport,
  formatDate: PanelMeasurementTableTracking_formatDate
} = src/* utils */.Wp;
const DISPLAY_STUDY_SUMMARY_INITIAL_VALUE = {
  key: undefined,
  //
  date: '',
  // '07-Sep-2010',
  modality: '',
  // 'CT',
  description: '' // 'CHEST/ABD/PELVIS W CONTRAST',
};
function PanelMeasurementTableTracking({
  servicesManager,
  extensionManager,
  commandsManager
}) {
  const [viewportGrid] = (0,ui_src/* useViewportGrid */.ih)();
  const {
    t
  } = (0,es/* useTranslation */.Bd)('MeasurementTable');
  const {
    measurementService,
    customizationService
  } = servicesManager.services;
  const [trackedMeasurements, sendTrackedMeasurementsEvent] = (0,getContextModule/* useTrackedMeasurements */.B)();
  const {
    trackedStudy,
    trackedSeries
  } = trackedMeasurements.context;
  const [displayStudySummary, setDisplayStudySummary] = (0,react.useState)(DISPLAY_STUDY_SUMMARY_INITIAL_VALUE);
  (0,react.useEffect)(() => {
    const updateDisplayStudySummary = async () => {
      if (trackedMeasurements.matches('tracking') && trackedStudy) {
        const studyMeta = src/* DicomMetadataStore */.H8.getStudy(trackedStudy);
        if (!studyMeta || !studyMeta.series || studyMeta.series.length === 0) {
          console.debug('Study metadata not available');
          return;
        }
        const instanceMeta = studyMeta.series[0].instances[0];
        const {
          StudyDate,
          StudyDescription
        } = instanceMeta;
        const modalities = new Set();
        studyMeta.series.forEach(series => {
          if (trackedSeries.includes(series.SeriesInstanceUID)) {
            modalities.add(series.instances[0].Modality);
          }
        });
        const modality = Array.from(modalities).join('/');
        setDisplayStudySummary(prevSummary => {
          if (prevSummary.key !== trackedStudy) {
            return {
              key: trackedStudy,
              date: StudyDate,
              modality,
              description: StudyDescription
            };
          }
          return prevSummary;
        });
      } else if (!trackedStudy) {
        setDisplayStudySummary(DISPLAY_STUDY_SUMMARY_INITIAL_VALUE);
      }
    };
    updateDisplayStudySummary();
  }, [trackedMeasurements, trackedStudy, trackedSeries]);
  const {
    disableEditing
  } = customizationService.getCustomization('PanelMeasurement.disableEditing', {
    id: 'default.disableEditing',
    disableEditing: false
  });
  return /*#__PURE__*/react.createElement(react.Fragment, null, displayStudySummary.key && /*#__PURE__*/react.createElement(ui_next_src/* StudySummary */.u3, {
    date: PanelMeasurementTableTracking_formatDate(displayStudySummary.date),
    description: displayStudySummary.description
  }), /*#__PURE__*/react.createElement(cornerstone_src.PanelMeasurement, {
    servicesManager: servicesManager,
    extensionManager: extensionManager,
    commandsManager: commandsManager,
    measurementFilter: measurement => trackedStudy === measurement.referenceStudyUID && trackedSeries.includes(measurement.referenceSeriesUID),
    customHeader: ({
      additionalFindings,
      measurements
    }) => {
      const disabled = additionalFindings.length === 0 && measurements.length === 0;
      if (disableEditing || disabled) {
        return null;
      }
      return /*#__PURE__*/react.createElement("div", {
        className: "bg-background flex h-9 w-full items-center rounded pr-0.5"
      }, /*#__PURE__*/react.createElement("div", {
        className: "flex space-x-1"
      }, /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
        size: "sm",
        variant: "ghost",
        className: "pl-1.5",
        onClick: () => {
          const measurements = measurementService.getMeasurements();
          const trackedMeasurements = measurements.filter(m => trackedStudy === m.referenceStudyUID && trackedSeries.includes(m.referenceSeriesUID));
          downloadCSVReport(trackedMeasurements);
        }
      }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Download, {
        className: "h-5 w-5"
      }), /*#__PURE__*/react.createElement("span", {
        className: "pl-1"
      }, "CSV")), /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
        size: "sm",
        variant: "ghost",
        className: "pl-0.5",
        onClick: () => {
          sendTrackedMeasurementsEvent('SAVE_REPORT', {
            viewportId: viewportGrid.activeViewportId,
            isBackupSave: true
          });
        }
      }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Add, null), "Create SR"), /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
        size: "sm",
        variant: "ghost",
        className: "pl-0.5",
        onClick: () => {
          measurementService.clearMeasurements();
        }
      }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Delete, null), "Delete All")));
    }
  }));
}
/* harmony default export */ const panels_PanelMeasurementTableTracking = (PanelMeasurementTableTracking);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/panels/index.js



// EXTERNAL MODULE: ../../../node_modules/i18next/dist/esm/i18next.js
var i18next = __webpack_require__(40680);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/getPanelModule.tsx
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }




// TODO:
// - No loading UI exists yet
// - cancel promises when component is destroyed
// - show errors in UI for thumbnails if promise fails

function getPanelModule({
  commandsManager,
  extensionManager,
  servicesManager
}) {
  return [{
    name: 'seriesList',
    iconName: 'tab-studies',
    iconLabel: 'Studies',
    label: i18next/* default */.A.t('SidePanel:Studies'),
    component: props => /*#__PURE__*/react.createElement(panels_PanelStudyBrowserTracking, _extends({}, props, {
      commandsManager: commandsManager,
      extensionManager: extensionManager,
      servicesManager: servicesManager
    }))
  }, {
    name: 'trackedMeasurements',
    iconName: 'tab-linear',
    iconLabel: 'Measure',
    label: i18next/* default */.A.t('SidePanel:Measurements'),
    component: props => /*#__PURE__*/react.createElement(panels_PanelMeasurementTableTracking, _extends({}, props, {
      commandsManager: commandsManager,
      extensionManager: extensionManager,
      servicesManager: servicesManager
    }))
  }];
}
/* harmony default export */ const src_getPanelModule = (getPanelModule);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/getViewportModule.tsx
function getViewportModule_extends() { return getViewportModule_extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, getViewportModule_extends.apply(null, arguments); }

const Component = /*#__PURE__*/react.lazy(() => {
  return __webpack_require__.e(/* import() */ 9862).then(__webpack_require__.bind(__webpack_require__, 49862));
});
const OHIFCornerstoneViewport = props => {
  return /*#__PURE__*/react.createElement(react.Suspense, {
    fallback: /*#__PURE__*/react.createElement("div", null, "Loading...")
  }, /*#__PURE__*/react.createElement(Component, props));
};
function getViewportModule({
  servicesManager,
  commandsManager,
  extensionManager
}) {
  const ExtendedOHIFCornerstoneTrackingViewport = props => {
    return /*#__PURE__*/react.createElement(OHIFCornerstoneViewport, getViewportModule_extends({
      servicesManager: servicesManager,
      commandsManager: commandsManager,
      extensionManager: extensionManager
    }, props));
  };
  return [{
    name: 'cornerstone-tracked',
    component: ExtendedOHIFCornerstoneTrackingViewport
  }];
}
/* harmony default export */ const src_getViewportModule = (getViewportModule);
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/package.json
const package_namespaceObject = /*#__PURE__*/JSON.parse('{"UU":"@ohif/extension-measurement-tracking"}');
;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/id.js

const id = package_namespaceObject.UU;

;// CONCATENATED MODULE: ../../../extensions/measurement-tracking/src/index.tsx




const measurementTrackingExtension = {
  /**
   * Only required property. Should be a unique value across all extensions.
   */
  id: id,
  getContextModule: getContextModule/* default */.A,
  getPanelModule: src_getPanelModule,
  getViewportModule: src_getViewportModule
};
/* harmony default export */ const measurement_tracking_src = (measurementTrackingExtension);

/***/ })

}]);