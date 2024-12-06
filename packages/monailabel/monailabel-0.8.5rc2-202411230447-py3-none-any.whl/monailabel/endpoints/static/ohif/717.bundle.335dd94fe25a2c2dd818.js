"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[717,2591,4182,1801],{

/***/ 14696:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ dynamicVolumeExtension)
});

// NAMESPACE OBJECT: ../../../extensions/cornerstone-dynamic-volume/src/actions/index.ts
var actions_namespaceObject = {};
__webpack_require__.r(actions_namespaceObject);
__webpack_require__.d(actions_namespaceObject, {
  updateSegmentationsChartDisplaySet: () => (updateSegmentationsChartDisplaySet)
});

;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/package.json
const package_namespaceObject = /*#__PURE__*/JSON.parse('{"UU":"@ohif/extension-cornerstone-dynamic-volume"}');
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/id.js

const id = package_namespaceObject.UU;
const SOPClassHandlerName = 'dynamic-volume';

// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var src = __webpack_require__(29463);
// EXTERNAL MODULE: ../../../node_modules/@cornerstonejs/core/dist/esm/index.js
var esm = __webpack_require__(81985);
// EXTERNAL MODULE: ../../../node_modules/@cornerstonejs/tools/dist/esm/index.js + 82 modules
var dist_esm = __webpack_require__(55139);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/actions/updateSegmentationsChartDisplaySet.ts



const CHART_MODALITY = 'CHT';
const SEG_CHART_INSTANCE_UID = src/* utils */.Wp.guid();

// Private SOPClassUid for chart data
const ChartDataSOPClassUid = '1.9.451.13215.7.3.2.7.6.1';
const {
  utilities: csToolsUtils
} = dist_esm;
function _getDateTimeStr() {
  const now = new Date();
  const date = now.getFullYear() + ('0' + now.getUTCMonth()).slice(-2) + ('0' + now.getUTCDate()).slice(-2);
  const time = ('0' + now.getUTCHours()).slice(-2) + ('0' + now.getUTCMinutes()).slice(-2) + ('0' + now.getUTCSeconds()).slice(-2);
  return {
    date,
    time
  };
}
function _getTimePointsDataByTagName(volume, timePointsTag) {
  const uniqueTimePoints = volume.imageIds.reduce((timePoints, imageId) => {
    const instance = src/* DicomMetadataStore */.H8.getInstanceByImageId(imageId);
    const timePointValue = instance[timePointsTag];
    if (timePointValue !== undefined) {
      timePoints.add(timePointValue);
    }
    return timePoints;
  }, new Set());
  return Array.from(uniqueTimePoints).sort((a, b) => a - b);
}
function _convertTimePointsUnit(timePoints, timePointsUnit) {
  const validUnits = ['ms', 's', 'm', 'h'];
  const divisors = [1000, 60, 60];
  const currentUnitIndex = validUnits.indexOf(timePointsUnit);
  let divisor = 1;
  if (currentUnitIndex !== -1) {
    for (let i = currentUnitIndex; i < validUnits.length - 1; i++) {
      const newDivisor = divisor * divisors[i];
      const greaterThanDivisorCount = timePoints.filter(timePoint => timePoint > newDivisor).length;

      // Change the scale only if more than 50% of the time points are
      // greater than the new divisor.
      if (greaterThanDivisorCount <= timePoints.length / 2) {
        break;
      }
      divisor = newDivisor;
      timePointsUnit = validUnits[i + 1];
    }
    if (divisor > 1) {
      timePoints = timePoints.map(timePoint => timePoint / divisor);
    }
  }
  return {
    timePoints,
    timePointsUnit
  };
}

// It currently supports only one tag but a few other will be added soon
// Supported 4D Tags
//   (0018,1060) Trigger Time                   [NOK]
//   (0018,0081) Echo Time                      [NOK]
//   (0018,0086) Echo Number                    [NOK]
//   (0020,0100) Temporal Position Identifier   [NOK]
//   (0054,1300) FrameReferenceTime             [OK]
function _getTimePointsData(volume) {
  const timePointsTags = {
    FrameReferenceTime: {
      unit: 'ms'
    }
  };
  const timePointsTagNames = Object.keys(timePointsTags);
  let timePoints;
  let timePointsUnit;
  for (let i = 0; i < timePointsTagNames.length; i++) {
    const tagName = timePointsTagNames[i];
    const curTimePoints = _getTimePointsDataByTagName(volume, tagName);
    if (curTimePoints.length) {
      timePoints = curTimePoints;
      timePointsUnit = timePointsTags[tagName].unit;
      break;
    }
  }
  if (!timePoints.length) {
    const concatTagNames = timePointsTagNames.join(', ');
    throw new Error(`Could not extract time points data for the following tags: ${concatTagNames}`);
  }
  const convertedTimePoints = _convertTimePointsUnit(timePoints, timePointsUnit);
  timePoints = convertedTimePoints.timePoints;
  timePointsUnit = convertedTimePoints.timePointsUnit;
  return {
    timePoints,
    timePointsUnit
  };
}
function _getSegmentationData(segmentation, volumesTimePointsCache, {
  servicesManager
}) {
  const {
    displaySetService,
    segmentationService,
    viewportGridService
  } = servicesManager.services;
  const displaySets = displaySetService.getActiveDisplaySets();
  const dynamic4DDisplaySet = displaySets.find(displaySet => {
    const anInstance = displaySet.instances?.[0];
    if (anInstance) {
      return anInstance.FrameReferenceTime !== undefined || anInstance.NumberOfTimeSlices !== undefined;
    }
    return false;
  });

  // const referencedDynamicVolume = cs.cache.getVolume(dynamic4DDisplaySet.displaySetInstanceUID);
  let volumeCacheKey;
  const volumeId = dynamic4DDisplaySet.displaySetInstanceUID;
  for (const [key] of esm.cache._volumeCache) {
    if (key.includes(volumeId)) {
      volumeCacheKey = key;
      break;
    }
  }
  let referencedDynamicVolume;
  if (volumeCacheKey) {
    referencedDynamicVolume = esm.cache.getVolume(volumeCacheKey);
  }
  const {
    StudyInstanceUID,
    StudyDescription
  } = src/* DicomMetadataStore */.H8.getInstanceByImageId(referencedDynamicVolume.imageIds[0]);
  const segmentationVolume = segmentationService.getLabelmapVolume(segmentation.segmentationId);
  const maskVolumeId = segmentationVolume?.volumeId;
  const [timeData, _] = csToolsUtils.dynamicVolume.getDataInTime(referencedDynamicVolume, {
    maskVolumeId
  });
  const pixelCount = timeData.length;
  if (pixelCount === 0) {
    return [];
  }

  // Todo: this is useless we should be able to grab color with just segRepUID and segmentIndex
  // const color = csTools.segmentation.config.color.getSegmentIndexColor(
  //   segmentationRepresentationUID,
  //   1 // segmentIndex
  // );
  const viewportId = viewportGridService.getActiveViewportId();
  const color = segmentationService.getSegmentColor(viewportId, segmentation.segmentationId, 1);
  const hexColor = esm.utilities.color.rgbToHex(color[0], color[1], color[2]);
  let timePointsData = volumesTimePointsCache.get(referencedDynamicVolume);
  if (!timePointsData) {
    timePointsData = _getTimePointsData(referencedDynamicVolume);
    volumesTimePointsCache.set(referencedDynamicVolume, timePointsData);
  }
  const {
    timePoints,
    timePointsUnit
  } = timePointsData;
  if (timePoints.length !== timeData[0].length) {
    throw new Error('Invalid number of time points returned');
  }
  const timepointsCount = timePoints.length;
  const chartSeriesData = new Array(timepointsCount);
  for (let i = 0; i < timepointsCount; i++) {
    const average = timeData.reduce((acc, cur) => acc + cur[i] / pixelCount, 0);
    chartSeriesData[i] = [timePoints[i], average];
  }
  return {
    StudyInstanceUID,
    StudyDescription,
    chartData: {
      series: {
        label: segmentation.label,
        points: chartSeriesData,
        color: hexColor
      },
      axis: {
        x: {
          label: `Time (${timePointsUnit})`
        },
        y: {
          label: `Vl (Bq/ml)`
        }
      }
    }
  };
}
function _getInstanceFromSegmentations(segmentations, {
  servicesManager
}) {
  if (!segmentations.length) {
    return;
  }
  const volumesTimePointsCache = new WeakMap();
  const segmentationsData = segmentations.map(segmentation => _getSegmentationData(segmentation, volumesTimePointsCache, {
    servicesManager
  }));
  const {
    date: seriesDate,
    time: seriesTime
  } = _getDateTimeStr();
  const series = segmentationsData.reduce((allSeries, curSegData) => {
    return [...allSeries, curSegData.chartData.series];
  }, []);
  const instance = {
    SOPClassUID: ChartDataSOPClassUid,
    Modality: CHART_MODALITY,
    SOPInstanceUID: src/* utils */.Wp.guid(),
    SeriesDate: seriesDate,
    SeriesTime: seriesTime,
    SeriesInstanceUID: SEG_CHART_INSTANCE_UID,
    StudyInstanceUID: segmentationsData[0].StudyInstanceUID,
    StudyDescription: segmentationsData[0].StudyDescription,
    SeriesNumber: 100,
    SeriesDescription: 'Segmentation chart series data',
    chartData: {
      series,
      axis: {
        ...segmentationsData[0].chartData.axis
      }
    }
  };
  const seriesMetadata = {
    StudyInstanceUID: instance.StudyInstanceUID,
    StudyDescription: instance.StudyDescription,
    SeriesInstanceUID: instance.SeriesInstanceUID,
    SeriesDescription: instance.SeriesDescription,
    SeriesNumber: instance.SeriesNumber,
    SeriesTime: instance.SeriesTime,
    SOPClassUID: instance.SOPClassUID,
    Modality: instance.Modality
  };
  return {
    seriesMetadata,
    instance
  };
}
function updateSegmentationsChartDisplaySet({
  servicesManager
}) {
  debugger;
  const {
    segmentationService
  } = servicesManager.services;
  const segmentations = segmentationService.getSegmentations();
  const {
    seriesMetadata,
    instance
  } = _getInstanceFromSegmentations(segmentations, {
    servicesManager
  }) ?? {};
  if (seriesMetadata && instance) {
    // An event is triggered after adding the instance and the displaySet is created
    src/* DicomMetadataStore */.H8.addSeriesMetadata([seriesMetadata], true);
    src/* DicomMetadataStore */.H8.addInstances([instance], true);
  }
}

;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/actions/index.ts


;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/commandsModule.ts



const LABELMAP = dist_esm.Enums.SegmentationRepresentations.Labelmap;
const commandsModule = ({
  commandsManager,
  servicesManager
}) => {
  const services = servicesManager.services;
  const {
    displaySetService,
    viewportGridService,
    segmentationService
  } = services;
  const actions = {
    ...actions_namespaceObject,
    getDynamic4DDisplaySet: () => {
      const displaySets = displaySetService.getActiveDisplaySets();
      const dynamic4DDisplaySet = displaySets.find(displaySet => {
        const anInstance = displaySet.instances?.[0];
        if (anInstance) {
          return anInstance.FrameReferenceTime !== undefined || anInstance.NumberOfTimeSlices !== undefined || anInstance.TemporalPositionIdentifier !== undefined;
        }
        return false;
      });
      return dynamic4DDisplaySet;
    },
    getComputedDisplaySets: () => {
      const displaySetCache = displaySetService.getDisplaySetCache();
      const cachedDisplaySets = [...displaySetCache.values()];
      const computedDisplaySets = cachedDisplaySets.filter(displaySet => {
        return displaySet.isDerived;
      });
      return computedDisplaySets;
    },
    exportTimeReportCSV: ({
      segmentations,
      config,
      options,
      summaryStats
    }) => {
      const dynamic4DDisplaySet = actions.getDynamic4DDisplaySet();
      const volumeId = dynamic4DDisplaySet?.displaySetInstanceUID;

      // cache._volumeCache is a map that has a key that includes the volumeId
      // it is not exactly the volumeId, but it is the key that includes the volumeId
      // so we can't do cache._volumeCache.get(volumeId) we should iterate
      // over the keys and find the one that includes the volumeId
      let volumeCacheKey;
      for (const [key] of esm.cache._volumeCache) {
        if (key.includes(volumeId)) {
          volumeCacheKey = key;
          break;
        }
      }
      let dynamicVolume;
      if (volumeCacheKey) {
        dynamicVolume = esm.cache.getVolume(volumeCacheKey);
      }
      const instance = dynamic4DDisplaySet.instances[0];
      const csv = [];

      // CSV header information with placeholder empty values for the metadata lines
      csv.push(`Patient ID,${instance.PatientID},`);
      csv.push(`Study Date,${instance.StudyDate},`);
      csv.push(`StudyInstanceUID,${instance.StudyInstanceUID},`);
      csv.push(`StudyDescription,${instance.StudyDescription},`);
      csv.push(`SeriesInstanceUID,${instance.SeriesInstanceUID},`);

      // empty line
      csv.push('');
      csv.push('');

      // Helper function to calculate standard deviation
      function calculateStandardDeviation(data) {
        const n = data.length;
        const mean = data.reduce((acc, value) => acc + value, 0) / n;
        const squaredDifferences = data.map(value => (value - mean) ** 2);
        const variance = squaredDifferences.reduce((acc, value) => acc + value, 0) / n;
        const stdDeviation = Math.sqrt(variance);
        return stdDeviation;
      }
      // Iterate through each segmentation to get the timeData and ijkCoords
      segmentations.forEach(segmentation => {
        const volume = segmentationService.getLabelmapVolume(segmentation.segmentationId);
        const [timeData, ijkCoords] = dist_esm.utilities.dynamicVolume.getDataInTime(dynamicVolume, {
          maskVolumeId: volume.volumeId
        });
        if (summaryStats) {
          // Adding column headers for pixel identifier and segmentation label ids
          let headers = 'Operation,Segmentation Label ID';
          const maxLength = dynamicVolume.numTimePoints;
          for (let t = 0; t < maxLength; t++) {
            headers += `,Time Point ${t}`;
          }
          csv.push(headers);
          // // perform summary statistics on the timeData including for each time point, mean, median, min, max, and standard deviation for
          // // all the voxels in the ROI
          const mean = [];
          const min = [];
          const minIJK = [];
          const max = [];
          const maxIJK = [];
          const std = [];
          const numVoxels = timeData.length;
          // Helper function to calculate standard deviation
          for (let timeIndex = 0; timeIndex < maxLength; timeIndex++) {
            // for each voxel in the ROI, get the value at the current time point
            const voxelValues = [];
            let sum = 0;
            let minValue = Infinity;
            let maxValue = -Infinity;
            let minIndex = 0;
            let maxIndex = 0;

            // Single pass through the data to collect all needed values
            for (let voxelIndex = 0; voxelIndex < numVoxels; voxelIndex++) {
              const value = timeData[voxelIndex][timeIndex];
              voxelValues.push(value);
              sum += value;
              if (value < minValue) {
                minValue = value;
                minIndex = voxelIndex;
              }
              if (value > maxValue) {
                maxValue = value;
                maxIndex = voxelIndex;
              }
            }
            mean.push(sum / numVoxels);
            min.push(minValue);
            minIJK.push(ijkCoords[minIndex]);
            max.push(maxValue);
            maxIJK.push(ijkCoords[maxIndex]);
            std.push(calculateStandardDeviation(voxelValues));
          }
          let row = `Mean,${segmentation.label}`;
          // Generate separate rows for each statistic
          for (let t = 0; t < maxLength; t++) {
            row += `,${mean[t]}`;
          }
          csv.push(row);
          row = `Standard Deviation,${segmentation.label}`;
          for (let t = 0; t < maxLength; t++) {
            row += `,${std[t]}`;
          }
          csv.push(row);
          row = `Min,${segmentation.label}`;
          for (let t = 0; t < maxLength; t++) {
            row += `,${min[t]}`;
          }
          csv.push(row);
          row = `Max,${segmentation.label}`;
          for (let t = 0; t < maxLength; t++) {
            row += `,${max[t]}`;
          }
          csv.push(row);
        } else {
          // Adding column headers for pixel identifier and segmentation label ids
          let headers = 'Pixel Identifier (IJK),Segmentation Label ID';
          const maxLength = dynamicVolume.numTimePoints;
          for (let t = 0; t < maxLength; t++) {
            headers += `,Time Point ${t}`;
          }
          csv.push(headers);
          // Assuming timeData and ijkCoords are of the same length
          for (let i = 0; i < timeData.length; i++) {
            // Generate the pixel identifier
            const pixelIdentifier = `${ijkCoords[i][0]}_${ijkCoords[i][1]}_${ijkCoords[i][2]}`;

            // Start a new row for the current pixel
            let row = `${pixelIdentifier},${segmentation.label}`;

            // Add time data points for this pixel
            for (let t = 0; t < timeData[i].length; t++) {
              row += `,${timeData[i][t]}`;
            }

            // Append the row to the CSV array
            csv.push(row);
          }
        }
      });

      // Convert to CSV string
      const csvContent = csv.join('\n');

      // Generate filename and trigger download
      const filename = `${instance.PatientID}.csv`;
      const blob = new Blob([csvContent], {
        type: 'text/csv;charset=utf-8;'
      });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    swapDynamicWithComputedDisplaySet: ({
      displaySet
    }) => {
      const computedDisplaySet = displaySet;
      const displaySetCache = displaySetService.getDisplaySetCache();
      const cachedDisplaySetKeys = [displaySetCache.keys()];
      const {
        displaySetInstanceUID
      } = computedDisplaySet;
      // Check to see if computed display set is already in cache
      if (!cachedDisplaySetKeys.includes(displaySetInstanceUID)) {
        displaySetCache.set(displaySetInstanceUID, computedDisplaySet);
      }

      // Get all viewports and their corresponding indices
      const {
        viewports
      } = viewportGridService.getState();

      // get the viewports in the grid
      // iterate over them and find the ones that are showing a dynamic
      // volume (displaySet), and replace that exact displaySet with the
      // computed displaySet

      const dynamic4DDisplaySet = actions.getDynamic4DDisplaySet();
      const viewportsToUpdate = [];
      for (const [key, value] of viewports) {
        const viewport = value;
        const viewportOptions = viewport.viewportOptions;
        const {
          displaySetInstanceUIDs
        } = viewport;
        const displaySetInstanceUIDIndex = displaySetInstanceUIDs.indexOf(dynamic4DDisplaySet.displaySetInstanceUID);
        if (displaySetInstanceUIDIndex !== -1) {
          const newViewport = {
            viewportId: viewport.viewportId,
            // merge the other displaySetInstanceUIDs with the new one
            displaySetInstanceUIDs: [...displaySetInstanceUIDs.slice(0, displaySetInstanceUIDIndex), displaySetInstanceUID, ...displaySetInstanceUIDs.slice(displaySetInstanceUIDIndex + 1)],
            viewportOptions: {
              initialImageOptions: viewportOptions.initialImageOptions,
              viewportType: 'volume',
              orientation: viewportOptions.orientation,
              background: viewportOptions.background
            }
          };
          viewportsToUpdate.push(newViewport);
        }
      }
      viewportGridService.setDisplaySetsForViewports(viewportsToUpdate);
    },
    swapComputedWithDynamicDisplaySet: () => {
      // Todo: this assumes there is only one dynamic display set in the viewer
      const dynamicDisplaySet = actions.getDynamic4DDisplaySet();
      const displaySetCache = displaySetService.getDisplaySetCache();
      const cachedDisplaySetKeys = [...displaySetCache.keys()]; // Fix: Spread to get the array
      const {
        displaySetInstanceUID
      } = dynamicDisplaySet;

      // Check to see if dynamic display set is already in cache
      if (!cachedDisplaySetKeys.includes(displaySetInstanceUID)) {
        displaySetCache.set(displaySetInstanceUID, dynamicDisplaySet);
      }

      // Get all viewports and their corresponding indices
      const {
        viewports
      } = viewportGridService.getState();

      // Get the computed 4D display set
      const computed4DDisplaySet = actions.getComputedDisplaySets()[0];
      const viewportsToUpdate = [];
      for (const [key, value] of viewports) {
        const viewport = value;
        const viewportOptions = viewport.viewportOptions;
        const {
          displaySetInstanceUIDs
        } = viewport;
        const displaySetInstanceUIDIndex = displaySetInstanceUIDs.indexOf(computed4DDisplaySet.displaySetInstanceUID);
        if (displaySetInstanceUIDIndex !== -1) {
          const newViewport = {
            viewportId: viewport.viewportId,
            // merge the other displaySetInstanceUIDs with the new one
            displaySetInstanceUIDs: [...displaySetInstanceUIDs.slice(0, displaySetInstanceUIDIndex), displaySetInstanceUID, ...displaySetInstanceUIDs.slice(displaySetInstanceUIDIndex + 1)],
            viewportOptions: {
              initialImageOptions: viewportOptions.initialImageOptions,
              viewportType: 'volume',
              orientation: viewportOptions.orientation,
              background: viewportOptions.background
            }
          };
          viewportsToUpdate.push(newViewport);
        }
      }
      viewportGridService.setDisplaySetsForViewports(viewportsToUpdate);
    },
    createNewLabelMapForDynamicVolume: async ({
      label
    }) => {
      const {
        viewports,
        activeViewportId
      } = viewportGridService.getState();

      // get the dynamic 4D display set
      const dynamic4DDisplaySet = actions.getDynamic4DDisplaySet();
      const dynamic4DDisplaySetInstanceUID = dynamic4DDisplaySet.displaySetInstanceUID;

      // check if the dynamic 4D display set is in the display, if not we might have
      // the computed volumes and we should choose them for the segmentation
      // creation

      let referenceDisplaySet;
      const activeViewport = viewports.get(activeViewportId);
      const activeDisplaySetInstanceUIDs = activeViewport.displaySetInstanceUIDs;
      const dynamicIsInActiveViewport = activeDisplaySetInstanceUIDs.includes(dynamic4DDisplaySetInstanceUID);
      if (dynamicIsInActiveViewport) {
        referenceDisplaySet = dynamic4DDisplaySet;
      }
      if (!referenceDisplaySet) {
        // try to see if there is any derived displaySet in the active viewport
        // which is referencing the dynamic 4D display set

        // Todo: this is wrong but I don't have time to fix it now
        const cachedDisplaySets = displaySetService.getDisplaySetCache();
        for (const [key, displaySet] of cachedDisplaySets) {
          if (displaySet.referenceDisplaySetUID === dynamic4DDisplaySetInstanceUID) {
            referenceDisplaySet = displaySet;
            break;
          }
        }
      }
      if (!referenceDisplaySet) {
        throw new Error('No reference display set found based on the dynamic data');
      }
      const displaySet = displaySetService.getDisplaySetByUID(referenceDisplaySet.displaySetInstanceUID);
      const segmentationId = await segmentationService.createLabelmapForDisplaySet(displaySet, {
        label
      });
      const firstViewport = viewports.values().next().value;
      await segmentationService.addSegmentationRepresentation(firstViewport.viewportId, {
        segmentationId
      });
      return segmentationId;
    }
  };
  const definitions = {
    updateSegmentationsChartDisplaySet: {
      commandFn: actions.updateSegmentationsChartDisplaySet,
      storeContexts: [],
      options: {}
    },
    exportTimeReportCSV: {
      commandFn: actions.exportTimeReportCSV,
      storeContexts: [],
      options: {}
    },
    swapDynamicWithComputedDisplaySet: {
      commandFn: actions.swapDynamicWithComputedDisplaySet,
      storeContexts: [],
      options: {}
    },
    createNewLabelMapForDynamicVolume: {
      commandFn: actions.createNewLabelMapForDynamicVolume,
      storeContexts: [],
      options: {}
    },
    swapComputedWithDynamicDisplaySet: {
      commandFn: actions.swapComputedWithDynamicDisplaySet,
      storeContexts: [],
      options: {}
    }
  };
  return {
    actions,
    definitions,
    defaultContext: 'DYNAMIC-VOLUME:CORNERSTONE'
  };
};
/* harmony default export */ const src_commandsModule = (commandsModule);
// EXTERNAL MODULE: ../../../node_modules/react/index.js
var react = __webpack_require__(86326);
// EXTERNAL MODULE: ../../ui/src/index.js + 690 modules
var ui_src = __webpack_require__(35647);
// EXTERNAL MODULE: ../../ui-next/src/index.ts + 2483 modules
var ui_next_src = __webpack_require__(35570);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/panels/DynamicVolumeControls.tsx
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }




const controlClassNames = {
  sizeClassName: 'w-[58px] h-[28px]',
  arrowsDirection: 'horizontal',
  labelPosition: 'bottom'
};
const Header = ({
  title,
  tooltip
}) => /*#__PURE__*/react.createElement("div", {
  className: "flex items-center space-x-1"
}, /*#__PURE__*/react.createElement(ui_src/* Tooltip */.m_, {
  content: /*#__PURE__*/react.createElement("div", {
    className: "text-white"
  }, tooltip),
  position: "bottom-left",
  tight: true,
  tooltipBoxClassName: "max-w-xs p-2"
}, /*#__PURE__*/react.createElement(ui_src/* Icon */.In, {
  name: "info-link",
  className: "text-primary-active h-[14px] w-[14px]"
})), /*#__PURE__*/react.createElement("span", {
  className: "text-aqua-pale text-[11px] uppercase"
}, title));
const DynamicVolumeControls = ({
  isPlaying,
  onPlayPauseChange,
  // fps
  fps,
  onFpsChange,
  minFps,
  maxFps,
  // Frames
  currentFrameIndex,
  onFrameChange,
  framesLength,
  onGenerate,
  onDoubleRangeChange,
  onDynamicClick
}) => {
  const [computedView, setComputedView] = (0,react.useState)(false);
  const [computeViewMode, setComputeViewMode] = (0,react.useState)(esm.Enums.DynamicOperatorType.SUM);
  const [sliderRangeValues, setSliderRangeValues] = (0,react.useState)([0, framesLength - 1]);
  const handleSliderChange = newValues => {
    onDoubleRangeChange(newValues);
    setSliderRangeValues(newValues);
  };
  const formatLabel = value => Math.round(value);
  return /*#__PURE__*/react.createElement("div", {
    className: "flex select-none flex-col"
  }, /*#__PURE__*/react.createElement(ui_src/* PanelSection */.aU, {
    title: "Controls",
    childrenClassName: "space-y-4 pb-5 px-5"
  }, /*#__PURE__*/react.createElement("div", {
    className: "mt-2"
  }, /*#__PURE__*/react.createElement(Header, {
    title: "View",
    tooltip: 'Select the view mode, 4D to view the dynamic volume or Computed to view the computed volume'
  }), /*#__PURE__*/react.createElement(ui_src/* ButtonGroup */.e2, {
    className: "mt-2 w-full"
  }, /*#__PURE__*/react.createElement("button", {
    className: "w-1/2",
    onClick: () => {
      setComputedView(false);
      onDynamicClick?.();
    }
  }, "4D"), /*#__PURE__*/react.createElement("button", {
    className: "w-1/2",
    onClick: () => {
      setComputedView(true);
    }
  }, "Computed"))), /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement(FrameControls, {
    onPlayPauseChange: onPlayPauseChange,
    isPlaying: isPlaying,
    computedView: computedView
    // fps
    ,
    fps: fps,
    onFpsChange: onFpsChange,
    minFps: minFps,
    maxFps: maxFps
    //
    ,
    framesLength: framesLength,
    onFrameChange: onFrameChange,
    currentFrameIndex: currentFrameIndex
  })), /*#__PURE__*/react.createElement("div", {
    className: `mt-6 flex flex-col ${computedView ? '' : 'ohif-disabled'}`
  }, /*#__PURE__*/react.createElement(Header, {
    title: "Computed Operation",
    tooltip: /*#__PURE__*/react.createElement("div", null, "Operation Buttons (SUM, AVERAGE, SUBTRACT): Select the mathematical operation to be applied to the data set.", /*#__PURE__*/react.createElement("br", null), " Range Slider: Choose the numeric range within which the operation will be performed.", /*#__PURE__*/react.createElement("br", null), "Generate Button: Execute the chosen operation on the specified range of data.", ' ')
  }), /*#__PURE__*/react.createElement(ui_src/* ButtonGroup */.e2, {
    className: `mt-2 w-full`,
    separated: true
  }, /*#__PURE__*/react.createElement("button", {
    className: "w-1/2",
    onClick: () => setComputeViewMode(esm.Enums.DynamicOperatorType.SUM)
  }, esm.Enums.DynamicOperatorType.SUM.toString().toUpperCase()), /*#__PURE__*/react.createElement("button", {
    className: "w-1/2",
    onClick: () => setComputeViewMode(esm.Enums.DynamicOperatorType.AVERAGE)
  }, esm.Enums.DynamicOperatorType.AVERAGE.toString().toUpperCase()), /*#__PURE__*/react.createElement("button", {
    className: "w-1/2",
    onClick: () => setComputeViewMode(esm.Enums.DynamicOperatorType.SUBTRACT)
  }, esm.Enums.DynamicOperatorType.SUBTRACT.toString().toUpperCase())), /*#__PURE__*/react.createElement("div", {
    className: "mt-2 w-full"
  }, /*#__PURE__*/react.createElement(ui_next_src/* DoubleSlider */.Jg, {
    min: 0,
    max: framesLength - 1,
    step: 1,
    defaultValue: sliderRangeValues,
    onValueChange: handleSliderChange,
    formatLabel: formatLabel,
    className: "w-full"
  })), /*#__PURE__*/react.createElement(ui_src/* Button */.$n, {
    className: "mt-2 !h-[26px] !w-[115px] self-start !p-0",
    onClick: () => {
      onGenerate(computeViewMode);
    }
  }, "Generate"))));
};
/* harmony default export */ const panels_DynamicVolumeControls = (DynamicVolumeControls);
function FrameControls({
  isPlaying,
  onPlayPauseChange,
  fps,
  minFps,
  maxFps,
  onFpsChange,
  framesLength,
  onFrameChange,
  currentFrameIndex,
  computedView
}) {
  const getPlayPauseIconName = () => isPlaying ? 'icon-pause' : 'icon-play';
  return /*#__PURE__*/react.createElement("div", {
    className: computedView && 'ohif-disabled'
  }, /*#__PURE__*/react.createElement(Header, {
    title: "4D Controls",
    tooltip: /*#__PURE__*/react.createElement("div", null, "Play/Pause Button: Begin or pause the animation of the 4D visualization. ", /*#__PURE__*/react.createElement("br", null), " Frame Selector: Navigate through individual frames of the 4D data. ", /*#__PURE__*/react.createElement("br", null), " FPS (Frames Per Second) Selector: Adjust the playback speed of the animation.")
  }), /*#__PURE__*/react.createElement("div", {
    className: "mt-3 flex justify-between"
  }, /*#__PURE__*/react.createElement(ui_src/* IconButton */.K0, {
    className: "bg-customblue-30 h-[26px] w-[58px] rounded-[4px]",
    onClick: () => onPlayPauseChange(!isPlaying)
  }, /*#__PURE__*/react.createElement(ui_src/* Icon */.In, {
    name: getPlayPauseIconName(),
    className: "active:text-primary-light hover:bg-customblue-300 h-[24px] w-[24px] cursor-pointer text-white"
  })), /*#__PURE__*/react.createElement(ui_src/* InputNumber */.YI, _extends({
    value: currentFrameIndex,
    onChange: onFrameChange,
    minValue: 0,
    maxValue: framesLength - 1,
    label: "Frame"
  }, controlClassNames)), /*#__PURE__*/react.createElement(ui_src/* InputNumber */.YI, _extends({
    value: fps,
    onChange: onFpsChange,
    minValue: minFps,
    maxValue: maxFps
  }, controlClassNames, {
    label: "FPS"
  }))));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/panels/PanelGenerateImage.tsx





const SOPClassHandlerId = '@ohif/extension-default.sopClassHandlerModule.stack';
function PanelGenerateImage({
  servicesManager,
  commandsManager
}) {
  const {
    cornerstoneViewportService,
    viewportGridService,
    displaySetService
  } = servicesManager.services;
  const [{
    isCineEnabled
  }, cineService] = (0,ui_src/* useCine */.tq)();
  const [{
    activeViewportId
  }] = (0,ui_src/* useViewportGrid */.ih)();

  //
  const [timePointsRange, setTimePointsRange] = (0,react.useState)([0, 0]);
  const [timePointsRangeToUseForGenerate, setTimePointsRangeToUseForGenerate] = (0,react.useState)([0, 0]);
  const [computedDisplaySet, setComputedDisplaySet] = (0,react.useState)(null);
  const [dynamicVolume, setDynamicVolume] = (0,react.useState)(null);
  const [frameRate, setFrameRate] = (0,react.useState)(20);
  const [isPlaying, setIsPlaying] = (0,react.useState)(isCineEnabled);
  const [timePointRendered, setTimePointRendered] = (0,react.useState)(null);
  const [displayingComputed, setDisplayingComputed] = (0,react.useState)(false);

  //
  const uuidComputedVolume = (0,react.useRef)(esm.utilities.uuidv4());
  const uuidDynamicVolume = (0,react.useRef)(null);
  const computedVolumeId = `cornerstoneStreamingImageVolume:${uuidComputedVolume.current}`;
  (0,react.useEffect)(() => {
    const viewportDataChangedEvt = cornerstoneViewportService.EVENTS.VIEWPORT_DATA_CHANGED;
    const cineStateChangedEvt = servicesManager.services.cineService.EVENTS.CINE_STATE_CHANGED;
    const viewportDataChangedCallback = evtDetails => {
      evtDetails.viewportData.data.forEach(volumeData => {
        if (volumeData.volume?.isDynamicVolume()) {
          setDynamicVolume(volumeData.volume);
          uuidDynamicVolume.current = volumeData.displaySetInstanceUID;
          const newRange = [1, volumeData.volume.numTimePoints];
          setTimePointsRange(newRange);
          setTimePointsRangeToUseForGenerate(newRange);
        }
      });
    };
    const cineStateChangedCallback = evt => {
      setIsPlaying(evt.isPlaying);
    };
    const {
      unsubscribe: unsubscribeViewportData
    } = cornerstoneViewportService.subscribe(viewportDataChangedEvt, viewportDataChangedCallback);
    const {
      unsubscribe: unsubscribeCineState
    } = servicesManager.services.cineService.subscribe(cineStateChangedEvt, cineStateChangedCallback);
    return () => {
      unsubscribeViewportData();
      unsubscribeCineState();
    };
  }, [cornerstoneViewportService, cineService, servicesManager.services.cineService]);
  (0,react.useEffect)(() => {
    const evt = esm.Enums.Events.DYNAMIC_VOLUME_TIME_POINT_INDEX_CHANGED;
    const callback = evt => {
      setTimePointRendered(evt.detail.timePointIndex);
    };
    esm.eventTarget.addEventListener(evt, callback);
    return () => {
      esm.eventTarget.removeEventListener(evt, callback);
    };
  }, [cornerstoneViewportService]);
  (0,react.useEffect)(() => {
    const displaySetUIDs = viewportGridService.getDisplaySetsUIDsForViewport(activeViewportId);
    if (!displaySetUIDs?.length) {
      return;
    }
    const displaySets = displaySetUIDs.map(displaySetService.getDisplaySetByUID);
    const dynamicVolumeDisplaySet = displaySets.find(displaySet => displaySet.isDynamicVolume);
    if (!dynamicVolumeDisplaySet) {
      return;
    }
    const dynamicVolume = esm.cache.getVolumes().find(volume => volume.volumeId.includes(dynamicVolumeDisplaySet.displaySetInstanceUID));
    if (!dynamicVolume) {
      return;
    }
    setDynamicVolume(dynamicVolume);
    uuidDynamicVolume.current = dynamicVolumeDisplaySet.displaySetInstanceUID;
    const newRange = [1, dynamicVolume.numTimePoints];
    setTimePointsRange(newRange);
    setTimePointsRangeToUseForGenerate(newRange);
  }, [activeViewportId, viewportGridService, displaySetService, cornerstoneViewportService, cineService]);
  function renderGeneratedImage(displaySet) {
    commandsManager.runCommand('swapDynamicWithComputedDisplaySet', {
      displaySet
    });
    setDisplayingComputed(true);
  }
  function renderDynamicImage(displaySet) {
    commandsManager.runCommand('swapComputedWithDynamicDisplaySet');
  }

  // Get computed volume from cache, calculate the data across the time frames,
  // set the scalar data to the computedVolume, and create displaySet
  async function onGenerateImage(operationName) {
    const dynamicVolumeId = dynamicVolume.volumeId;
    if (!dynamicVolumeId) {
      return;
    }
    let computedVolume = esm.cache.getVolume(computedVolumeId);
    if (!computedVolume) {
      computedVolume = await esm.volumeLoader.createAndCacheDerivedVolume(dynamicVolumeId, {
        volumeId: computedVolumeId
      });
    }
    const [start, end] = timePointsRangeToUseForGenerate;
    const frameNumbers = Array.from({
      length: end - start + 1
    }, (_, i) => i + start - 1);
    const options = {
      frameNumbers: operationName === 'SUBTRACT' ? [start, end - 1] : frameNumbers,
      targetVolume: computedVolume
    };
    dist_esm.utilities.dynamicVolume.updateVolumeFromTimeData(dynamicVolume, operationName, options);

    // If computed display set does not exist, create an object to be used as
    // the displaySet. If it does exist, update the image data and vtkTexture
    if (!computedDisplaySet) {
      const displaySet = {
        volumeLoaderSchema: computedVolume.volumeId.split(':')[0],
        displaySetInstanceUID: uuidComputedVolume.current,
        SOPClassHandlerId: SOPClassHandlerId,
        Modality: dynamicVolume.metadata.Modality,
        isMultiFrame: false,
        numImageFrames: 1,
        uid: uuidComputedVolume.current,
        referenceDisplaySetUID: dynamicVolume.volumeId.split(':')[1],
        madeInClient: true,
        FrameOfReferenceUID: dynamicVolume.metadata.FrameOfReferenceUID,
        isDerived: true,
        imageIds: computedVolume.imageIds
      };
      setComputedDisplaySet(displaySet);
      renderGeneratedImage(displaySet);
    } else {
      commandsManager.runCommand('updateVolumeData', {
        volume: computedVolume
      });
      cornerstoneViewportService.getRenderingEngine().render();
      renderGeneratedImage(computedDisplaySet);
    }
  }
  const onPlayPauseChange = isPlaying => {
    isPlaying ? handlePlay() : handleStop();
  };
  const handlePlay = () => {
    setIsPlaying(true);
    const viewportInfo = cornerstoneViewportService.getViewportInfo(activeViewportId);
    if (!viewportInfo) {
      return;
    }
    const {
      element
    } = viewportInfo;
    cineService.playClip(element, {
      framesPerSecond: frameRate,
      viewportId: activeViewportId
    });
  };
  const handleStop = () => {
    setIsPlaying(false);
    const {
      element
    } = cornerstoneViewportService.getViewportInfo(activeViewportId);
    cineService.stopClip(element);
  };
  const handleSetFrameRate = newFrameRate => {
    setFrameRate(newFrameRate);
    handleStop();
    handlePlay();
  };
  function handleSliderChange(newValues) {
    if (newValues[0] === timePointsRangeToUseForGenerate[0] && newValues[1] === timePointsRangeToUseForGenerate[1]) {
      return;
    }
    setTimePointsRangeToUseForGenerate(newValues);
  }
  if (!dynamicVolume || timePointsRange.length === 0) {
    return null;
  }
  return /*#__PURE__*/react.createElement(panels_DynamicVolumeControls, {
    fps: frameRate,
    isPlaying: isPlaying,
    onPlayPauseChange: onPlayPauseChange,
    minFps: 1,
    maxFps: 50,
    currentFrameIndex: timePointRendered,
    onFpsChange: handleSetFrameRate,
    framesLength: timePointsRange[1],
    onFrameChange: timePointIndex => {
      dynamicVolume.timePointIndex = timePointIndex;
    },
    onGenerate: onGenerateImage,
    onDynamicClick: displayingComputed ? () => renderDynamicImage(computedDisplaySet) : null,
    onDoubleRangeChange: handleSliderChange,
    initialRangeValues: timePointsRangeToUseForGenerate
  });
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/panels/DynamicDataPanel.tsx


function DynamicDataPanel({
  servicesManager,
  commandsManager,
  tab
}) {
  return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement("div", {
    className: "flex flex-col text-white",
    "data-cy": 'dynamic-volume-panel'
  }, /*#__PURE__*/react.createElement(PanelGenerateImage, {
    commandsManager: commandsManager,
    servicesManager: servicesManager
  })));
}
/* harmony default export */ const panels_DynamicDataPanel = (DynamicDataPanel);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/panels/WorkflowPanel.tsx

function WorkflowPanel({
  servicesManager
}) {
  const ProgressDropdownWithService = servicesManager.services.customizationService.getCustomization('progressDropdownWithServiceComponent').component;
  return /*#__PURE__*/React.createElement("div", {
    "data-cy": 'workflow-panel',
    className: "bg-secondary-dark mb-1 px-3 py-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "mb-1"
  }, "Workflow"), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(ProgressDropdownWithService, {
    servicesManager: servicesManager
  })));
}
/* harmony default export */ const panels_WorkflowPanel = ((/* unused pure expression or super */ null && (WorkflowPanel)));
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/panels/index.js




// EXTERNAL MODULE: ../../../extensions/cornerstone/src/index.tsx + 105 modules
var cornerstone_src = __webpack_require__(11185);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/panels/DynamicExport.tsx



function DynamicExport({
  commandsManager,
  servicesManager
}) {
  const segmentations = (0,cornerstone_src.useSegmentations)({
    servicesManager
  });
  if (!segmentations?.length) {
    return null;
  }
  return /*#__PURE__*/react.createElement("div", {
    className: "flex gap-2"
  }, /*#__PURE__*/react.createElement("div", {
    className: "flex h-8 w-full items-center rounded pr-0.5"
  }, /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    size: "sm",
    variant: "ghost",
    className: "pl-1.5",
    onClick: () => {
      commandsManager.runCommand('exportTimeReportCSV', {
        segmentations,
        options: {
          filename: 'TimeData.csv'
        }
      });
    }
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Export, null), /*#__PURE__*/react.createElement("span", {
    className: "pl-1"
  }, "Time Data"))), /*#__PURE__*/react.createElement("div", {
    className: "flex h-8 w-full items-center rounded pr-0.5"
  }, /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    size: "sm",
    variant: "ghost",
    className: "pl-1.5",
    onClick: () => {
      commandsManager.runCommand('exportTimeReportCSV', {
        segmentations,
        summaryStats: true,
        options: {
          filename: 'ROIStats.csv'
        }
      });
    }
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Export, null), /*#__PURE__*/react.createElement("span", {
    className: "pl-1"
  }, "ROI Stats"))));
}
/* harmony default export */ const panels_DynamicExport = (DynamicExport);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/getPanelModule.tsx





function getPanelModule({
  commandsManager,
  extensionManager,
  servicesManager,
  configuration
}) {
  const wrappedDynamicDataPanel = () => {
    return /*#__PURE__*/react.createElement(panels_DynamicDataPanel, {
      commandsManager: commandsManager,
      servicesManager: servicesManager,
      extensionManager: extensionManager
    });
  };
  const wrappedDynamicSegmentation = () => {
    return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement(ui_next_src/* Toolbox */.OO, {
      commandsManager: commandsManager,
      servicesManager: servicesManager,
      extensionManager: extensionManager,
      buttonSectionId: "dynamic-toolbox",
      title: "Threshold Tools"
    }), /*#__PURE__*/react.createElement(cornerstone_src.PanelSegmentation, {
      servicesManager: servicesManager,
      commandsManager: commandsManager,
      extensionManager: extensionManager,
      configuration: configuration
    }, /*#__PURE__*/react.createElement(panels_DynamicExport, {
      servicesManager: servicesManager,
      commandsManager: commandsManager
    })));
  };
  return [{
    name: 'dynamic-volume',
    iconName: 'tab-4d',
    iconLabel: '4D Workflow',
    label: '4D Workflow',
    component: wrappedDynamicDataPanel
  }, {
    name: 'dynamic-segmentation',
    iconName: 'tab-segmentation',
    iconLabel: 'Segmentation',
    label: 'Segmentation',
    component: wrappedDynamicSegmentation
  }];
}
/* harmony default export */ const src_getPanelModule = (getPanelModule);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/getHangingProtocolModule.ts
const DEFAULT_COLORMAP = '2hot';
const toolGroupIds = {
  pt: 'dynamic4D-pt',
  fusion: 'dynamic4D-fusion',
  ct: 'dynamic4D-ct'
};
function getPTOptions({
  colormap,
  voiInverted
} = {}) {
  return {
    blendMode: 'MIP',
    colormap,
    voi: {
      windowWidth: 5,
      windowCenter: 2.5
    },
    voiInverted
  };
}
function getPTViewports() {
  const ptOptionsParams = {
    colormap: {
      name: DEFAULT_COLORMAP,
      opacity: [{
        value: 0,
        opacity: 0
      }, {
        value: 0.1,
        opacity: 1
      }, {
        value: 1,
        opacity: 1
      }]
    },
    voiInverted: false
  };
  return [{
    viewportOptions: {
      viewportId: 'ptAxial',
      viewportType: 'volume',
      orientation: 'axial',
      toolGroupId: toolGroupIds.pt,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'axialSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ptWLSync',
        source: true,
        target: true
      }]
    },
    displaySets: [{
      id: 'ptDisplaySet',
      options: {
        ...getPTOptions(ptOptionsParams)
      }
    }]
  }, {
    viewportOptions: {
      viewportId: 'ptSagittal',
      viewportType: 'volume',
      orientation: 'sagittal',
      toolGroupId: toolGroupIds.pt,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'sagittalSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ptWLSync',
        source: true,
        target: true
      }]
    },
    displaySets: [{
      id: 'ptDisplaySet',
      options: {
        ...getPTOptions(ptOptionsParams)
      }
    }]
  }, {
    viewportOptions: {
      viewportId: 'ptCoronal',
      viewportType: 'volume',
      orientation: 'coronal',
      toolGroupId: toolGroupIds.pt,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'coronalSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ptWLSync',
        source: true,
        target: true
      }]
    },
    displaySets: [{
      id: 'ptDisplaySet',
      options: {
        ...getPTOptions(ptOptionsParams)
      }
    }]
  }];
}
function getFusionViewports() {
  const ptOptionsParams = {
    colormap: {
      name: DEFAULT_COLORMAP,
      opacity: [{
        value: 0,
        opacity: 0
      }, {
        value: 0.1,
        opacity: 0.8
      }, {
        value: 1,
        opacity: 0.8
      }]
    }
  };
  return [{
    viewportOptions: {
      viewportId: 'fusionAxial',
      viewportType: 'volume',
      orientation: 'axial',
      toolGroupId: toolGroupIds.fusion,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'axialSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ctWLSync',
        source: false,
        target: true
      }, {
        type: 'voi',
        id: 'fusionWLSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ptFusionWLSync',
        source: false,
        target: true,
        options: {
          syncInvertState: false
        }
      }, {
        type: 'hydrateseg',
        id: 'sameFORId',
        source: true,
        target: true,
        options: {
          matchingRules: ['sameFOR']
        }
      }]
    },
    displaySets: [{
      id: 'ctDisplaySet'
    }, {
      options: {
        ...getPTOptions(ptOptionsParams)
      },
      id: 'ptDisplaySet'
    }]
  }, {
    viewportOptions: {
      viewportId: 'fusionSagittal',
      viewportType: 'volume',
      orientation: 'sagittal',
      toolGroupId: toolGroupIds.fusion,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'sagittalSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ctWLSync',
        source: false,
        target: true
      }, {
        type: 'voi',
        id: 'fusionWLSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ptFusionWLSync',
        source: false,
        target: true,
        options: {
          syncInvertState: false
        }
      }, {
        type: 'hydrateseg',
        id: 'sameFORId',
        source: true,
        target: true,
        options: {
          matchingRules: ['sameFOR']
        }
      }]
    },
    displaySets: [{
      id: 'ctDisplaySet'
    }, {
      options: {
        ...getPTOptions(ptOptionsParams)
      },
      id: 'ptDisplaySet'
    }]
  }, {
    viewportOptions: {
      viewportId: 'fusionCoronal',
      viewportType: 'volume',
      orientation: 'coronal',
      toolGroupId: toolGroupIds.fusion,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'coronalSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ctWLSync',
        source: false,
        target: true
      }, {
        type: 'voi',
        id: 'fusionWLSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ptFusionWLSync',
        source: false,
        target: true,
        options: {
          syncInvertState: false
        }
      }, {
        type: 'hydrateseg',
        id: 'sameFORId',
        source: true,
        target: true,
        options: {
          matchingRules: ['sameFOR']
        }
      }]
    },
    displaySets: [{
      id: 'ctDisplaySet'
    }, {
      options: {
        ...getPTOptions(ptOptionsParams)
      },
      id: 'ptDisplaySet'
    }]
  }];
}
function getSeriesChartViewport() {
  return {
    viewportOptions: {
      viewportId: 'seriesChart'
    },
    displaySets: [{
      id: 'chartDisplaySet',
      options: {
        // This dataset does not require the download of any instance since it is pre-computed locally,
        // but interleaveTopToBottom.ts was not loading any series because it consider that all viewports
        // are a Cornerstone viewport which is not true in this case and it waits for all viewports to
        // have called interleaveTopToBottom(...).
        skipLoading: true
      }
    }]
  };
}
function getCTViewports() {
  return [{
    viewportOptions: {
      viewportId: 'ctAxial',
      viewportType: 'volume',
      orientation: 'axial',
      toolGroupId: toolGroupIds.ct,
      initialImageOptions: {
        preset: 'middle' // 'first', 'last', 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'axialSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ctWLSync',
        source: true,
        target: true
      }]
    },
    displaySets: [{
      id: 'ctDisplaySet'
    }]
  }, {
    viewportOptions: {
      viewportId: 'ctSagittal',
      viewportType: 'volume',
      orientation: 'sagittal',
      toolGroupId: toolGroupIds.ct,
      initialImageOptions: {
        preset: 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'sagittalSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ctWLSync',
        source: true,
        target: true
      }]
    },
    displaySets: [{
      id: 'ctDisplaySet'
    }]
  }, {
    viewportOptions: {
      viewportId: 'ctCoronal',
      viewportType: 'volume',
      orientation: 'coronal',
      toolGroupId: toolGroupIds.ct,
      initialImageOptions: {
        preset: 'middle'
      },
      syncGroups: [{
        type: 'cameraPosition',
        id: 'coronalSync',
        source: true,
        target: true
      }, {
        type: 'voi',
        id: 'ctWLSync',
        source: true,
        target: true
      }]
    },
    displaySets: [{
      id: 'ctDisplaySet'
    }]
  }];
}
const defaultProtocol = {
  id: 'default4D',
  locked: true,
  // Don't store this hanging protocol as it applies to the currently active
  // display set by default
  // cacheId: null,
  hasUpdatedPriorsInformation: false,
  name: 'Default',
  createdDate: '2023-01-01T00:00:00.000Z',
  modifiedDate: '2023-01-01T00:00:00.000Z',
  availableTo: {},
  editableBy: {},
  imageLoadStrategy: 'default',
  // "default" , "interleaveTopToBottom",  "interleaveCenter"
  protocolMatchingRules: [{
    attribute: 'ModalitiesInStudy',
    constraint: {
      contains: ['CT', 'PT']
    }
  }],
  // -1 would be used to indicate active only, whereas other values are
  // the number of required priors referenced - so 0 means active with
  // 0 or more priors.
  numberOfPriorsReferenced: -1,
  displaySetSelectors: {
    defaultDisplaySetId: {
      // Unused currently
      imageMatchingRules: [],
      // Matches displaysets, NOT series
      seriesMatchingRules: [
      // Try to match series with images by default, to prevent weird display
      // on SEG/SR containing studies
      {
        attribute: 'numImageFrames',
        constraint: {
          greaterThan: {
            value: 0
          }
        }
      }]
      // Can be used to select matching studies
      // studyMatchingRules: [],
    },
    ctDisplaySet: {
      // Unused currently
      imageMatchingRules: [],
      // Matches displaysets, NOT series
      seriesMatchingRules: [{
        attribute: 'Modality',
        constraint: {
          equals: {
            value: 'CT'
          }
        },
        required: true
      }, {
        attribute: 'isReconstructable',
        constraint: {
          equals: {
            value: true
          }
        },
        required: true
      }]
      // Can be used to select matching studies
      // studyMatchingRules: [],
    },
    ptDisplaySet: {
      // Unused currently
      imageMatchingRules: [],
      // Matches displaysets, NOT series
      seriesMatchingRules: [{
        attribute: 'Modality',
        constraint: {
          equals: 'PT'
        },
        required: true
      }, {
        attribute: 'isReconstructable',
        constraint: {
          equals: {
            value: true
          }
        },
        required: true
      }, {
        attribute: 'SeriesDescription',
        constraint: {
          contains: 'Corrected'
        }
      }, {
        weight: 2,
        attribute: 'SeriesDescription',
        constraint: {
          doesNotContain: {
            value: 'Uncorrected'
          }
        }
      }

      // Should we check if CorrectedImage contains ATTN?
      // (0028,0051) (CorrectedImage): NORM\DTIM\ATTN\SCAT\RADL\DECY
      ]
      // Can be used to select matching studies
      // studyMatchingRules: [],
    },
    chartDisplaySet: {
      // Unused currently
      imageMatchingRules: [],
      // Matches displaysets, NOT series
      seriesMatchingRules: [{
        attribute: 'Modality',
        constraint: {
          equals: {
            value: 'CHT'
          }
        },
        required: true
      }]
    }
  },
  stages: [{
    id: 'dataPreparation',
    name: 'Data Preparation',
    viewportStructure: {
      layoutType: 'grid',
      properties: {
        rows: 1,
        columns: 3
      }
    },
    viewports: [...getPTViewports()],
    createdDate: '2023-01-01T00:00:00.000Z'
  }, {
    id: 'registration',
    name: 'Registration',
    viewportStructure: {
      layoutType: 'grid',
      properties: {
        rows: 3,
        columns: 3
      }
    },
    viewports: [...getFusionViewports(), ...getCTViewports(), ...getPTViewports()],
    createdDate: '2023-01-01T00:00:00.000Z'
  }, {
    id: 'roiQuantification',
    name: 'ROI Quantification',
    viewportStructure: {
      layoutType: 'grid',
      properties: {
        rows: 1,
        columns: 3
      }
    },
    viewports: [...getFusionViewports()],
    createdDate: '2023-01-01T00:00:00.000Z'
  }, {
    id: 'kineticAnalysis',
    name: 'Kinetic Analysis',
    viewportStructure: {
      layoutType: 'grid',
      properties: {
        rows: 2,
        columns: 3,
        layoutOptions: [{
          x: 0,
          y: 0,
          width: 1 / 3,
          height: 1 / 2
        }, {
          x: 1 / 3,
          y: 0,
          width: 1 / 3,
          height: 1 / 2
        }, {
          x: 2 / 3,
          y: 0,
          width: 1 / 3,
          height: 1 / 2
        }, {
          x: 0,
          y: 1 / 2,
          width: 1,
          height: 1 / 2
        }]
      }
    },
    viewports: [...getFusionViewports(), getSeriesChartViewport()],
    createdDate: '2023-01-01T00:00:00.000Z'
  }]
};

/**
 * HangingProtocolModule should provide a list of hanging protocols that will be
 * available in OHIF for Modes to use to decide on the structure of the viewports
 * and also the series that hung in the viewports. Each hanging protocol is defined by
 * { name, protocols}. Examples include the default hanging protocol provided by
 * the default extension that shows 2x2 viewports.
 */

function getHangingProtocolModule() {
  return [{
    name: defaultProtocol.id,
    protocol: defaultProtocol
  }];
}
/* harmony default export */ const src_getHangingProtocolModule = (getHangingProtocolModule);
;// CONCATENATED MODULE: ../../../extensions/cornerstone-dynamic-volume/src/index.ts






/**
 * You can remove any of the following modules if you don't need them.
 */
const dynamicVolumeExtension = {
  /**
   * Only required property. Should be a unique value across all extensions.
   * You ID can be anything you want, but it should be unique.
   */
  id: id,
  /**
   * Perform any pre-registration tasks here. This is called before the extension
   * is registered. Usually we run tasks such as: configuring the libraries
   * (e.g. cornerstone, cornerstoneTools, ...) or registering any services that
   * this extension is providing.
   */
  preRegistration: ({
    servicesManager,
    commandsManager,
    configuration = {}
  }) => {
    // TODO: look for the right fix
    esm.cache.setMaxCacheSize(5 * 1024 * 1024 * 1024);
  },
  /**
   * PanelModule should provide a list of panels that will be available in OHIF
   * for Modes to consume and render. Each panel is defined by a {name,
   * iconName, iconLabel, label, component} object. Example of a panel module
   * is the StudyBrowserPanel that is provided by the default extension in OHIF.
   */
  getPanelModule: src_getPanelModule,
  /**
   * ViewportModule should provide a list of viewports that will be available in OHIF
   * for Modes to consume and use in the viewports. Each viewport is defined by
   * {name, component} object. Example of a viewport module is the CornerstoneViewport
   * that is provided by the Cornerstone extension in OHIF.
   */
  getHangingProtocolModule: src_getHangingProtocolModule,
  /**
   * CommandsModule should provide a list of commands that will be available in OHIF
   * for Modes to consume and use in the viewports. Each command is defined by
   * an object of { actions, definitions, defaultContext } where actions is an
   * object of functions, definitions is an object of available commands, their
   * options, and defaultContext is the default context for the command to run against.
   */
  getCommandsModule: ({
    servicesManager,
    commandsManager,
    extensionManager
  }) => {
    return src_commandsModule({
      servicesManager,
      commandsManager,
      extensionManager
    });
  }
};


/***/ })

}]);