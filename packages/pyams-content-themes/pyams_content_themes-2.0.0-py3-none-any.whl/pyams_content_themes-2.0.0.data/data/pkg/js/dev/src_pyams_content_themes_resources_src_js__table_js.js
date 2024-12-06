"use strict";
(self["webpackChunkpyams_content_themes"] = self["webpackChunkpyams_content_themes"] || []).push([["src_pyams_content_themes_resources_src_js__table_js"],{

/***/ "./src/pyams_content_themes/resources/src/js/_table.js":
/*!*************************************************************!*\
  !*** ./src/pyams_content_themes/resources/src/js/_table.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var datatables_net_bs4__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! datatables.net-bs4 */ "./node_modules/datatables.net-bs4/js/dataTables.bootstrap4.mjs");
/* harmony import */ var datatables_net_responsive_bs4__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! datatables.net-responsive-bs4 */ "./node_modules/datatables.net-responsive-bs4/js/responsive.bootstrap4.mjs");
/* harmony import */ var datatables_net_rowgroup__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! datatables.net-rowgroup */ "./node_modules/datatables.net-rowgroup/js/dataTables.rowGroup.mjs");
/* harmony import */ var datatables_net_plugins_i18n_fr_FR_mjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! datatables.net-plugins/i18n/fr-FR.mjs */ "./node_modules/datatables.net-plugins/i18n/fr-FR.mjs");
/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t["return"] && (u = t["return"](), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }




var createTable = function createTable(table, config, options, callback) {
  return new Promise(function (resolve, reject) {
    var data = table.data();
    var settings = {
      language: datatables_net_plugins_i18n_fr_FR_mjs__WEBPACK_IMPORTED_MODULE_3__["default"],
      responsive: true
    };
    // initialize DOM string
    var dom = '';
    settings = $.extend({}, settings, data, config);
    if (settings.buttons) {
      dom += "<'row px-4 float-right'B>";
    }
    if (settings.searchBuilder) {
      dom += "Q";
    }
    if (settings.searchPanes) {
      dom += "P";
    }
    if (settings.searching !== false || settings.lengthChange !== false) {
      dom += "<'row px-2'";
      if (settings.searching !== false) {
        dom += "<'" + (settings.lengthChange !== false ? "col-sm-6 col-md-8" : "col-sm-12") + "'f>";
      }
      if (settings.lengthChange !== false) {
        dom += "<'" + (settings.searching !== false ? "col-sm-6 col-md-4" : "col-sm-12") + "'l>";
      }
      dom += ">";
    }
    dom += "<'row'<'col-sm-12'tr>>";
    if (settings.info !== false || settings.paging !== false) {
      dom += "<'row px-2 py-1'";
      if (settings.info !== false) {
        dom += "<'col-sm-12 " + (settings.paging !== false ? "col-md-5" : "") + "'i>";
      }
      if (settings.paging !== false) {
        dom += "<'col-sm-12 " + (settings.info !== false ? "col-md-7" : "") + "'p>";
      }
      dom += ">";
    }
    settings.dom = dom;
    // initialize sorting
    var order = data.amsDatatableOrder || data.amsOrder;
    if (typeof order === 'string') {
      var orders = order.split(';');
      order = [];
      var _iterator = _createForOfIteratorHelper(orders),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var col = _step.value;
          var colOrder = col.split(',');
          colOrder[0] = parseInt(colOrder[0]);
          order.push(colOrder);
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
    }
    if (order) {
      settings.order = order;
    }
    // initialize columns
    var heads = $('thead th', table),
      columns = [];
    heads.each(function (idx, th) {
      columns[idx] = $(th).data('ams-column') || {};
    });
    var sortables = heads.listattr('data-ams-sortable');
    var _iterator2 = _createForOfIteratorHelper(sortables.entries()),
      _step2;
    try {
      for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
        var iterator = _step2.value;
        var _iterator4 = _slicedToArray(iterator, 2),
          idx = _iterator4[0],
          sortable = _iterator4[1];
        if (data.rowReorder) {
          columns[idx].sortable = false;
        } else if (sortable !== undefined) {
          columns[idx].sortable = typeof sortable === 'string' ? JSON.parse(sortable) : sortable;
        }
      }
    } catch (err) {
      _iterator2.e(err);
    } finally {
      _iterator2.f();
    }
    var types = heads.listattr('data-ams-type');
    var _iterator3 = _createForOfIteratorHelper(types.entries()),
      _step3;
    try {
      for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
        var _iterator5 = _step3.value;
        var _iterator6 = _slicedToArray(_iterator5, 2),
          _idx = _iterator6[0],
          stype = _iterator6[1];
        if (stype !== undefined) {
          columns[_idx].type = stype;
        }
      }
    } catch (err) {
      _iterator3.e(err);
    } finally {
      _iterator3.f();
    }
    settings.columns = columns;
    // initialize table
    settings = $.extend({}, settings, options);
    table.trigger('datatable.init', [table, settings]);
    var instance = new datatables_net_bs4__WEBPACK_IMPORTED_MODULE_0__["default"]("#".concat(table.attr('id')), settings);
    table.trigger('datatable.finishing', [table, instance, settings]);
    if (callback) {
      callback(instance, settings);
    }
    if (settings.responsive) {
      setTimeout(function () {
        instance.responsive.rebuild();
        instance.responsive.recalc();
      }, 100);
    }
    table.trigger('datatable.finished', [table, instance, settings]);
    resolve(table);
  });
};
var PyAMS_datatable = {
  init: function init(tables, options, callback) {
    // Add autodetect formats
    var types = datatables_net_bs4__WEBPACK_IMPORTED_MODULE_0__["default"].ext.type;
    types.detect.unshift(function (data) {
      if (data !== null && data.match(/^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/[0-3][0-9]{3}$/)) {
        return 'date-euro';
      }
      return null;
    });
    types.detect.unshift(function (data) {
      if (data !== null && data.match(/^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/[0-3][0-9]{3} - ([0-1][0-9]|2[0-3]):[0-5][0-9]$/)) {
        return 'datetime-euro';
      }
      return null;
    });

    // Add sorting methods
    $.extend(types.order, {
      // numeric values using commas separators
      "numeric-comma-asc": function numericCommaAsc(a, b) {
        var x = a.replace(/,/, ".").replace(/ /g, '');
        var y = b.replace(/,/, ".").replace(/ /g, '');
        x = parseFloat(x);
        y = parseFloat(y);
        return x < y ? -1 : x > y ? 1 : 0;
      },
      "numeric-comma-desc": function numericCommaDesc(a, b) {
        var x = a.replace(/,/, ".").replace(/ /g, '');
        var y = b.replace(/,/, ".").replace(/ /g, '');
        x = parseFloat(x);
        y = parseFloat(y);
        return x < y ? 1 : x > y ? -1 : 0;
      },
      // date-euro column sorter
      "date-euro-pre": function dateEuroPre(a) {
        var trimmed = $.trim(a);
        var x;
        if (trimmed !== '') {
          var frDate = trimmed.split('/');
          x = (frDate[2] + frDate[1] + frDate[0]) * 1;
        } else {
          x = 10000000; // = l'an 1000 ...
        }

        return x;
      },
      "date-euro-asc": function dateEuroAsc(a, b) {
        return a - b;
      },
      "date-euro-desc": function dateEuroDesc(a, b) {
        return b - a;
      },
      // datetime-euro column sorter
      "datetime-euro-pre": function datetimeEuroPre(a) {
        var trimmed = $.trim(a);
        var x;
        if (trimmed !== '') {
          var frDateTime = trimmed.split(' - ');
          var frDate = frDateTime[0].split('/');
          var frTime = frDateTime[1].split(':');
          x = (frDate[2] + frDate[1] + frDate[0] + frTime[0] + frTime[1]) * 1;
        } else {
          x = 100000000000; // = l'an 1000 ...
        }

        return x;
      },
      "datetime-euro-asc": function datetimeEuroAsc(a, b) {
        return a - b;
      },
      "datetime-euro-desc": function datetimeEuroDesc(a, b) {
        return b - a;
      }
    });
    Promise.all([__webpack_require__.e(/*! import() */ "vendors-node_modules_datatables_net-bs4_css_dataTables_bootstrap4_css").then(__webpack_require__.bind(__webpack_require__, /*! datatables.net-bs4/css/dataTables.bootstrap4.css */ "./node_modules/datatables.net-bs4/css/dataTables.bootstrap4.css")), __webpack_require__.e(/*! import() */ "vendors-node_modules_datatables_net-responsive-bs4_css_responsive_bootstrap4_css").then(__webpack_require__.bind(__webpack_require__, /*! datatables.net-responsive-bs4/css/responsive.bootstrap4.css */ "./node_modules/datatables.net-responsive-bs4/css/responsive.bootstrap4.css"))]).then(function () {
      var $tables = $.map(tables, function (elt) {
        return new Promise(function (resolve, reject) {
          var table = $(elt),
            data = table.data(),
            config = data.config;
          resolve(createTable(table, config, options, callback));
        });
      });
      $.when.apply($, $tables).then();
    });
  }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PyAMS_datatable);

/***/ })

}]);
//# sourceMappingURL=src_pyams_content_themes_resources_src_js__table_js.js.map