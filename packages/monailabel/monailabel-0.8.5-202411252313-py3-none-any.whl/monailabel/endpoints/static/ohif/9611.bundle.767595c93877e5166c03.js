"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([[9611],{

/***/ 69611:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ Viewport_OHIFCornerstoneViewport)
});

// EXTERNAL MODULE: ../../../node_modules/react/index.js
var react = __webpack_require__(86326);
// EXTERNAL MODULE: ../../../node_modules/react-resize-detector/build/index.esm.js
var index_esm = __webpack_require__(81980);
// EXTERNAL MODULE: ../../../node_modules/@cornerstonejs/tools/dist/esm/index.js + 82 modules
var esm = __webpack_require__(55139);
// EXTERNAL MODULE: ../../../node_modules/@cornerstonejs/core/dist/esm/index.js
var dist_esm = __webpack_require__(81985);
// EXTERNAL MODULE: ../../core/src/index.ts + 71 modules
var src = __webpack_require__(29463);
// EXTERNAL MODULE: ../../ui/src/index.js + 690 modules
var ui_src = __webpack_require__(35647);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/state.ts
var state = __webpack_require__(71353);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/OHIFCornerstoneViewport.css
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ../../../node_modules/prop-types/index.js
var prop_types = __webpack_require__(97598);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/Overlays/ViewportImageScrollbar.tsx




function CornerstoneImageScrollbar({
  viewportData,
  viewportId,
  element,
  imageSliceData,
  setImageSliceData,
  scrollbarHeight,
  servicesManager
}) {
  const {
    cineService,
    cornerstoneViewportService
  } = servicesManager.services;
  const onImageScrollbarChange = (imageIndex, viewportId) => {
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    const {
      isCineEnabled
    } = cineService.getState();
    if (isCineEnabled) {
      // on image scrollbar change, stop the CINE if it is playing
      cineService.stopClip(element, {
        viewportId
      });
      cineService.setCine({
        id: viewportId,
        isPlaying: false
      });
    }
    dist_esm.utilities.jumpToSlice(viewport.element, {
      imageIndex,
      debounceLoading: true
    });
  };
  (0,react.useEffect)(() => {
    if (!viewportData) {
      return;
    }
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    if (!viewport || viewport instanceof dist_esm.VolumeViewport3D) {
      return;
    }
    const imageIndex = viewport.getCurrentImageIdIndex();
    const numberOfSlices = viewport.getNumberOfSlices();
    setImageSliceData({
      imageIndex: imageIndex,
      numberOfSlices
    });
  }, [viewportId, viewportData]);
  (0,react.useEffect)(() => {
    if (!viewportData) {
      return;
    }
    const {
      viewportType
    } = viewportData;
    const eventId = viewportType === dist_esm.Enums.ViewportType.STACK && dist_esm.Enums.Events.STACK_VIEWPORT_SCROLL || viewportType === dist_esm.Enums.ViewportType.ORTHOGRAPHIC && dist_esm.Enums.Events.VOLUME_NEW_IMAGE || dist_esm.Enums.Events.IMAGE_RENDERED;
    const updateIndex = event => {
      const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
      if (!viewport || viewport instanceof dist_esm.VolumeViewport3D) {
        return;
      }
      const {
        imageIndex,
        newImageIdIndex = imageIndex
      } = event.detail;
      const numberOfSlices = viewport.getNumberOfSlices();
      // find the index of imageId in the imageIds
      setImageSliceData({
        imageIndex: newImageIdIndex,
        numberOfSlices
      });
    };
    element.addEventListener(eventId, updateIndex);
    return () => {
      element.removeEventListener(eventId, updateIndex);
    };
  }, [viewportData, element]);
  return /*#__PURE__*/react.createElement(ui_src/* ImageScrollbar */.uq, {
    onChange: evt => onImageScrollbarChange(evt, viewportId),
    max: imageSliceData.numberOfSlices ? imageSliceData.numberOfSlices - 1 : 0,
    height: scrollbarHeight,
    value: imageSliceData.imageIndex || 0
  });
}
CornerstoneImageScrollbar.propTypes = {
  viewportData: (prop_types_default()).object,
  viewportId: (prop_types_default()).string.isRequired,
  element: prop_types_default().instanceOf(Element),
  scrollbarHeight: (prop_types_default()).string,
  imageSliceData: (prop_types_default()).object.isRequired,
  setImageSliceData: (prop_types_default()).func.isRequired,
  servicesManager: (prop_types_default()).object.isRequired
};
/* harmony default export */ const ViewportImageScrollbar = (CornerstoneImageScrollbar);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/Viewport/Overlays/CustomizableViewportOverlay.tsx + 2 modules
var CustomizableViewportOverlay = __webpack_require__(5791);
// EXTERNAL MODULE: ../../../node_modules/classnames/index.js
var classnames = __webpack_require__(55530);
var classnames_default = /*#__PURE__*/__webpack_require__.n(classnames);
// EXTERNAL MODULE: ../../../node_modules/gl-matrix/esm/index.js + 1 modules
var gl_matrix_esm = __webpack_require__(3823);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/Overlays/ViewportOrientationMarkers.css
// extracted by mini-css-extract-plugin

;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/Overlays/ViewportOrientationMarkers.tsx






const {
  getOrientationStringLPS,
  invertOrientationStringLPS
} = esm.utilities.orientation;
function ViewportOrientationMarkers({
  element,
  viewportData,
  imageSliceData,
  viewportId,
  servicesManager,
  orientationMarkers = ['top', 'left']
}) {
  // Rotation is in degrees
  const [rotation, setRotation] = (0,react.useState)(0);
  const [flipHorizontal, setFlipHorizontal] = (0,react.useState)(false);
  const [flipVertical, setFlipVertical] = (0,react.useState)(false);
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  (0,react.useEffect)(() => {
    const cameraModifiedListener = evt => {
      const {
        previousCamera,
        camera
      } = evt.detail;
      const {
        rotation
      } = camera;
      if (rotation !== undefined) {
        setRotation(rotation);
      }
      if (camera.flipHorizontal !== undefined && previousCamera.flipHorizontal !== camera.flipHorizontal) {
        setFlipHorizontal(camera.flipHorizontal);
      }
      if (camera.flipVertical !== undefined && previousCamera.flipVertical !== camera.flipVertical) {
        setFlipVertical(camera.flipVertical);
      }
    };
    element.addEventListener(dist_esm.Enums.Events.CAMERA_MODIFIED, cameraModifiedListener);
    return () => {
      element.removeEventListener(dist_esm.Enums.Events.CAMERA_MODIFIED, cameraModifiedListener);
    };
  }, []);
  const markers = (0,react.useMemo)(() => {
    if (!viewportData) {
      return '';
    }
    let rowCosines, columnCosines, isDefaultValueSetForRowCosine, isDefaultValueSetForColumnCosine;
    if (viewportData.viewportType === 'stack') {
      const imageIndex = imageSliceData.imageIndex;
      const imageId = viewportData.data[0].imageIds?.[imageIndex];

      // Workaround for below TODO stub
      if (!imageId) {
        return false;
      }
      ({
        rowCosines,
        columnCosines,
        isDefaultValueSetForColumnCosine,
        isDefaultValueSetForColumnCosine
      } = dist_esm.metaData.get('imagePlaneModule', imageId) || {});
    } else {
      if (!element || !(0,dist_esm.getEnabledElement)(element)) {
        return '';
      }
      const {
        viewport
      } = (0,dist_esm.getEnabledElement)(element);
      const {
        viewUp,
        viewPlaneNormal
      } = viewport.getCamera();
      const viewRight = gl_matrix_esm/* vec3.create */.eR.create();
      gl_matrix_esm/* vec3.cross */.eR.cross(viewRight, viewUp, viewPlaneNormal);
      columnCosines = [-viewUp[0], -viewUp[1], -viewUp[2]];
      rowCosines = viewRight;
    }
    if (!rowCosines || !columnCosines || rotation === undefined || isDefaultValueSetForRowCosine || isDefaultValueSetForColumnCosine) {
      return '';
    }
    const markers = _getOrientationMarkers(rowCosines, columnCosines, rotation, flipVertical, flipHorizontal);
    const ohifViewport = cornerstoneViewportService.getViewportInfo(viewportId);
    if (!ohifViewport) {
      console.log('ViewportOrientationMarkers::No viewport');
      return null;
    }
    return orientationMarkers.map((m, index) => /*#__PURE__*/react.createElement("div", {
      className: classnames_default()('overlay-text', `${m}-mid orientation-marker`, 'text-aqua-pale', 'text-[13px]', 'leading-5'),
      key: `${m}-mid orientation-marker`
    }, /*#__PURE__*/react.createElement("div", {
      className: "orientation-marker-value"
    }, markers[m])));
  }, [viewportData, imageSliceData, rotation, flipVertical, flipHorizontal, orientationMarkers, element]);
  return /*#__PURE__*/react.createElement("div", {
    className: "ViewportOrientationMarkers select-none"
  }, markers);
}

/**
 *
 * Computes the orientation labels on a Cornerstone-enabled Viewport element
 * when the viewport settings change (e.g. when a horizontal flip or a rotation occurs)
 *
 * @param {*} rowCosines
 * @param {*} columnCosines
 * @param {*} rotation in degrees
 * @returns
 */
function _getOrientationMarkers(rowCosines, columnCosines, rotation, flipVertical, flipHorizontal) {
  const rowString = getOrientationStringLPS(rowCosines);
  const columnString = getOrientationStringLPS(columnCosines);
  const oppositeRowString = invertOrientationStringLPS(rowString);
  const oppositeColumnString = invertOrientationStringLPS(columnString);
  const markers = {
    top: oppositeColumnString,
    left: oppositeRowString,
    right: rowString,
    bottom: columnString
  };

  // If any vertical or horizontal flips are applied, change the orientation strings ahead of
  // the rotation applications
  if (flipVertical) {
    markers.top = invertOrientationStringLPS(markers.top);
    markers.bottom = invertOrientationStringLPS(markers.bottom);
  }
  if (flipHorizontal) {
    markers.left = invertOrientationStringLPS(markers.left);
    markers.right = invertOrientationStringLPS(markers.right);
  }

  // Swap the labels accordingly if the viewport has been rotated
  // This could be done in a more complex way for intermediate rotation values (e.g. 45 degrees)
  if (rotation === 90 || rotation === -270) {
    return {
      top: markers.left,
      left: invertOrientationStringLPS(markers.top),
      right: invertOrientationStringLPS(markers.bottom),
      bottom: markers.right // left
    };
  } else if (rotation === -90 || rotation === 270) {
    return {
      top: invertOrientationStringLPS(markers.left),
      left: markers.top,
      bottom: markers.left,
      right: markers.bottom
    };
  } else if (rotation === 180 || rotation === -180) {
    return {
      top: invertOrientationStringLPS(markers.top),
      left: invertOrientationStringLPS(markers.left),
      bottom: invertOrientationStringLPS(markers.bottom),
      right: invertOrientationStringLPS(markers.right)
    };
  }
  return markers;
}
/* harmony default export */ const Overlays_ViewportOrientationMarkers = (ViewportOrientationMarkers);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/Overlays/ViewportImageSliceLoadingIndicator.tsx



function ViewportImageSliceLoadingIndicator({
  viewportData,
  element
}) {
  const [loading, setLoading] = (0,react.useState)(false);
  const [error, setError] = (0,react.useState)(false);
  const loadIndicatorRef = (0,react.useRef)(null);
  const imageIdToBeLoaded = (0,react.useRef)(null);
  const setLoadingState = evt => {
    clearTimeout(loadIndicatorRef.current);
    loadIndicatorRef.current = setTimeout(() => {
      setLoading(true);
    }, 50);
  };
  const setFinishLoadingState = evt => {
    clearTimeout(loadIndicatorRef.current);
    setLoading(false);
  };
  const setErrorState = evt => {
    clearTimeout(loadIndicatorRef.current);
    if (imageIdToBeLoaded.current === evt.detail.imageId) {
      setError(evt.detail.error);
      imageIdToBeLoaded.current = null;
    }
  };
  (0,react.useEffect)(() => {
    element.addEventListener(dist_esm.Enums.Events.STACK_VIEWPORT_SCROLL, setLoadingState);
    element.addEventListener(dist_esm.Enums.Events.IMAGE_LOAD_ERROR, setErrorState);
    element.addEventListener(dist_esm.Enums.Events.STACK_NEW_IMAGE, setFinishLoadingState);
    return () => {
      element.removeEventListener(dist_esm.Enums.Events.STACK_VIEWPORT_SCROLL, setLoadingState);
      element.removeEventListener(dist_esm.Enums.Events.STACK_NEW_IMAGE, setFinishLoadingState);
      element.removeEventListener(dist_esm.Enums.Events.IMAGE_LOAD_ERROR, setErrorState);
    };
  }, [element, viewportData]);
  if (error) {
    return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement("div", {
      className: "absolute top-0 left-0 h-full w-full bg-black opacity-50"
    }, /*#__PURE__*/react.createElement("div", {
      className: "transparent flex h-full w-full items-center justify-center"
    }, /*#__PURE__*/react.createElement("p", {
      className: "text-primary-light text-xl font-light"
    }, /*#__PURE__*/react.createElement("h4", null, "Error Loading Image"), /*#__PURE__*/react.createElement("p", null, "An error has occurred."), /*#__PURE__*/react.createElement("p", null, error)))));
  }
  if (loading) {
    return (
      /*#__PURE__*/
      // IMPORTANT: we need to use the pointer-events-none class to prevent the loading indicator from
      // interacting with the mouse, since scrolling should propagate to the viewport underneath
      react.createElement("div", {
        className: "pointer-events-none absolute top-0 left-0 h-full w-full bg-black opacity-50"
      }, /*#__PURE__*/react.createElement("div", {
        className: "transparent flex h-full w-full items-center justify-center"
      }, /*#__PURE__*/react.createElement("p", {
        className: "text-primary-light text-xl font-light"
      }, "Loading...")))
    );
  }
  return null;
}
ViewportImageSliceLoadingIndicator.propTypes = {
  error: (prop_types_default()).object,
  element: (prop_types_default()).object
};
/* harmony default export */ const Overlays_ViewportImageSliceLoadingIndicator = (ViewportImageSliceLoadingIndicator);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/Overlays/CornerstoneOverlays.tsx





function CornerstoneOverlays(props) {
  const {
    viewportId,
    element,
    scrollbarHeight,
    servicesManager
  } = props;
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const [imageSliceData, setImageSliceData] = (0,react.useState)({
    imageIndex: 0,
    numberOfSlices: 0
  });
  const [viewportData, setViewportData] = (0,react.useState)(null);
  (0,react.useEffect)(() => {
    const {
      unsubscribe
    } = cornerstoneViewportService.subscribe(cornerstoneViewportService.EVENTS.VIEWPORT_DATA_CHANGED, props => {
      if (props.viewportId !== viewportId) {
        return;
      }
      setViewportData(props.viewportData);
    });
    return () => {
      unsubscribe();
    };
  }, [viewportId]);
  if (!element) {
    return null;
  }
  if (viewportData) {
    const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
    if (viewportInfo?.viewportOptions?.customViewportProps?.hideOverlays) {
      return null;
    }
  }
  return /*#__PURE__*/react.createElement("div", {
    className: "noselect"
  }, /*#__PURE__*/react.createElement(ViewportImageScrollbar, {
    viewportId: viewportId,
    viewportData: viewportData,
    element: element,
    imageSliceData: imageSliceData,
    setImageSliceData: setImageSliceData,
    scrollbarHeight: scrollbarHeight,
    servicesManager: servicesManager
  }), /*#__PURE__*/react.createElement(CustomizableViewportOverlay/* default */.Ay, {
    imageSliceData: imageSliceData,
    viewportData: viewportData,
    viewportId: viewportId,
    servicesManager: servicesManager,
    element: element
  }), /*#__PURE__*/react.createElement(Overlays_ViewportImageSliceLoadingIndicator, {
    viewportData: viewportData,
    element: element
  }), /*#__PURE__*/react.createElement(Overlays_ViewportOrientationMarkers, {
    imageSliceData: imageSliceData,
    element: element,
    viewportData: viewportData,
    servicesManager: servicesManager,
    viewportId: viewportId
  }));
}
/* harmony default export */ const Overlays_CornerstoneOverlays = (CornerstoneOverlays);
// EXTERNAL MODULE: ./state/index.js + 1 modules
var state_0 = __webpack_require__(45981);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/CinePlayer/CinePlayer.tsx




function WrappedCinePlayer({
  enabledVPElement,
  viewportId,
  servicesManager
}) {
  const {
    customizationService,
    displaySetService,
    viewportGridService
  } = servicesManager.services;
  const [{
    isCineEnabled,
    cines
  }, cineService] = (0,ui_src/* useCine */.tq)();
  const [newStackFrameRate, setNewStackFrameRate] = (0,react.useState)(24);
  const [dynamicInfo, setDynamicInfo] = (0,react.useState)(null);
  const [appConfig] = (0,state_0/* useAppConfig */.r)();
  const isMountedRef = (0,react.useRef)(null);
  const cineHandler = () => {
    if (!cines?.[viewportId] || !enabledVPElement) {
      return;
    }
    const {
      isPlaying = false,
      frameRate = 24
    } = cines[viewportId];
    const validFrameRate = Math.max(frameRate, 1);
    return isPlaying ? cineService.playClip(enabledVPElement, {
      framesPerSecond: validFrameRate,
      viewportId
    }) : cineService.stopClip(enabledVPElement);
  };
  const newDisplaySetHandler = (0,react.useCallback)(() => {
    if (!enabledVPElement || !isCineEnabled) {
      return;
    }
    const {
      viewports
    } = viewportGridService.getState();
    const {
      displaySetInstanceUIDs
    } = viewports.get(viewportId);
    let frameRate = 24;
    let isPlaying = cines[viewportId]?.isPlaying || false;
    displaySetInstanceUIDs.forEach(displaySetInstanceUID => {
      const displaySet = displaySetService.getDisplaySetByUID(displaySetInstanceUID);
      if (displaySet.FrameRate) {
        // displaySet.FrameRate corresponds to DICOM tag (0018,1063) which is defined as the the frame time in milliseconds
        // So a bit of math to get the actual frame rate.
        frameRate = Math.round(1000 / displaySet.FrameRate);
        isPlaying ||= !!appConfig.autoPlayCine;
      }

      // check if the displaySet is dynamic and set the dynamic info
      if (displaySet.isDynamicVolume) {
        const {
          dynamicVolumeInfo
        } = displaySet;
        const numTimePoints = dynamicVolumeInfo.timePoints.length;
        const label = dynamicVolumeInfo.splittingTag;
        const timePointIndex = dynamicVolumeInfo.timePointIndex || 0;
        setDynamicInfo({
          volumeId: displaySet.displaySetInstanceUID,
          timePointIndex,
          numTimePoints,
          label
        });
      } else {
        setDynamicInfo(null);
      }
    });
    if (isPlaying) {
      cineService.setIsCineEnabled(isPlaying);
    }
    cineService.setCine({
      id: viewportId,
      isPlaying,
      frameRate
    });
    setNewStackFrameRate(frameRate);
  }, [displaySetService, viewportId, viewportGridService, cines, isCineEnabled, enabledVPElement]);
  (0,react.useEffect)(() => {
    isMountedRef.current = true;
    newDisplaySetHandler();
    return () => {
      isMountedRef.current = false;
    };
  }, [isCineEnabled, newDisplaySetHandler]);
  (0,react.useEffect)(() => {
    if (!isCineEnabled) {
      return;
    }
    cineHandler();
  }, [isCineEnabled, cineHandler, enabledVPElement]);

  /**
   * Use effect for handling new display set
   */
  (0,react.useEffect)(() => {
    if (!enabledVPElement) {
      return;
    }
    enabledVPElement.addEventListener(dist_esm.Enums.Events.VIEWPORT_NEW_IMAGE_SET, newDisplaySetHandler);
    // this doesn't makes sense that we are listening to this event on viewport element
    enabledVPElement.addEventListener(dist_esm.Enums.Events.VOLUME_VIEWPORT_NEW_VOLUME, newDisplaySetHandler);
    return () => {
      cineService.setCine({
        id: viewportId,
        isPlaying: false
      });
      enabledVPElement.removeEventListener(dist_esm.Enums.Events.VIEWPORT_NEW_IMAGE_SET, newDisplaySetHandler);
      enabledVPElement.removeEventListener(dist_esm.Enums.Events.VOLUME_VIEWPORT_NEW_VOLUME, newDisplaySetHandler);
    };
  }, [enabledVPElement, newDisplaySetHandler, viewportId]);
  (0,react.useEffect)(() => {
    if (!cines || !cines[viewportId] || !enabledVPElement || !isMountedRef.current) {
      return;
    }
    cineHandler();
    return () => {
      cineService.stopClip(enabledVPElement, {
        viewportId
      });
    };
  }, [cines, viewportId, cineService, enabledVPElement, cineHandler]);
  if (!isCineEnabled) {
    return null;
  }
  const cine = cines[viewportId];
  const isPlaying = cine?.isPlaying || false;
  return /*#__PURE__*/react.createElement(RenderCinePlayer, {
    viewportId: viewportId,
    cineService: cineService,
    newStackFrameRate: newStackFrameRate,
    isPlaying: isPlaying,
    dynamicInfo: dynamicInfo,
    customizationService: customizationService
  });
}
function RenderCinePlayer({
  viewportId,
  cineService,
  newStackFrameRate,
  isPlaying,
  dynamicInfo: dynamicInfoProp,
  customizationService
}) {
  const {
    component: CinePlayerComponent = ui_src/* CinePlayer */.F0
  } = customizationService.get('cinePlayer') ?? {};
  const [dynamicInfo, setDynamicInfo] = (0,react.useState)(dynamicInfoProp);
  (0,react.useEffect)(() => {
    setDynamicInfo(dynamicInfoProp);
  }, [dynamicInfoProp]);

  /**
   * Use effect for handling 4D time index changed
   */
  (0,react.useEffect)(() => {
    if (!dynamicInfo) {
      return;
    }
    const handleTimePointIndexChange = evt => {
      const {
        volumeId,
        timePointIndex,
        numTimePoints,
        splittingTag
      } = evt.detail;
      setDynamicInfo({
        volumeId,
        timePointIndex,
        numTimePoints,
        label: splittingTag
      });
    };
    dist_esm.eventTarget.addEventListener(dist_esm.Enums.Events.DYNAMIC_VOLUME_TIME_POINT_INDEX_CHANGED, handleTimePointIndexChange);
    return () => {
      dist_esm.eventTarget.removeEventListener(dist_esm.Enums.Events.DYNAMIC_VOLUME_TIME_POINT_INDEX_CHANGED, handleTimePointIndexChange);
    };
  }, [dynamicInfo]);
  (0,react.useEffect)(() => {
    if (!dynamicInfo) {
      return;
    }
    const {
      volumeId,
      timePointIndex,
      numTimePoints,
      splittingTag
    } = dynamicInfo || {};
    const volume = dist_esm.cache.getVolume(volumeId, true);
    volume.timePointIndex = timePointIndex;
    setDynamicInfo({
      volumeId,
      timePointIndex,
      numTimePoints,
      label: splittingTag
    });
  }, []);
  const updateDynamicInfo = (0,react.useCallback)(props => {
    const {
      volumeId,
      timePointIndex
    } = props;
    const volume = dist_esm.cache.getVolume(volumeId, true);
    volume.timePointIndex = timePointIndex;
  }, []);
  return /*#__PURE__*/react.createElement(CinePlayerComponent, {
    className: "absolute left-1/2 bottom-3 -translate-x-1/2",
    frameRate: newStackFrameRate,
    isPlaying: isPlaying,
    onClose: () => {
      // also stop the clip
      cineService.setCine({
        id: viewportId,
        isPlaying: false
      });
      cineService.setIsCineEnabled(false);
      cineService.setViewportCineClosed(viewportId);
    },
    onPlayPauseChange: isPlaying => {
      cineService.setCine({
        id: viewportId,
        isPlaying
      });
    },
    onFrameRateChange: frameRate => cineService.setCine({
      id: viewportId,
      frameRate
    }),
    dynamicInfo: dynamicInfo,
    updateDynamicInfo: updateDynamicInfo
  });
}
/* harmony default export */ const CinePlayer = (WrappedCinePlayer);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/CinePlayer/index.ts

/* harmony default export */ const components_CinePlayer = (CinePlayer);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/contextProviders/ViewportActionCornersProvider.tsx
var ViewportActionCornersProvider = __webpack_require__(76255);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/OHIFViewportActionCorners.tsx



function OHIFViewportActionCorners({
  viewportId
}) {
  const [viewportActionCornersState] = (0,ViewportActionCornersProvider/* useViewportActionCornersContext */.R4)();
  if (!viewportActionCornersState[viewportId]) {
    return null;
  }
  return /*#__PURE__*/react.createElement(ui_src/* ViewportActionCorners */.R2, {
    cornerComponents: viewportActionCornersState[viewportId]
  });
}
/* harmony default export */ const components_OHIFViewportActionCorners = (OHIFViewportActionCorners);
// EXTERNAL MODULE: ../../../node_modules/react-i18next/dist/es/index.js + 15 modules
var es = __webpack_require__(99993);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/Colormap.tsx



function Colormap({
  colormaps,
  viewportId,
  displaySets,
  commandsManager,
  servicesManager
}) {
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const [activeDisplaySet, setActiveDisplaySet] = (0,react.useState)(displaySets[0]);
  const [showPreview, setShowPreview] = (0,react.useState)(false);
  const [prePreviewColormap, setPrePreviewColormap] = (0,react.useState)(null);
  const showPreviewRef = (0,react.useRef)(showPreview);
  showPreviewRef.current = showPreview;
  const prePreviewColormapRef = (0,react.useRef)(prePreviewColormap);
  prePreviewColormapRef.current = prePreviewColormap;
  const activeDisplaySetRef = (0,react.useRef)(activeDisplaySet);
  activeDisplaySetRef.current = activeDisplaySet;
  const onSetColorLUT = (0,react.useCallback)(props => {
    // TODO: Better way to check if it's a fusion
    const oneOpacityColormaps = ['Grayscale', 'X Ray'];
    const opacity = displaySets.length > 1 && !oneOpacityColormaps.includes(props.colormap.name) ? 0.5 : 1;
    commandsManager.run({
      commandName: 'setViewportColormap',
      commandOptions: {
        ...props,
        opacity,
        immediate: true
      },
      context: 'CORNERSTONE'
    });
  }, [commandsManager]);
  const getViewportColormap = (viewportId, displaySet) => {
    const {
      displaySetInstanceUID
    } = displaySet;
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    if (viewport instanceof dist_esm.StackViewport) {
      const {
        colormap
      } = viewport.getProperties();
      if (!colormap) {
        return colormaps.find(c => c.Name === 'Grayscale') || colormaps[0];
      }
      return colormap;
    }
    const actorEntries = viewport.getActors();
    const actorEntry = actorEntries?.find(entry => entry.referencedId.includes(displaySetInstanceUID));
    const {
      colormap
    } = viewport.getProperties(actorEntry.referencedId);
    if (!colormap) {
      return colormaps.find(c => c.Name === 'Grayscale') || colormaps[0];
    }
    return colormap;
  };
  const buttons = (0,react.useMemo)(() => {
    return displaySets.map((displaySet, index) => ({
      children: displaySet.Modality,
      key: index,
      style: {
        minWidth: `calc(100% / ${displaySets.length})`,
        fontSize: '0.8rem',
        textAlign: 'center',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
      }
    }));
  }, [displaySets]);
  (0,react.useEffect)(() => {
    setActiveDisplaySet(displaySets[displaySets.length - 1]);
  }, [displaySets]);
  return /*#__PURE__*/react.createElement(react.Fragment, null, buttons.length > 1 && /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex w-full justify-center"
  }, /*#__PURE__*/react.createElement(ui_src/* ButtonGroup */.e2, {
    onActiveIndexChange: index => {
      setActiveDisplaySet(displaySets[index]);
      setPrePreviewColormap(null);
    },
    activeIndex: displaySets.findIndex(ds => ds.displaySetInstanceUID === activeDisplaySetRef.current.displaySetInstanceUID) || 1,
    className: "w-[70%] text-[10px]"
  }, buttons.map(({
    children,
    key,
    style
  }) => /*#__PURE__*/react.createElement("div", {
    key: key,
    style: style
  }, children)))), /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex w-full justify-center"
  }, /*#__PURE__*/react.createElement(ui_src/* SwitchButton */.L$, {
    label: "Preview in viewport",
    checked: showPreview,
    onChange: checked => {
      setShowPreview(checked);
    }
  })), /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.DividerItem */.se.VG, null), /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.ItemPanel */.se.cV, null, colormaps.map((colormap, index) => /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.Item */.se.q7, {
    key: index,
    label: colormap.description,
    onClick: () => {
      onSetColorLUT({
        viewportId,
        colormap,
        displaySetInstanceUID: activeDisplaySetRef.current.displaySetInstanceUID
      });
      setPrePreviewColormap(null);
    },
    onMouseEnter: () => {
      if (showPreviewRef.current) {
        setPrePreviewColormap(getViewportColormap(viewportId, activeDisplaySetRef.current));
        onSetColorLUT({
          viewportId,
          colormap,
          displaySetInstanceUID: activeDisplaySetRef.current.displaySetInstanceUID
        });
      }
    },
    onMouseLeave: () => {
      if (showPreviewRef.current && prePreviewColormapRef.current) {
        onSetColorLUT({
          viewportId,
          colormap: prePreviewColormapRef.current,
          displaySetInstanceUID: activeDisplaySetRef.current.displaySetInstanceUID
        });
      }
    }
  }))));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/Colorbar.tsx




function setViewportColorbar(viewportId, displaySets, commandsManager, servicesManager, colorbarOptions) {
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
  const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
  const backgroundColor = viewportInfo.getViewportOptions().background;
  const isLight = backgroundColor ? dist_esm.utilities.isEqual(backgroundColor, [1, 1, 1]) : false;
  if (isLight) {
    colorbarOptions.ticks = {
      position: 'left',
      style: {
        font: '12px Arial',
        color: '#000000',
        maxNumTicks: 8,
        tickSize: 5,
        tickWidth: 1,
        labelMargin: 3
      }
    };
  }
  const displaySetInstanceUIDs = [];
  if (viewport instanceof dist_esm.StackViewport) {
    displaySetInstanceUIDs.push(viewportId);
  }
  if (viewport instanceof dist_esm.VolumeViewport) {
    displaySets.forEach(ds => {
      displaySetInstanceUIDs.push(ds.displaySetInstanceUID);
    });
  }
  commandsManager.run({
    commandName: 'toggleViewportColorbar',
    commandOptions: {
      viewportId,
      options: colorbarOptions,
      displaySetInstanceUIDs
    },
    context: 'CORNERSTONE'
  });
}
function Colorbar({
  viewportId,
  displaySets,
  commandsManager,
  servicesManager,
  colorbarProperties
}) {
  const {
    colorbarService
  } = servicesManager.services;
  const {
    width: colorbarWidth,
    colorbarTickPosition,
    colorbarContainerPosition,
    colormaps,
    colorbarInitialColormap
  } = colorbarProperties;
  const [showColorbar, setShowColorbar] = (0,react.useState)(colorbarService.hasColorbar(viewportId));
  const onSetColorbar = (0,react.useCallback)(() => {
    setViewportColorbar(viewportId, displaySets, commandsManager, servicesManager, {
      viewportId,
      colormaps,
      ticks: {
        position: colorbarTickPosition
      },
      width: colorbarWidth,
      position: colorbarContainerPosition,
      activeColormapName: colorbarInitialColormap
    });
  }, [commandsManager]);
  (0,react.useEffect)(() => {
    const updateColorbarState = () => {
      setShowColorbar(colorbarService.hasColorbar(viewportId));
    };
    const {
      unsubscribe
    } = colorbarService.subscribe(colorbarService.EVENTS.STATE_CHANGED, updateColorbarState);
    return () => {
      unsubscribe();
    };
  }, [viewportId]);
  return /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex w-full justify-center"
  }, /*#__PURE__*/react.createElement("div", {
    className: "mr-2 w-[28px]"
  }), /*#__PURE__*/react.createElement(ui_src/* SwitchButton */.L$, {
    label: "Display Color bar",
    checked: showColorbar,
    onChange: () => {
      onSetColorbar();
    }
  }));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/WindowLevel.tsx



function WindowLevel({
  viewportId,
  commandsManager,
  presets
}) {
  const {
    t
  } = (0,es/* useTranslation */.Bd)('WindowLevelActionMenu');
  const onSetWindowLevel = (0,react.useCallback)(props => {
    commandsManager.run({
      commandName: 'setViewportWindowLevel',
      commandOptions: {
        ...props,
        viewportId
      },
      context: 'CORNERSTONE'
    });
  }, [commandsManager, viewportId]);
  return /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.ItemPanel */.se.cV, null, presets.map((modalityPresets, modalityIndex) => /*#__PURE__*/react.createElement(react.Fragment, {
    key: modalityIndex
  }, Object.entries(modalityPresets).map(([modality, presetsArray]) => /*#__PURE__*/react.createElement(react.Fragment, {
    key: modality
  }, /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.HeaderItem */.se.N5, null, t('Modality Presets', {
    modality
  })), presetsArray.map((preset, index) => /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.Item */.se.q7, {
    key: `${modality}-${index}`,
    label: preset.description,
    secondaryLabel: `${preset.window} / ${preset.level}`,
    onClick: () => onSetWindowLevel(preset)
  })))))));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeRenderingPresetsContent.tsx




function VolumeRenderingPresetsContent({
  presets,
  viewportId,
  commandsManager,
  onClose
}) {
  const [filteredPresets, setFilteredPresets] = (0,react.useState)(presets);
  const [searchValue, setSearchValue] = (0,react.useState)('');
  const [selectedPreset, setSelectedPreset] = (0,react.useState)(null);
  const handleSearchChange = (0,react.useCallback)(value => {
    setSearchValue(value);
    const filtered = value ? presets.filter(preset => preset.name.toLowerCase().includes(value.toLowerCase())) : presets;
    setFilteredPresets(filtered);
  }, [presets]);
  const handleApply = (0,react.useCallback)(props => {
    commandsManager.runCommand('setViewportPreset', {
      ...props
    });
  }, [commandsManager]);
  const formatLabel = (label, maxChars) => {
    return label.length > maxChars ? `${label.slice(0, maxChars)}...` : label;
  };
  return /*#__PURE__*/react.createElement("div", {
    className: "flex min-h-full w-full flex-col justify-between"
  }, /*#__PURE__*/react.createElement("div", {
    className: "border-secondary-light h-[433px] w-full overflow-hidden rounded border bg-black px-2.5"
  }, /*#__PURE__*/react.createElement("div", {
    className: "flex h-[46px] w-full items-center justify-start"
  }, /*#__PURE__*/react.createElement("div", {
    className: "h-[26px] w-[200px]"
  }, /*#__PURE__*/react.createElement(ui_src/* InputFilterText */.Cv, {
    value: searchValue,
    onDebounceChange: handleSearchChange,
    placeholder: 'Search all'
  }))), /*#__PURE__*/react.createElement("div", {
    className: "ohif-scrollbar overflow h-[385px] w-full overflow-y-auto"
  }, /*#__PURE__*/react.createElement("div", {
    className: "grid grid-cols-4 gap-3 pt-2 pr-3"
  }, filteredPresets.map((preset, index) => /*#__PURE__*/react.createElement("div", {
    key: index,
    className: "flex cursor-pointer flex-col items-start",
    onClick: () => {
      setSelectedPreset(preset);
      handleApply({
        preset: preset.name,
        viewportId
      });
    }
  }, /*#__PURE__*/react.createElement(ui_src/* Icon */.In, {
    name: preset.name,
    className: selectedPreset?.name === preset.name ? 'border-primary-light h-[75px] w-[95px] max-w-none rounded border-2' : 'hover:border-primary-light h-[75px] w-[95px] max-w-none rounded border-2 border-black'
  }), /*#__PURE__*/react.createElement("label", {
    className: "text-aqua-pale mt-2 text-left text-xs"
  }, formatLabel(preset.name, 11))))))), /*#__PURE__*/react.createElement("footer", {
    className: "flex h-[60px] w-full items-center justify-end"
  }, /*#__PURE__*/react.createElement("div", {
    className: "flex"
  }, /*#__PURE__*/react.createElement(ui_src/* Button */.$n, {
    name: "Cancel",
    size: ui_src/* ButtonEnums.size */.Ny.Ej.medium,
    type: ui_src/* ButtonEnums.type */.Ny.NW.secondary,
    onClick: onClose
  }, ' ', "Cancel", ' '))));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeRenderingPresets.tsx



function VolumeRenderingPresets({
  viewportId,
  servicesManager,
  commandsManager,
  volumeRenderingPresets
}) {
  const {
    uiModalService
  } = servicesManager.services;
  const onClickPresets = () => {
    uiModalService.show({
      content: VolumeRenderingPresetsContent,
      title: 'Rendering Presets',
      movable: true,
      contentProps: {
        onClose: uiModalService.hide,
        presets: volumeRenderingPresets,
        viewportId,
        commandsManager
      },
      containerDimensions: 'h-[543px] w-[460px]',
      contentDimensions: 'h-[493px] w-[460px]  pl-[12px] pr-[12px]'
    });
  };
  return /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.Item */.se.q7, {
    label: "Rendering Presets",
    icon: /*#__PURE__*/react.createElement(ui_src/* Icon */.In, {
      name: "VolumeRendering"
    }),
    rightIcon: /*#__PURE__*/react.createElement(ui_src/* Icon */.In, {
      name: "action-new-dialog"
    }),
    onClick: onClickPresets
  });
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeRenderingQuality.tsx

function VolumeRenderingQuality({
  volumeRenderingQualityRange,
  commandsManager,
  servicesManager,
  viewportId
}) {
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const {
    min,
    max,
    step
  } = volumeRenderingQualityRange;
  const [quality, setQuality] = (0,react.useState)(null);
  const onChange = (0,react.useCallback)(value => {
    commandsManager.runCommand('setVolumeRenderingQulaity', {
      viewportId,
      volumeQuality: value
    });
    setQuality(value);
  }, [commandsManager, viewportId]);
  const calculateBackground = value => {
    const percentage = (value - 0) / (1 - 0) * 100;
    return `linear-gradient(to right, #5acce6 0%, #5acce6 ${percentage}%, #3a3f99 ${percentage}%, #3a3f99 100%)`;
  };
  (0,react.useEffect)(() => {
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    const {
      actor
    } = viewport.getActors()[0];
    const mapper = actor.getMapper();
    const image = mapper.getInputData();
    const spacing = image.getSpacing();
    const sampleDistance = mapper.getSampleDistance();
    const averageSpacing = spacing.reduce((a, b) => a + b) / 3.0;
    if (sampleDistance === averageSpacing) {
      setQuality(1);
    } else {
      setQuality(Math.sqrt(averageSpacing / (sampleDistance * 0.5)));
    }
  }, [cornerstoneViewportService, viewportId]);
  return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex  w-full flex-row !items-center justify-between gap-[10px]"
  }, /*#__PURE__*/react.createElement("label", {
    className: "block text-white",
    htmlFor: "volume"
  }, "Quality"), quality !== null && /*#__PURE__*/react.createElement("input", {
    className: "bg-inputfield-main h-2 w-[120px] cursor-pointer appearance-none rounded-lg",
    value: quality,
    id: "volume",
    max: max,
    min: min,
    type: "range",
    step: step,
    onChange: e => onChange(parseInt(e.target.value, 10)),
    style: {
      background: calculateBackground((quality - min) / (max - min)),
      '--thumb-inner-color': '#5acce6',
      '--thumb-outer-color': '#090c29'
    }
  })));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeShift.tsx

function VolumeShift({
  viewportId,
  commandsManager,
  servicesManager
}) {
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const [minShift, setMinShift] = (0,react.useState)(null);
  const [maxShift, setMaxShift] = (0,react.useState)(null);
  const [shift, setShift] = (0,react.useState)(cornerstoneViewportService.getCornerstoneViewport(viewportId)?.shiftedBy || 0);
  const [step, setStep] = (0,react.useState)(null);
  const [isBlocking, setIsBlocking] = (0,react.useState)(false);
  const prevShiftRef = (0,react.useRef)(shift);
  const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
  const {
    actor
  } = viewport.getActors()[0];
  const ofun = actor.getProperty().getScalarOpacity(0);
  (0,react.useEffect)(() => {
    if (isBlocking) {
      return;
    }
    const range = ofun.getRange();
    const transferFunctionWidth = range[1] - range[0];
    const minShift = -transferFunctionWidth;
    const maxShift = transferFunctionWidth;
    setMinShift(minShift);
    setMaxShift(maxShift);
    setStep(Math.pow(10, Math.floor(Math.log10(transferFunctionWidth / 500))));
  }, [cornerstoneViewportService, viewportId, actor, ofun, isBlocking]);
  const onChangeRange = (0,react.useCallback)(newShift => {
    const shiftDifference = newShift - prevShiftRef.current;
    prevShiftRef.current = newShift;
    viewport.shiftedBy = newShift;
    commandsManager.runCommand('shiftVolumeOpacityPoints', {
      viewportId,
      shift: shiftDifference
    });
  }, [commandsManager, viewportId, viewport]);
  const calculateBackground = value => {
    const percentage = (value - 0) / (1 - 0) * 100;
    return `linear-gradient(to right, #5acce6 0%, #5acce6 ${percentage}%, #3a3f99 ${percentage}%, #3a3f99 100%)`;
  };
  return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex  w-full flex-row !items-center justify-between gap-[10px]"
  }, /*#__PURE__*/react.createElement("label", {
    className: "block  text-white",
    htmlFor: "shift"
  }, "Shift"), step !== null && /*#__PURE__*/react.createElement("input", {
    className: "bg-inputfield-main h-2 w-[120px] cursor-pointer appearance-none rounded-lg",
    value: shift,
    onChange: e => {
      const shiftValue = parseInt(e.target.value, 10);
      setShift(shiftValue);
      onChangeRange(shiftValue);
    },
    id: "shift",
    onMouseDown: () => setIsBlocking(true),
    onMouseUp: () => setIsBlocking(false),
    max: maxShift,
    min: minShift,
    type: "range",
    step: step,
    style: {
      background: calculateBackground((shift - minShift) / (maxShift - minShift)),
      '--thumb-inner-color': '#5acce6',
      '--thumb-outer-color': '#090c29'
    }
  })));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeLighting.tsx

function VolumeLighting({
  servicesManager,
  commandsManager,
  viewportId
}) {
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const [ambient, setAmbient] = (0,react.useState)(null);
  const [diffuse, setDiffuse] = (0,react.useState)(null);
  const [specular, setSpecular] = (0,react.useState)(null);
  const onAmbientChange = (0,react.useCallback)(() => {
    commandsManager.runCommand('setVolumeLighting', {
      viewportId,
      options: {
        ambient
      }
    });
  }, [ambient, commandsManager, viewportId]);
  const onDiffuseChange = (0,react.useCallback)(() => {
    commandsManager.runCommand('setVolumeLighting', {
      viewportId,
      options: {
        diffuse
      }
    });
  }, [diffuse, commandsManager, viewportId]);
  const onSpecularChange = (0,react.useCallback)(() => {
    commandsManager.runCommand('setVolumeLighting', {
      viewportId,
      options: {
        specular
      }
    });
  }, [specular, commandsManager, viewportId]);
  const calculateBackground = value => {
    const percentage = (value - 0) / (1 - 0) * 100;
    return `linear-gradient(to right, #5acce6 0%, #5acce6 ${percentage}%, #3a3f99 ${percentage}%, #3a3f99 100%)`;
  };
  (0,react.useEffect)(() => {
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    const {
      actor
    } = viewport.getActors()[0];
    const ambient = actor.getProperty().getAmbient();
    const diffuse = actor.getProperty().getDiffuse();
    const specular = actor.getProperty().getSpecular();
    setAmbient(ambient);
    setDiffuse(diffuse);
    setSpecular(specular);
  }, [viewportId, cornerstoneViewportService]);
  return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex  w-full flex-row !items-center justify-between gap-[10px]"
  }, /*#__PURE__*/react.createElement("label", {
    className: "block  text-white",
    htmlFor: "ambient"
  }, "Ambient"), ambient !== null && /*#__PURE__*/react.createElement("input", {
    className: "bg-inputfield-main h-2 w-[120px] cursor-pointer appearance-none rounded-lg",
    value: ambient,
    onChange: e => {
      setAmbient(e.target.value);
      onAmbientChange();
    },
    id: "ambient",
    max: 1,
    min: 0,
    type: "range",
    step: 0.1,
    style: {
      background: calculateBackground(ambient),
      '--thumb-inner-color': '#5acce6',
      '--thumb-outer-color': '#090c29'
    }
  })), /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex  w-full flex-row !items-center justify-between gap-[10px]"
  }, /*#__PURE__*/react.createElement("label", {
    className: "block  text-white",
    htmlFor: "diffuse"
  }, "Diffuse"), diffuse !== null && /*#__PURE__*/react.createElement("input", {
    className: "bg-inputfield-main h-2 w-[120px] cursor-pointer appearance-none rounded-lg",
    value: diffuse,
    onChange: e => {
      setDiffuse(e.target.value);
      onDiffuseChange();
    },
    id: "diffuse",
    max: 1,
    min: 0,
    type: "range",
    step: 0.1,
    style: {
      background: calculateBackground(diffuse),
      '--thumb-inner-color': '#5acce6',
      '--thumb-outer-color': '#090c29'
    }
  })), /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex  w-full flex-row !items-center justify-between gap-[10px]"
  }, /*#__PURE__*/react.createElement("label", {
    className: "block  text-white",
    htmlFor: "specular"
  }, "Specular"), specular !== null && /*#__PURE__*/react.createElement("input", {
    className: "bg-inputfield-main h-2 w-[120px] cursor-pointer appearance-none rounded-lg",
    value: specular,
    onChange: e => {
      setSpecular(e.target.value);
      onSpecularChange();
    },
    id: "specular",
    max: 1,
    min: 0,
    type: "range",
    step: 0.1,
    style: {
      background: calculateBackground(specular),
      '--thumb-inner-color': '#5acce6',
      '--thumb-outer-color': '#090c29'
    }
  })));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeShade.tsx


function VolumeShade({
  commandsManager,
  viewportId,
  servicesManager
}) {
  const {
    cornerstoneViewportService
  } = servicesManager.services;
  const [shade, setShade] = (0,react.useState)(true);
  const [key, setKey] = (0,react.useState)(0);
  const onShadeChange = (0,react.useCallback)(checked => {
    commandsManager.runCommand('setVolumeLighting', {
      viewportId,
      options: {
        shade: checked
      }
    });
  }, [commandsManager, viewportId]);
  (0,react.useEffect)(() => {
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    const {
      actor
    } = viewport.getActors()[0];
    const shade = actor.getProperty().getShade();
    setShade(shade);
    setKey(key + 1);
  }, [viewportId, cornerstoneViewportService]);
  return /*#__PURE__*/react.createElement(ui_src/* SwitchButton */.L$, {
    key: key,
    label: "Shade",
    checked: shade,
    onChange: () => {
      setShade(!shade);
      onShadeChange(!shade);
    }
  });
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/VolumeRenderingOptions.tsx






function VolumeRenderingOptions({
  viewportId,
  commandsManager,
  volumeRenderingQualityRange,
  servicesManager
}) {
  return /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.ItemPanel */.se.cV, null, /*#__PURE__*/react.createElement(VolumeRenderingQuality, {
    viewportId: viewportId,
    commandsManager: commandsManager,
    servicesManager: servicesManager,
    volumeRenderingQualityRange: volumeRenderingQualityRange
  }), /*#__PURE__*/react.createElement(VolumeShift, {
    viewportId: viewportId,
    commandsManager: commandsManager,
    servicesManager: servicesManager
  }), /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item mt-2 flex !h-[20px] w-full justify-start"
  }, /*#__PURE__*/react.createElement("div", {
    className: "text-aqua-pale text-[13px]"
  }, "LIGHTING")), /*#__PURE__*/react.createElement("div", {
    className: "bg-primary-dark mt-1 mb-1 h-[2px] w-full"
  }), /*#__PURE__*/react.createElement("div", {
    className: "all-in-one-menu-item flex w-full justify-center"
  }, /*#__PURE__*/react.createElement(VolumeShade, {
    commandsManager: commandsManager,
    servicesManager: servicesManager,
    viewportId: viewportId
  })), /*#__PURE__*/react.createElement(VolumeLighting, {
    viewportId: viewportId,
    commandsManager: commandsManager,
    servicesManager: servicesManager
  }));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/WindowLevelActionMenu.tsx












const nonWLModalities = ['SR', 'SEG', 'SM', 'RTSTRUCT', 'RTPLAN', 'RTDOSE'];
function WindowLevelActionMenu({
  viewportId,
  element,
  presets,
  verticalDirection,
  horizontalDirection,
  commandsManager,
  servicesManager,
  colorbarProperties,
  displaySets,
  volumeRenderingPresets,
  volumeRenderingQualityRange
}) {
  const {
    colormaps,
    colorbarContainerPosition,
    colorbarInitialColormap,
    colorbarTickPosition,
    width: colorbarWidth
  } = colorbarProperties;
  const {
    colorbarService,
    cornerstoneViewportService
  } = servicesManager.services;
  const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
  const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
  const backgroundColor = viewportInfo.getViewportOptions().background;
  const isLight = backgroundColor ? dist_esm.utilities.isEqual(backgroundColor, [1, 1, 1]) : false;
  const {
    t
  } = (0,es/* useTranslation */.Bd)('WindowLevelActionMenu');
  const [viewportGrid] = (0,ui_src/* useViewportGrid */.ih)();
  const {
    activeViewportId
  } = viewportGrid;
  const [vpHeight, setVpHeight] = (0,react.useState)(element?.clientHeight);
  const [menuKey, setMenuKey] = (0,react.useState)(0);
  const [is3DVolume, setIs3DVolume] = (0,react.useState)(false);
  const onSetColorbar = (0,react.useCallback)(() => {
    setViewportColorbar(viewportId, displaySets, commandsManager, servicesManager, {
      colormaps,
      ticks: {
        position: colorbarTickPosition
      },
      width: colorbarWidth,
      position: colorbarContainerPosition,
      activeColormapName: colorbarInitialColormap
    });
  }, [commandsManager]);
  (0,react.useEffect)(() => {
    const newVpHeight = element?.clientHeight;
    if (vpHeight !== newVpHeight) {
      setVpHeight(newVpHeight);
    }
  }, [element, vpHeight]);
  (0,react.useEffect)(() => {
    if (!colorbarService.hasColorbar(viewportId)) {
      return;
    }
    window.setTimeout(() => {
      colorbarService.removeColorbar(viewportId);
      onSetColorbar();
    }, 0);
  }, [viewportId, displaySets, viewport]);
  (0,react.useEffect)(() => {
    setMenuKey(menuKey + 1);
    const viewport = cornerstoneViewportService.getCornerstoneViewport(viewportId);
    if (viewport instanceof dist_esm.VolumeViewport3D) {
      setIs3DVolume(true);
    } else {
      setIs3DVolume(false);
    }
  }, [displaySets, viewportId, presets, volumeRenderingQualityRange, volumeRenderingPresets, colorbarProperties, activeViewportId, viewportGrid]);
  return /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.IconMenu */.se.dd, {
    icon: "viewport-window-level",
    verticalDirection: verticalDirection,
    horizontalDirection: horizontalDirection,
    iconClassName: classnames_default()(
    // Visible on hover and for the active viewport
    activeViewportId === viewportId ? 'visible' : 'invisible group-hover/pane:visible', 'flex shrink-0 cursor-pointer rounded active:text-white text-primary-light', isLight ? ' hover:bg-secondary-dark' : 'hover:bg-secondary-light/60'),
    menuStyle: {
      maxHeight: vpHeight - 32,
      minWidth: 218
    },
    onVisibilityChange: () => {
      setVpHeight(element.clientHeight);
    },
    menuKey: menuKey
  }, /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.ItemPanel */.se.cV, null, !is3DVolume && /*#__PURE__*/react.createElement(Colorbar, {
    viewportId: viewportId,
    displaySets: displaySets.filter(ds => !nonWLModalities.includes(ds.Modality)),
    commandsManager: commandsManager,
    servicesManager: servicesManager,
    colorbarProperties: colorbarProperties
  }), colormaps && !is3DVolume && /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.SubMenu */.se.g8, {
    key: "colorLUTPresets",
    itemLabel: "Color LUT",
    itemIcon: "icon-color-lut"
  }, /*#__PURE__*/react.createElement(Colormap, {
    colormaps: colormaps,
    viewportId: viewportId,
    displaySets: displaySets.filter(ds => !nonWLModalities.includes(ds.Modality)),
    commandsManager: commandsManager,
    servicesManager: servicesManager
  })), presets && presets.length > 0 && !is3DVolume && /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.SubMenu */.se.g8, {
    key: "windowLevelPresets",
    itemLabel: t('Modality Window Presets'),
    itemIcon: "viewport-window-level"
  }, /*#__PURE__*/react.createElement(WindowLevel, {
    viewportId: viewportId,
    commandsManager: commandsManager,
    presets: presets
  })), volumeRenderingPresets && is3DVolume && /*#__PURE__*/react.createElement(VolumeRenderingPresets, {
    servicesManager: servicesManager,
    viewportId: viewportId,
    commandsManager: commandsManager,
    volumeRenderingPresets: volumeRenderingPresets
  }), volumeRenderingQualityRange && is3DVolume && /*#__PURE__*/react.createElement(ui_src/* AllInOneMenu.SubMenu */.se.g8, {
    itemLabel: "Rendering Options"
  }, /*#__PURE__*/react.createElement(VolumeRenderingOptions, {
    viewportId: viewportId,
    commandsManager: commandsManager,
    volumeRenderingQualityRange: volumeRenderingQualityRange,
    servicesManager: servicesManager
  }))));
}
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/WindowLevelActionMenu/getWindowLevelActionMenu.tsx


function getWindowLevelActionMenu({
  viewportId,
  element,
  displaySets,
  servicesManager,
  commandsManager,
  verticalDirection,
  horizontalDirection
}) {
  const {
    customizationService
  } = servicesManager.services;
  const {
    presets
  } = customizationService.get('cornerstone.windowLevelPresets');
  const colorbarProperties = customizationService.get('cornerstone.colorbar');
  const {
    volumeRenderingPresets,
    volumeRenderingQualityRange
  } = customizationService.get('cornerstone.3dVolumeRendering');
  const displaySetPresets = displaySets.filter(displaySet => presets[displaySet.Modality]).map(displaySet => {
    return {
      [displaySet.Modality]: presets[displaySet.Modality]
    };
  });
  const modalities = displaySets.map(displaySet => displaySet.Modality).filter(modality => !nonWLModalities.includes(modality));
  if (modalities.length === 0) {
    return null;
  }
  return /*#__PURE__*/react.createElement(WindowLevelActionMenu, {
    viewportId: viewportId,
    element: element,
    presets: displaySetPresets,
    verticalDirection: verticalDirection,
    horizontalDirection: horizontalDirection,
    commandsManager: commandsManager,
    servicesManager: servicesManager,
    colorbarProperties: colorbarProperties,
    displaySets: displaySets,
    volumeRenderingPresets: volumeRenderingPresets,
    volumeRenderingQualityRange: volumeRenderingQualityRange
  });
}
// EXTERNAL MODULE: ../../ui-next/src/index.ts + 2483 modules
var ui_next_src = __webpack_require__(35570);
// EXTERNAL MODULE: ../../../node_modules/@cornerstonejs/tools/dist/esm/enums/index.js + 2 modules
var enums = __webpack_require__(99737);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/ViewportDataOverlaySettingMenu/ViewportSegmentationMenu.tsx



function ViewportSegmentationMenu({
  viewportId,
  servicesManager
}) {
  const {
    segmentationService
  } = servicesManager.services;
  const [activeSegmentations, setActiveSegmentations] = (0,react.useState)([]);
  const [availableSegmentations, setAvailableSegmentations] = (0,react.useState)([]);
  (0,react.useEffect)(() => {
    const updateSegmentations = () => {
      const active = segmentationService.getSegmentationRepresentations(viewportId);
      setActiveSegmentations(active);
      const all = segmentationService.getSegmentations();
      const available = all.filter(seg => !active.some(activeSeg => activeSeg.segmentationId === seg.segmentationId));
      setAvailableSegmentations(available);
    };
    updateSegmentations();
    const subscriptions = [segmentationService.EVENTS.SEGMENTATION_MODIFIED, segmentationService.EVENTS.SEGMENTATION_REMOVED, segmentationService.EVENTS.SEGMENTATION_REPRESENTATION_MODIFIED].map(event => segmentationService.subscribe(event, updateSegmentations));
    return () => {
      subscriptions.forEach(subscription => subscription.unsubscribe());
    };
  }, [segmentationService, viewportId]);
  const toggleSegmentationRepresentationVisibility = (segmentationId, type = enums.SegmentationRepresentations.Labelmap) => {
    segmentationService.toggleSegmentationRepresentationVisibility(viewportId, {
      segmentationId,
      type
    });
  };
  const addSegmentationToViewport = segmentationId => {
    segmentationService.addSegmentationRepresentation(viewportId, {
      segmentationId
    });
  };
  const removeSegmentationFromViewport = segmentationId => {
    segmentationService.removeSegmentationRepresentations(viewportId, {
      segmentationId
    });
  };
  return /*#__PURE__*/react.createElement("div", {
    className: "bg-muted flex h-full w-[262px] flex-col rounded p-3"
  }, /*#__PURE__*/react.createElement("span", {
    className: "text-muted-foreground mb-2 text-xs font-semibold"
  }, "Current Viewport"), /*#__PURE__*/react.createElement("ul", {
    className: "space-y-1"
  }, activeSegmentations.map(segmentation => /*#__PURE__*/react.createElement("li", {
    key: segmentation.id,
    className: "flex items-center text-sm"
  }, /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    variant: "ghost",
    size: "icon",
    className: "text-muted-foreground mr-2",
    onClick: () => removeSegmentationFromViewport(segmentation.segmentationId)
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Minus, {
    className: "h-6 w-6"
  })), /*#__PURE__*/react.createElement("span", {
    className: "text-foreground flex-grow"
  }, segmentation.label), segmentation.visible ? /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    variant: "ghost",
    size: "icon",
    className: "text-muted-foreground",
    onClick: () => toggleSegmentationRepresentationVisibility(segmentation.segmentationId, segmentation.type)
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Hide, {
    className: "h-6 w-6"
  })) : /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    variant: "ghost",
    size: "icon",
    className: "text-muted-foreground",
    onClick: () => toggleSegmentationRepresentationVisibility(segmentation.segmentationId, segmentation.type)
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Show, {
    className: "h-6 w-6"
  }))))), availableSegmentations.length > 0 && /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement(ui_next_src/* Separator */.wv, {
    className: "bg-input mb-3"
  }), /*#__PURE__*/react.createElement("span", {
    className: "text-muted-foreground mb-2 text-xs font-semibold"
  }, "Available"), /*#__PURE__*/react.createElement("ul", {
    className: "space-y-1"
  }, availableSegmentations.map(({
    segmentationId,
    label
  }) => /*#__PURE__*/react.createElement("li", {
    key: segmentationId,
    className: "flex items-center text-sm"
  }, /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    variant: "ghost",
    size: "icon",
    className: "text-muted-foreground mr-2",
    onClick: () => addSegmentationToViewport(segmentationId)
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.Plus, {
    className: "h-6 w-6"
  })), /*#__PURE__*/react.createElement("span", {
    className: "text-foreground/60"
  }, label))))));
}
/* harmony default export */ const ViewportDataOverlaySettingMenu_ViewportSegmentationMenu = (ViewportSegmentationMenu);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/hooks/useSegmentations.ts
var useSegmentations = __webpack_require__(73421);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/ViewportDataOverlaySettingMenu/ViewportSegmentationMenuWrapper.tsx





function ViewportSegmentationMenuWrapper({
  viewportId,
  displaySets,
  servicesManager,
  commandsManager,
  location
}) {
  const {
    viewportActionCornersService,
    viewportGridService
  } = servicesManager.services;
  const segmentations = (0,useSegmentations/* useSegmentations */.j)({
    servicesManager
  });
  const activeViewportId = viewportGridService.getActiveViewportId();
  const isActiveViewport = viewportId === activeViewportId;
  const {
    align,
    side
  } = getAlignAndSide(viewportActionCornersService, location);
  if (!segmentations?.length) {
    return null;
  }
  return /*#__PURE__*/react.createElement(ui_next_src/* Popover */.AM, null, /*#__PURE__*/react.createElement(ui_next_src/* PopoverTrigger */.Wv, {
    asChild: true,
    className: "flex items-center justify-center"
  }, /*#__PURE__*/react.createElement(ui_next_src/* Button */.$n, {
    variant: "ghost",
    size: "icon"
  }, /*#__PURE__*/react.createElement(ui_next_src/* Icons */.FI.ViewportViews, {
    className: classnames_default()('text-highlight', isActiveViewport ? 'visible' : 'invisible group-hover/pane:visible')
  }))), /*#__PURE__*/react.createElement(ui_next_src/* PopoverContent */.hl, {
    className: "border-none bg-transparent p-0 shadow-none",
    side: side,
    align: align,
    alignOffset: -15,
    sideOffset: 5
  }, /*#__PURE__*/react.createElement(ViewportDataOverlaySettingMenu_ViewportSegmentationMenu, {
    className: "w-full",
    viewportId: viewportId,
    displaySets: displaySets,
    servicesManager: servicesManager,
    commandsManager: commandsManager
  })));
}
const getAlignAndSide = (viewportActionCornersService, location) => {
  const ViewportActionCornersLocations = viewportActionCornersService.LOCATIONS;
  switch (location) {
    case ViewportActionCornersLocations.topLeft:
      return {
        align: 'start',
        side: 'bottom'
      };
    case ViewportActionCornersLocations.topRight:
      return {
        align: 'end',
        side: 'bottom'
      };
    case ViewportActionCornersLocations.bottomLeft:
      return {
        align: 'start',
        side: 'top'
      };
    case ViewportActionCornersLocations.bottomRight:
      return {
        align: 'end',
        side: 'top'
      };
    default:
      console.debug('Unknown location, defaulting to bottom-start');
      return {
        align: 'start',
        side: 'bottom'
      };
  }
};
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/components/ViewportDataOverlaySettingMenu/index.tsx


function getViewportDataOverlaySettingsMenu(props) {
  return /*#__PURE__*/react.createElement(ViewportSegmentationMenuWrapper, props);
}
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/stores/usePositionPresentationStore.ts
var usePositionPresentationStore = __webpack_require__(44646);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/stores/useLutPresentationStore.ts
var useLutPresentationStore = __webpack_require__(10182);
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/stores/useSegmentationPresentationStore.ts + 1 modules
var useSegmentationPresentationStore = __webpack_require__(2847);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/utils/presentations/getViewportPresentations.ts



function getViewportPresentations(viewportId, viewportOptions) {
  const {
    lutPresentationStore
  } = useLutPresentationStore/* useLutPresentationStore */.I.getState();
  const {
    positionPresentationStore
  } = usePositionPresentationStore/* usePositionPresentationStore */.q.getState();
  const {
    segmentationPresentationStore
  } = useSegmentationPresentationStore/* useSegmentationPresentationStore */.v.getState();

  // NOTE: this is the new viewport state, we should not get the presentationIds from the cornerstoneViewportService
  // since that has the old viewport state
  const {
    presentationIds
  } = viewportOptions;
  if (!presentationIds) {
    return {
      positionPresentation: null,
      lutPresentation: null,
      segmentationPresentation: null
    };
  }
  const {
    lutPresentationId,
    positionPresentationId,
    segmentationPresentationId
  } = presentationIds;
  return {
    positionPresentation: positionPresentationStore[positionPresentationId],
    lutPresentation: lutPresentationStore[lutPresentationId],
    segmentationPresentation: segmentationPresentationStore[segmentationPresentationId]
  };
}
// EXTERNAL MODULE: ../../../extensions/cornerstone/src/stores/useSynchronizersStore.ts
var useSynchronizersStore = __webpack_require__(68578);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/utils/ActiveViewportBehavior.tsx

const MODALITIES_REQUIRING_CINE_AUTO_MOUNT = ['OT', 'US'];
const ActiveViewportBehavior = /*#__PURE__*/(0,react.memo)(({
  servicesManager,
  viewportId
}) => {
  const {
    displaySetService,
    cineService,
    viewportGridService,
    customizationService
  } = servicesManager.services;
  const [activeViewportId, setActiveViewportId] = (0,react.useState)(viewportId);
  (0,react.useEffect)(() => {
    const subscription = viewportGridService.subscribe(viewportGridService.EVENTS.ACTIVE_VIEWPORT_ID_CHANGED, ({
      viewportId
    }) => setActiveViewportId(viewportId));
    return () => subscription.unsubscribe();
  }, [viewportId, viewportGridService]);
  (0,react.useEffect)(() => {
    if (cineService.isViewportCineClosed(activeViewportId)) {
      return;
    }
    const displaySetInstanceUIDs = viewportGridService.getDisplaySetsUIDsForViewport(activeViewportId);
    if (!displaySetInstanceUIDs) {
      return;
    }
    const displaySets = displaySetInstanceUIDs.map(uid => displaySetService.getDisplaySetByUID(uid));
    if (!displaySets.length) {
      return;
    }
    const modalities = displaySets.map(displaySet => displaySet?.Modality);
    const {
      modalities: sourceModalities
    } = customizationService.getModeCustomization('autoCineModalities', {
      id: 'autoCineModalities',
      modalities: MODALITIES_REQUIRING_CINE_AUTO_MOUNT
    });
    const requiresCine = modalities.some(modality => sourceModalities.includes(modality));
    if (requiresCine && !cineService.getState().isCineEnabled) {
      cineService.setIsCineEnabled(true);
    }
  }, [activeViewportId, cineService, viewportGridService, displaySetService, customizationService]);
  return null;
}, arePropsEqual);
ActiveViewportBehavior.displayName = 'ActiveViewportBehavior';
function arePropsEqual(prevProps, nextProps) {
  return prevProps.viewportId === nextProps.viewportId && prevProps.servicesManager === nextProps.servicesManager;
}
/* harmony default export */ const utils_ActiveViewportBehavior = (ActiveViewportBehavior);
;// CONCATENATED MODULE: ../../../extensions/cornerstone/src/Viewport/OHIFCornerstoneViewport.tsx

















const STACK = 'stack';

/**
 * Caches the jump to measurement operation, so that if display set is shown,
 * it can jump to the measurement.
 */
let cacheJumpToMeasurementEvent;

// Todo: This should be done with expose of internal API similar to react-vtkjs-viewport
// Then we don't need to worry about the re-renders if the props change.
const OHIFCornerstoneViewport = /*#__PURE__*/react.memo(props => {
  const {
    displaySets,
    dataSource,
    viewportOptions,
    displaySetOptions,
    servicesManager,
    commandsManager,
    onElementEnabled,
    // eslint-disable-next-line react/prop-types
    onElementDisabled,
    isJumpToMeasurementDisabled = false,
    // Note: you SHOULD NOT use the initialImageIdOrIndex for manipulation
    // of the imageData in the OHIFCornerstoneViewport. This prop is used
    // to set the initial state of the viewport's first image to render
    // eslint-disable-next-line react/prop-types
    initialImageIndex,
    // if the viewport is part of a hanging protocol layout
    // we should not really rely on the old synchronizers and
    // you see below we only rehydrate the synchronizers if the viewport
    // is not part of the hanging protocol layout. HPs should
    // define their own synchronizers. Since the synchronizers are
    // viewportId dependent and
    // eslint-disable-next-line react/prop-types
    isHangingProtocolLayout
  } = props;
  const viewportId = viewportOptions.viewportId;
  if (!viewportId) {
    throw new Error('Viewport ID is required');
  }

  // Make sure displaySetOptions has one object per displaySet
  while (displaySetOptions.length < displaySets.length) {
    displaySetOptions.push({});
  }

  // Since we only have support for dynamic data in volume viewports, we should
  // handle this case here and set the viewportType to volume if any of the
  // displaySets are dynamic volumes
  viewportOptions.viewportType = displaySets.some(ds => ds.isDynamicVolume && ds.isReconstructable) ? 'volume' : viewportOptions.viewportType;
  const [scrollbarHeight, setScrollbarHeight] = (0,react.useState)('100px');
  const [enabledVPElement, setEnabledVPElement] = (0,react.useState)(null);
  const elementRef = (0,react.useRef)();
  const [appConfig] = (0,state_0/* useAppConfig */.r)();
  const {
    displaySetService,
    toolbarService,
    toolGroupService,
    syncGroupService,
    cornerstoneViewportService,
    segmentationService,
    cornerstoneCacheService,
    viewportActionCornersService
  } = servicesManager.services;
  const [viewportDialogState] = (0,ui_src/* useViewportDialog */.OR)();
  // useCallback for scroll bar height calculation
  const setImageScrollBarHeight = (0,react.useCallback)(() => {
    const scrollbarHeight = `${elementRef.current.clientHeight - 40}px`;
    setScrollbarHeight(scrollbarHeight);
  }, [elementRef]);

  // useCallback for onResize
  const onResize = (0,react.useCallback)(() => {
    if (elementRef.current) {
      cornerstoneViewportService.resize();
      setImageScrollBarHeight();
    }
  }, [elementRef]);
  const cleanUpServices = (0,react.useCallback)(viewportInfo => {
    const renderingEngineId = viewportInfo.getRenderingEngineId();
    const syncGroups = viewportInfo.getSyncGroups();
    toolGroupService.removeViewportFromToolGroup(viewportId, renderingEngineId);
    syncGroupService.removeViewportFromSyncGroup(viewportId, renderingEngineId, syncGroups);
    segmentationService.clearSegmentationRepresentations(viewportId);
    viewportActionCornersService.clear(viewportId);
  }, [viewportId, segmentationService, syncGroupService, toolGroupService, viewportActionCornersService]);
  const elementEnabledHandler = (0,react.useCallback)(evt => {
    // check this is this element reference and return early if doesn't match
    if (evt.detail.element !== elementRef.current) {
      return;
    }
    const {
      viewportId,
      element
    } = evt.detail;
    const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
    (0,state/* setEnabledElement */.ye)(viewportId, element);
    setEnabledVPElement(element);
    const renderingEngineId = viewportInfo.getRenderingEngineId();
    const toolGroupId = viewportInfo.getToolGroupId();
    const syncGroups = viewportInfo.getSyncGroups();
    toolGroupService.addViewportToToolGroup(viewportId, renderingEngineId, toolGroupId);
    syncGroupService.addViewportToSyncGroup(viewportId, renderingEngineId, syncGroups);

    // we don't need reactivity here so just use state
    const {
      synchronizersStore
    } = useSynchronizersStore/* useSynchronizersStore */.U.getState();
    if (synchronizersStore?.[viewportId]?.length && !isHangingProtocolLayout) {
      // If the viewport used to have a synchronizer, re apply it again
      _rehydrateSynchronizers(viewportId, syncGroupService);
    }
    if (onElementEnabled && typeof onElementEnabled === 'function') {
      onElementEnabled(evt);
    }
  }, [viewportId, onElementEnabled, toolGroupService]);

  // disable the element upon unmounting
  (0,react.useEffect)(() => {
    cornerstoneViewportService.enableViewport(viewportId, elementRef.current);
    dist_esm.eventTarget.addEventListener(dist_esm.Enums.Events.ELEMENT_ENABLED, elementEnabledHandler);
    setImageScrollBarHeight();
    return () => {
      const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
      if (!viewportInfo) {
        return;
      }
      cornerstoneViewportService.storePresentation({
        viewportId
      });

      // This should be done after the store presentation since synchronizers
      // will get cleaned up and they need the viewportInfo to be present
      cleanUpServices(viewportInfo);
      if (onElementDisabled && typeof onElementDisabled === 'function') {
        onElementDisabled(viewportInfo);
      }
      cornerstoneViewportService.disableElement(viewportId);
      dist_esm.eventTarget.removeEventListener(dist_esm.Enums.Events.ELEMENT_ENABLED, elementEnabledHandler);
    };
  }, []);

  // subscribe to displaySet metadata invalidation (updates)
  // Currently, if the metadata changes we need to re-render the display set
  // for it to take effect in the viewport. As we deal with scaling in the loading,
  // we need to remove the old volume from the cache, and let the
  // viewport to re-add it which will use the new metadata. Otherwise, the
  // viewport will use the cached volume and the new metadata will not be used.
  // Note: this approach does not actually end of sending network requests
  // and it uses the network cache
  (0,react.useEffect)(() => {
    const {
      unsubscribe
    } = displaySetService.subscribe(displaySetService.EVENTS.DISPLAY_SET_SERIES_METADATA_INVALIDATED, async ({
      displaySetInstanceUID: invalidatedDisplaySetInstanceUID,
      invalidateData
    }) => {
      if (!invalidateData) {
        return;
      }
      const viewportInfo = cornerstoneViewportService.getViewportInfo(viewportId);
      if (viewportInfo.hasDisplaySet(invalidatedDisplaySetInstanceUID)) {
        const viewportData = viewportInfo.getViewportData();
        const newViewportData = await cornerstoneCacheService.invalidateViewportData(viewportData, invalidatedDisplaySetInstanceUID, dataSource, displaySetService);
        const keepCamera = true;
        cornerstoneViewportService.updateViewport(viewportId, newViewportData, keepCamera);
      }
    });
    return () => {
      unsubscribe();
    };
  }, [viewportId]);
  (0,react.useEffect)(() => {
    // handle the default viewportType to be stack
    if (!viewportOptions.viewportType) {
      viewportOptions.viewportType = STACK;
    }
    const loadViewportData = async () => {
      const viewportData = await cornerstoneCacheService.createViewportData(displaySets, viewportOptions, dataSource, initialImageIndex);
      const presentations = getViewportPresentations(viewportId, viewportOptions);
      let measurement;
      if (cacheJumpToMeasurementEvent?.viewportId === viewportId) {
        measurement = cacheJumpToMeasurementEvent.measurement;
        // Delete the position presentation so that viewport navigates direct
        presentations.positionPresentation = null;
        cacheJumpToMeasurementEvent = null;
      }

      // Note: This is a hack to get the grid to re-render the OHIFCornerstoneViewport component
      // Used for segmentation hydration right now, since the logic to decide whether
      // a viewport needs to render a segmentation lives inside the CornerstoneViewportService
      // so we need to re-render (force update via change of the needsRerendering) so that React
      // does the diffing and decides we should render this again (although the id and element has not changed)
      // so that the CornerstoneViewportService can decide whether to render the segmentation or not. Not that we reached here we can turn it off.
      if (viewportOptions.needsRerendering) {
        viewportOptions.needsRerendering = false;
      }
      cornerstoneViewportService.setViewportData(viewportId, viewportData, viewportOptions, displaySetOptions, presentations);
      if (measurement) {
        esm.annotation.selection.setAnnotationSelected(measurement.uid);
      }
    };
    loadViewportData();
  }, [viewportOptions, displaySets, dataSource]);

  /**
   * There are two scenarios for jump to click
   * 1. Current viewports contain the displaySet that the annotation was drawn on
   * 2. Current viewports don't contain the displaySet that the annotation was drawn on
   * and we need to change the viewports displaySet for jumping.
   * Since measurement_jump happens via events and listeners, the former case is handled
   * by the measurement_jump direct callback, but the latter case is handled first by
   * the viewportGrid to set the correct displaySet on the viewport, AND THEN we check
   * the cache for jumping to see if there is any jump queued, then we jump to the correct slice.
   */
  (0,react.useEffect)(() => {
    if (isJumpToMeasurementDisabled) {
      return;
    }
    const unsubscribeFromJumpToMeasurementEvents = _subscribeToJumpToMeasurementEvents(elementRef, viewportId, servicesManager);
    _checkForCachedJumpToMeasurementEvents(elementRef, viewportId, displaySets, servicesManager);
    return () => {
      unsubscribeFromJumpToMeasurementEvents();
    };
  }, [displaySets, elementRef, viewportId, isJumpToMeasurementDisabled, servicesManager]);

  // Set up the window level action menu in the viewport action corners.
  (0,react.useEffect)(() => {
    // Doing an === check here because the default config value when not set is true
    if (appConfig.addWindowLevelActionMenu === false) {
      return;
    }
    const location = viewportActionCornersService.LOCATIONS.topRight;

    // TODO: In the future we should consider using the customization service
    // to determine if and in which corner various action components should go.
    viewportActionCornersService.addComponent({
      viewportId,
      id: 'windowLevelActionMenu',
      component: getWindowLevelActionMenu({
        viewportId,
        element: elementRef.current,
        displaySets,
        servicesManager,
        commandsManager,
        location,
        verticalDirection: ui_src/* AllInOneMenu.VerticalDirection */.se.mq.TopToBottom,
        horizontalDirection: ui_src/* AllInOneMenu.HorizontalDirection */.se.Iu.RightToLeft
      }),
      location
    });
    viewportActionCornersService.addComponent({
      viewportId,
      id: 'segmentation',
      component: getViewportDataOverlaySettingsMenu({
        viewportId,
        element: elementRef.current,
        displaySets,
        servicesManager,
        commandsManager,
        location
      }),
      location
    });
  }, [displaySets, viewportId, viewportActionCornersService, servicesManager, commandsManager, appConfig]);
  const {
    ref: resizeRef
  } = (0,index_esm/* useResizeDetector */.u)({
    onResize
  });
  return /*#__PURE__*/react.createElement(react.Fragment, null, /*#__PURE__*/react.createElement("div", {
    className: "viewport-wrapper"
  }, /*#__PURE__*/react.createElement("div", {
    className: "cornerstone-viewport-element",
    style: {
      height: '100%',
      width: '100%'
    },
    onContextMenu: e => e.preventDefault(),
    onMouseDown: e => e.preventDefault(),
    ref: el => {
      resizeRef.current = el;
      elementRef.current = el;
    }
  }), /*#__PURE__*/react.createElement(Overlays_CornerstoneOverlays, {
    viewportId: viewportId,
    toolBarService: toolbarService,
    element: elementRef.current,
    scrollbarHeight: scrollbarHeight,
    servicesManager: servicesManager
  }), /*#__PURE__*/react.createElement(components_CinePlayer, {
    enabledVPElement: enabledVPElement,
    viewportId: viewportId,
    servicesManager: servicesManager
  }), /*#__PURE__*/react.createElement(utils_ActiveViewportBehavior, {
    viewportId: viewportId,
    servicesManager: servicesManager
  })), /*#__PURE__*/react.createElement("div", {
    className: "absolute top-[24px] w-full"
  }, viewportDialogState.viewportId === viewportId && /*#__PURE__*/react.createElement(ui_src/* Notification */.Eg, {
    id: "viewport-notification",
    message: viewportDialogState.message,
    type: viewportDialogState.type,
    actions: viewportDialogState.actions,
    onSubmit: viewportDialogState.onSubmit,
    onOutsideClick: viewportDialogState.onOutsideClick,
    onKeyPress: viewportDialogState.onKeyPress
  })), /*#__PURE__*/react.createElement(components_OHIFViewportActionCorners, {
    viewportId: viewportId
  }));
}, areEqual);
function _subscribeToJumpToMeasurementEvents(elementRef, viewportId, servicesManager) {
  const {
    measurementService,
    cornerstoneViewportService
  } = servicesManager.services;
  const {
    unsubscribe
  } = measurementService.subscribe(src/* MeasurementService */.C5.EVENTS.JUMP_TO_MEASUREMENT_VIEWPORT, props => {
    cacheJumpToMeasurementEvent = props;
    const {
      viewportId: jumpId,
      measurement,
      isConsumed
    } = props;
    if (!measurement || isConsumed) {
      return;
    }
    if (cacheJumpToMeasurementEvent.cornerstoneViewport === undefined) {
      // Decide on which viewport should handle this
      cacheJumpToMeasurementEvent.cornerstoneViewport = cornerstoneViewportService.getViewportIdToJump(jumpId, {
        displaySetInstanceUID: measurement.displaySetInstanceUID,
        ...measurement.metadata,
        referencedImageId: measurement.referencedImageId || measurement.metadata?.referencedImageId
      });
    }
    if (cacheJumpToMeasurementEvent.cornerstoneViewport !== viewportId) {
      return;
    }
    _jumpToMeasurement(measurement, elementRef, viewportId, servicesManager);
  });
  return unsubscribe;
}

// Check if there is a queued jumpToMeasurement event
function _checkForCachedJumpToMeasurementEvents(elementRef, viewportId, displaySets, servicesManager) {
  if (!cacheJumpToMeasurementEvent) {
    return;
  }
  if (cacheJumpToMeasurementEvent.isConsumed) {
    cacheJumpToMeasurementEvent = null;
    return;
  }
  const displaysUIDs = displaySets.map(displaySet => displaySet.displaySetInstanceUID);
  if (!displaysUIDs?.length) {
    return;
  }

  // Jump to measurement if the measurement exists
  const {
    measurement
  } = cacheJumpToMeasurementEvent;
  if (measurement && elementRef) {
    if (displaysUIDs.includes(measurement?.displaySetInstanceUID)) {
      _jumpToMeasurement(measurement, elementRef, viewportId, servicesManager);
    }
  }
}
function _jumpToMeasurement(measurement, targetElementRef, viewportId, servicesManager) {
  const {
    viewportGridService
  } = servicesManager.services;
  const targetElement = targetElementRef.current;

  // Todo: setCornerstoneMeasurementActive should be handled by the toolGroupManager
  //  to set it properly
  // setCornerstoneMeasurementActive(measurement);

  viewportGridService.setActiveViewportId(viewportId);
  const enabledElement = (0,dist_esm.getEnabledElement)(targetElement);
  if (enabledElement) {
    // See how the jumpToSlice() of Cornerstone3D deals with imageIdx param.
    const viewport = enabledElement.viewport;
    const {
      metadata
    } = measurement;
    if (!viewport.isReferenceViewable(metadata, {
      withNavigation: true,
      withOrientation: true
    })) {
      console.log("Reference isn't viewable, postponing until updated");
      return;
    }
    viewport.setViewReference(metadata);
    esm.annotation.selection.setAnnotationSelected(measurement.uid);
    // Jump to measurement consumed, remove.
    cacheJumpToMeasurementEvent?.consume?.();
    cacheJumpToMeasurementEvent = null;
  }
}
function _rehydrateSynchronizers(viewportId, syncGroupService) {
  const {
    synchronizersStore
  } = useSynchronizersStore/* useSynchronizersStore */.U.getState();
  const synchronizers = synchronizersStore[viewportId];
  if (!synchronizers) {
    return;
  }
  synchronizers.forEach(synchronizerObj => {
    if (!synchronizerObj.id) {
      return;
    }
    const {
      id,
      sourceViewports,
      targetViewports
    } = synchronizerObj;
    const synchronizer = syncGroupService.getSynchronizer(id);
    if (!synchronizer) {
      return;
    }
    const sourceViewportInfo = sourceViewports.find(sourceViewport => sourceViewport.viewportId === viewportId);
    const targetViewportInfo = targetViewports.find(targetViewport => targetViewport.viewportId === viewportId);
    const isSourceViewportInSynchronizer = synchronizer.getSourceViewports().find(sourceViewport => sourceViewport.viewportId === viewportId);
    const isTargetViewportInSynchronizer = synchronizer.getTargetViewports().find(targetViewport => targetViewport.viewportId === viewportId);

    // if the viewport was previously a source viewport, add it again
    if (sourceViewportInfo && !isSourceViewportInSynchronizer) {
      synchronizer.addSource({
        viewportId: sourceViewportInfo.viewportId,
        renderingEngineId: sourceViewportInfo.renderingEngineId
      });
    }

    // if the viewport was previously a target viewport, add it again
    if (targetViewportInfo && !isTargetViewportInSynchronizer) {
      synchronizer.addTarget({
        viewportId: targetViewportInfo.viewportId,
        renderingEngineId: targetViewportInfo.renderingEngineId
      });
    }
  });
}

// Component displayName
OHIFCornerstoneViewport.displayName = 'OHIFCornerstoneViewport';
function areEqual(prevProps, nextProps) {
  if (nextProps.needsRerendering) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: needsRerendering');
    return false;
  }
  if (prevProps.displaySets.length !== nextProps.displaySets.length) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: displaySets length change');
    return false;
  }
  if (prevProps.viewportOptions.orientation !== nextProps.viewportOptions.orientation) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: orientation change');
    return false;
  }
  if (prevProps.viewportOptions.toolGroupId !== nextProps.viewportOptions.toolGroupId) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: toolGroupId change');
    return false;
  }
  if (nextProps.viewportOptions.viewportType && prevProps.viewportOptions.viewportType !== nextProps.viewportOptions.viewportType) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: viewportType change');
    return false;
  }
  if (nextProps.viewportOptions.needsRerendering) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: viewportOptions.needsRerendering');
    return false;
  }
  const prevDisplaySets = prevProps.displaySets;
  const nextDisplaySets = nextProps.displaySets;
  if (prevDisplaySets.length !== nextDisplaySets.length) {
    console.debug('OHIFCornerstoneViewport: Rerender caused by: displaySets length mismatch');
    return false;
  }
  for (let i = 0; i < prevDisplaySets.length; i++) {
    const prevDisplaySet = prevDisplaySets[i];
    const foundDisplaySet = nextDisplaySets.find(nextDisplaySet => nextDisplaySet.displaySetInstanceUID === prevDisplaySet.displaySetInstanceUID);
    if (!foundDisplaySet) {
      console.debug('OHIFCornerstoneViewport: Rerender caused by: displaySet not found');
      return false;
    }

    // check they contain the same image
    if (foundDisplaySet.images?.length !== prevDisplaySet.images?.length) {
      console.debug('OHIFCornerstoneViewport: Rerender caused by: images length mismatch');
      return false;
    }

    // check if their imageIds are the same
    if (foundDisplaySet.images?.length) {
      for (let j = 0; j < foundDisplaySet.images.length; j++) {
        if (foundDisplaySet.images[j].imageId !== prevDisplaySet.images[j].imageId) {
          console.debug('OHIFCornerstoneViewport: Rerender caused by: imageId mismatch');
          return false;
        }
      }
    }
  }
  return true;
}

// Helper function to check if display sets have changed
function haveDisplaySetsChanged(prevDisplaySets, currentDisplaySets) {
  if (prevDisplaySets.length !== currentDisplaySets.length) {
    return true;
  }
  return currentDisplaySets.some((currentDS, index) => {
    const prevDS = prevDisplaySets[index];
    return currentDS.displaySetInstanceUID !== prevDS.displaySetInstanceUID;
  });
}
/* harmony default export */ const Viewport_OHIFCornerstoneViewport = (OHIFCornerstoneViewport);

/***/ })

}]);