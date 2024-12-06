"use strict";
(self["webpackChunkpyams_content_themes"] = self["webpackChunkpyams_content_themes"] || []).push([["src_pyams_content_themes_resources_src_js__gis_js"],{

/***/ "./src/pyams_content_themes/resources/src/js/_gis.js":
/*!***********************************************************!*\
  !*** ./src/pyams_content_themes/resources/src/js/_gis.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./_utils */ "./src/pyams_content_themes/resources/src/js/_utils.js");
/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), !0).forEach(function (r) { _defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function _defineProperty(obj, key, value) { key = _toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }

var createMap = function createMap(map, config, options, callback) {
  return new Promise(function (resolve, reject) {
    var data = map.data();
    var settings = {
      preferCanvas: data.mapLeafletPreferCanvas || false,
      attributionControl: data.mapLeafletAttributionControl === undefined ? config.attributionControl : data.mapLeafletAttributionControl,
      zoomControl: data.mapLeafletZoomControl === undefined ? config.zoomControl : data.mapLeafletZoomControl,
      fullscreenControl: data.mapLeafletFullscreen === undefined ? config.fullscreenControl && {
        pseudoFullscreen: true
      } || null : data.mapLeafletFullscreen,
      crs: data.mapLeafletCrs || _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject(config.crs) || L.CRS.EPSG3857,
      center: data.mapLeafletCenter || config.center,
      zoom: data.mapLeafletZoom || config.zoom,
      gestureHandling: data.mapLeafletWheelZoom === undefined ? !config.scrollWheelZoom : data.mapLeafletWheelZoom,
      keyboard: data.mapLeafletKeyboard === undefined ? config.keyboard && !L.Browser.mobile : data.amsLeafletKeyboard
    };
    settings = $.extend({}, settings, options);
    map.trigger('map.init', [map, settings, config]);
    var leafmap = L.map(map.attr('id'), settings),
      layersConfig = [];
    if (config.layers) {
      var _iterator = _createForOfIteratorHelper(config.layers),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var layerConfig = _step.value;
          map.trigger('map.layer.init', [map, layerConfig]);
          layersConfig.push(PyAMS_GIS.getLayer(map, leafmap, layerConfig));
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
    } else {
      layersConfig.push(L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        name: 'osm',
        title: 'OpenStreetMap',
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }));
    }
    $.when.apply($, layersConfig).then(function () {
      for (var _len = arguments.length, layers = new Array(_len), _key = 0; _key < _len; _key++) {
        layers[_key] = arguments[_key];
      }
      for (var _i = 0, _layers = layers; _i < _layers.length; _i++) {
        var layer = _layers[_i];
        layer.addTo(leafmap);
      }
      if (config.zoomControl && data.mapLeafletHideZoomControl !== true) {
        L.control.scale().addTo(leafmap);
      }
      if (config.center) {
        leafmap.setView(new L.LatLng(config.center.lat, config.center.lon), config.zoom || 13);
      } else if (config.bounds) {
        leafmap.fitBounds(config.bounds);
      }
      if (config.marker) {
        var icon = L.icon({
          iconUrl: '/--static--/pyams_gis/img/marker-icon.png',
          iconSize: [25, 41],
          iconAnchor: [12, 39]
        });
        var marker = L.marker();
        marker.setIcon(icon);
        marker.setLatLng({
          lon: config.marker.lon,
          lat: config.marker.lat
        });
        marker.addTo(leafmap);
      }
      map.data('leafmap', leafmap);
      map.data('leafmap.config', config);
      map.data('leafmap.layers', layers.reduce(function (res, layer) {
        return _objectSpread(_objectSpread({}, res), {}, _defineProperty({}, layer.options.name, layer));
      }, {}));
      map.trigger('map.finishing', [map, leafmap, config]);
      if (callback) {
        callback(leafmap, config);
      }
      map.trigger('map.finished', [map, leafmap, config]);
      resolve(leafmap);
    });
  });
};
var PyAMS_GIS = {
  /**
   * Map initialization
   *
   * @param maps: maps elements
   * @param options: optional maps configuration settings
   * @param callback: maps initialization callback
   */
  init: function init(maps, options, callback) {
    window.PyAMS_GIS = PyAMS_GIS;
    Promise.all([__webpack_require__.e(/*! import() */ "vendors-node_modules_leaflet_dist_leaflet-src_js").then(__webpack_require__.t.bind(__webpack_require__, /*! leaflet */ "./node_modules/leaflet/dist/leaflet-src.js", 23)), __webpack_require__.e(/*! import() */ "vendors-node_modules_leaflet_dist_leaflet_css").then(__webpack_require__.bind(__webpack_require__, /*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css"))]).then(function () {
      Promise.all([__webpack_require__.e(/*! import() */ "vendors-node_modules_leaflet-gesture-handling_dist_leaflet-gesture-handling_min_js").then(__webpack_require__.t.bind(__webpack_require__, /*! leaflet-gesture-handling */ "./node_modules/leaflet-gesture-handling/dist/leaflet-gesture-handling.min.js", 23)), __webpack_require__.e(/*! import() */ "node_modules_leaflet-gesture-handling_dist_leaflet-gesture-handling_css").then(__webpack_require__.bind(__webpack_require__, /*! leaflet-gesture-handling/dist/leaflet-gesture-handling.css */ "./node_modules/leaflet-gesture-handling/dist/leaflet-gesture-handling.css")), __webpack_require__.e(/*! import() */ "node_modules_leaflet-fullscreen_dist_Leaflet_fullscreen_js").then(__webpack_require__.t.bind(__webpack_require__, /*! leaflet-fullscreen */ "./node_modules/leaflet-fullscreen/dist/Leaflet.fullscreen.js", 23)), __webpack_require__.e(/*! import() */ "node_modules_leaflet-fullscreen_dist_leaflet_fullscreen_css").then(__webpack_require__.bind(__webpack_require__, /*! leaflet-fullscreen/dist/leaflet.fullscreen.css */ "./node_modules/leaflet-fullscreen/dist/leaflet.fullscreen.css"))]).then(function () {
        var $maps = $.map(maps, function (elt) {
          return new Promise(function (resolve, reject) {
            var map = $(elt),
              data = map.data(),
              config = data.mapConfiguration;
            if (config) {
              resolve(createMap(map, config, options, callback));
            } else {
              $.get(data.mapConfigurationUrl || 'get-map-configuration.json').then(function (config) {
                createMap(map, config, options, callback).then(function (leafmap) {
                  resolve({
                    'leafmap': leafmap,
                    'config': config
                  });
                });
              });
            }
          });
        });
        $.when.apply($, $maps).then();
      });
    });
  },
  /**
   * Get layer definition
   *
   * @param map: source map element
   * @param leafmap: current Leaflet map
   * @param layer: current layer definition
   */
  getLayer: function getLayer(map, leafmap, layer) {
    var factory = _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject(layer.factory);
    if (factory !== undefined) {
      delete layer.factory;
      var deferred = [];
      if (layer.dependsOn) {
        for (var name in layer.dependsOn) {
          if (!layer.dependsOn.hasOwnProperty(name)) {
            continue;
          }
          if (_utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject(name) === undefined) {
            deferred.push(_utils__WEBPACK_IMPORTED_MODULE_0__["default"].getScript(layer.dependsOn[name]));
          }
        }
        delete layer.dependsOn;
      }
      if (deferred.length > 0) {
        $.when.apply($, deferred);
      }
      return factory(map, leafmap, layer);
    }
  },
  /**
   * Layers factories
   */
  factory: {
    GeoJSON: function GeoJSON(map, leafmap, layer) {
      var url = layer.url;
      delete layer.url;
      var result = L.geoJSON(null, layer);
      map.on('map.finished', function (evt, map, leafmap, config) {
        $.get(url, function (data) {
          result.addData(data.geometry, {
            style: layer.style
          });
          if (config.fitLayer === layer.name) {
            leafmap.fitBounds(result.getBounds());
          }
        });
      });
      return result;
    },
    TileLayer: function TileLayer(map, leafmap, layer) {
      var url = layer.url;
      delete layer.url;
      return L.tileLayer(url, layer);
    },
    WMS: function WMS(map, leafmap, layer) {
      var url = layer.url;
      delete layer.url;
      return L.tileLayer.wms(url, layer);
    },
    Geoportal: {
      WMS: function WMS(map, leafmap, layer) {
        _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getCSS('/--static--/pyams_gis/css/leaflet-gp-3.0.2.min.css', 'geoportal');
        return L.geoportalLayer.WMS(layer);
      }
    },
    ESRI: {
      Feature: function Feature(map, leafmap, layer) {
        return L.esri.featureLayer(layer);
      }
    },
    Google: function Google(map, leafmap, layer) {
      var apiKey = layer.apiKey;
      delete layer.apiKey;
      if (_utils__WEBPACK_IMPORTED_MODULE_0__["default"].getObject('window.google.maps') === undefined) {
        var script = _utils__WEBPACK_IMPORTED_MODULE_0__["default"].getScript('https://maps.googleapis.com/maps/api/js?key=' + apiKey);
        $.when.apply($, [script]);
      }
      return L.gridLayer.googleMutant(layer);
    }
  }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PyAMS_GIS);

/***/ })

}]);
//# sourceMappingURL=src_pyams_content_themes_resources_src_js__gis_js.js.map