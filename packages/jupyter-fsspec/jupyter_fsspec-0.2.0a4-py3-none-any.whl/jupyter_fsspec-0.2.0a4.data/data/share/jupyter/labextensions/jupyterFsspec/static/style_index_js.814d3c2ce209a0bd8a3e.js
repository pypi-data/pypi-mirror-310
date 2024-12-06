"use strict";
(self["webpackChunkjupyterFsspec"] = self["webpackChunkjupyterFsspec"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/

.jfss-root {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  min-width: 32px;
  color: var(--jp-ui-font-color0);
  background-color: var(--jp-layout-color1);
  font-size: var(--jp-ui-font-size1);
  font-family: var(--jp-ui-font-family);
}

.jfss-mainlabel {
  margin: 0 0 0.5rem;
  font-size: var(--jp-ui-font-size2);
  font-weight: bold;
}

.jfss-sourcescontrols {
  display: flex;
  align-items: center;
  margin: 0 0 0.5rem;
  padding: 0 0 0 0.5rem;
  border: 1px solid var(--jp-layout-color2);
  border-radius: 2px;
  background-color: var(--jp-layout-color1);
}

.jfss-sourcesdivider {
  flex-grow: 1;
}

.jfss-sourceslabel {
  margin: 0;
  font-size: var(--jp-ui-font-size2);

  /* font-weight: bold; */
}

.jfss-refreshconfig {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  margin: 0;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0 2px 2px 0;
  background-color: var(--jp-layout-color2);
  font-weight: bold;
}

.jfss-primarydivider {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding: 1rem;

  /* background-color: purple; */
}

.jfss-upperarea {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: auto;
  width: 100%;
  height: 40%;

  /* background-color: greenyellow; */
}

.jfss-emptysourceshint {
  height: 3rem;
  margin: 0.5rem 0;
  color: var(--jp-content-link-color);
  user-select: none;
}

.jfss-userfilesystems {
  overflow-y: auto;
}

.jfss-label {
  box-sizing: border-box;
  margin-bottom: 0.5rem;
}

.jfss-tree-item-container {
  box-sizing: border-box;
  display: flex;
}

.jfss-filesize-lbl {
  margin-left: 0.5rem;
  color: var(--jp-ui-font-color3);
}

.jfss-hseparator {
  box-sizing: border-box;
  width: 100%;
  height: 0.1rem;
  background-color: var(--jp-border-color3);
}

.jfss-lowerarea {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 60%;
  margin-top: 1rem;

  /* background-color: orange; */
}

.jfss-resultarea {
  box-sizing: border-box;
  width: 100%;
  height: calc(100% - 1.1rem);
  overflow: auto;
  border-radius: 2px;

  /* border: 1px solid var(--jp-layout-color2);
  border-top: 0; */

  /* background-color: #ddd; */
}

.jfss-hidden {
  display: none;
}

.jp-fsspec-widget {
  height: 100%;
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
}

.jfss-fsitem-root {
  /* box-sizing: border-box; */

  display: flex;
  overflow: hidden;
  flex-direction: column;
  align-items: flex-start;
  flex: 1 0 1.75rem;

  /* font-weight: bold; */

  margin: 0 0.5rem 0.5rem 0;
  padding: 0.5rem;
  border-radius: 2px;
  background-color: var(--jp-layout-color2);
}

.jfss-browseAreaLabel {
  width: 100%;
  margin: 0 0.5rem 0.5rem 0;

  /* font-weight: bold; */
  font-size: var(--jp-ui-font-size2);
}

.jfss-selectedFsLabel {
  /* width: 100%; */
  margin: 0 0 0.5rem;
  padding: 0;
  border-radius: 2px;

  /* color: white; */

  /* background-color: var(--jp-layout-color2); */

  font-weight: bold;
}

.jfss-fsitem-protocol {
  box-sizing: border-box;
  align-self: flex-start;

  /* height: 1.25rem; */

  /* padding: .25rem; */

  /* border-radius: 2px; */
  overflow: hidden;

  /* background-color: var(--jp-layout-color4); */
  white-space: nowrap;
}

.jfss-fsitem-name {
  box-sizing: border-box;

  /* height: 1rem; */

  border-radius: 2px;
  font-weight: bold;
  white-space: nowrap;
}

.jfss-dir-symbol {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 1.1rem;
  min-height: 1.1rem;
  margin: 0 0.5rem 0 0;
  border-radius: 0.1rem;
  color: var(--jp-ui-inverse-font-color0);

  /* background-color: var(--jp-layout-color4); */
}

.jfss-tree-context-menu {
  position: absolute;
  padding: 0.25rem;
  border-width: var(--jp-border-width);
  border-color: var(--jp-border-color3);
  border-style: solid;
  background-color: var(--jp-layout-color0);

  /* background-color: orange; */

  /* width: 10rem;
  height: 200px; */

  /* background-color: purple; */
}

.jfss-tree-context-item {
  display: flex;
  align-items: center;
  width: 10rem;
  height: 1.2rem;
  padding: 0.25rem;
  border-width: 0 0 var(--jp-border-width) 0;
  border-color: var(--jp-border-color3);
  border-style: solid;
  background-color: var(--jp-layout-color1);
}

.jfss-filesys-item {
  width: 200px;
  height: 100px;

  /* background-color: green; */
}
`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"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","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n.jfss-root {\n  box-sizing: border-box;\n  width: 100%;\n  height: 100%;\n  min-width: 32px;\n  color: var(--jp-ui-font-color0);\n  background-color: var(--jp-layout-color1);\n  font-size: var(--jp-ui-font-size1);\n  font-family: var(--jp-ui-font-family);\n}\n\n.jfss-mainlabel {\n  margin: 0 0 0.5rem;\n  font-size: var(--jp-ui-font-size2);\n  font-weight: bold;\n}\n\n.jfss-sourcescontrols {\n  display: flex;\n  align-items: center;\n  margin: 0 0 0.5rem;\n  padding: 0 0 0 0.5rem;\n  border: 1px solid var(--jp-layout-color2);\n  border-radius: 2px;\n  background-color: var(--jp-layout-color1);\n}\n\n.jfss-sourcesdivider {\n  flex-grow: 1;\n}\n\n.jfss-sourceslabel {\n  margin: 0;\n  font-size: var(--jp-ui-font-size2);\n\n  /* font-weight: bold; */\n}\n\n.jfss-refreshconfig {\n  display: flex;\n  align-items: center;\n  justify-content: space-evenly;\n  margin: 0;\n  width: 1.5rem;\n  height: 1.5rem;\n  border-radius: 0 2px 2px 0;\n  background-color: var(--jp-layout-color2);\n  font-weight: bold;\n}\n\n.jfss-primarydivider {\n  box-sizing: border-box;\n  width: 100%;\n  height: 100%;\n  padding: 1rem;\n\n  /* background-color: purple; */\n}\n\n.jfss-upperarea {\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: column;\n  overflow: auto;\n  width: 100%;\n  height: 40%;\n\n  /* background-color: greenyellow; */\n}\n\n.jfss-emptysourceshint {\n  height: 3rem;\n  margin: 0.5rem 0;\n  color: var(--jp-content-link-color);\n  user-select: none;\n}\n\n.jfss-userfilesystems {\n  overflow-y: auto;\n}\n\n.jfss-label {\n  box-sizing: border-box;\n  margin-bottom: 0.5rem;\n}\n\n.jfss-tree-item-container {\n  box-sizing: border-box;\n  display: flex;\n}\n\n.jfss-filesize-lbl {\n  margin-left: 0.5rem;\n  color: var(--jp-ui-font-color3);\n}\n\n.jfss-hseparator {\n  box-sizing: border-box;\n  width: 100%;\n  height: 0.1rem;\n  background-color: var(--jp-border-color3);\n}\n\n.jfss-lowerarea {\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: column;\n  width: 100%;\n  height: 60%;\n  margin-top: 1rem;\n\n  /* background-color: orange; */\n}\n\n.jfss-resultarea {\n  box-sizing: border-box;\n  width: 100%;\n  height: calc(100% - 1.1rem);\n  overflow: auto;\n  border-radius: 2px;\n\n  /* border: 1px solid var(--jp-layout-color2);\n  border-top: 0; */\n\n  /* background-color: #ddd; */\n}\n\n.jfss-hidden {\n  display: none;\n}\n\n.jp-fsspec-widget {\n  height: 100%;\n  overflow-y: auto;\n  padding: 10px;\n  box-sizing: border-box;\n}\n\n.jfss-fsitem-root {\n  /* box-sizing: border-box; */\n\n  display: flex;\n  overflow: hidden;\n  flex-direction: column;\n  align-items: flex-start;\n  flex: 1 0 1.75rem;\n\n  /* font-weight: bold; */\n\n  margin: 0 0.5rem 0.5rem 0;\n  padding: 0.5rem;\n  border-radius: 2px;\n  background-color: var(--jp-layout-color2);\n}\n\n.jfss-browseAreaLabel {\n  width: 100%;\n  margin: 0 0.5rem 0.5rem 0;\n\n  /* font-weight: bold; */\n  font-size: var(--jp-ui-font-size2);\n}\n\n.jfss-selectedFsLabel {\n  /* width: 100%; */\n  margin: 0 0 0.5rem;\n  padding: 0;\n  border-radius: 2px;\n\n  /* color: white; */\n\n  /* background-color: var(--jp-layout-color2); */\n\n  font-weight: bold;\n}\n\n.jfss-fsitem-protocol {\n  box-sizing: border-box;\n  align-self: flex-start;\n\n  /* height: 1.25rem; */\n\n  /* padding: .25rem; */\n\n  /* border-radius: 2px; */\n  overflow: hidden;\n\n  /* background-color: var(--jp-layout-color4); */\n  white-space: nowrap;\n}\n\n.jfss-fsitem-name {\n  box-sizing: border-box;\n\n  /* height: 1rem; */\n\n  border-radius: 2px;\n  font-weight: bold;\n  white-space: nowrap;\n}\n\n.jfss-dir-symbol {\n  box-sizing: border-box;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  min-width: 1.1rem;\n  min-height: 1.1rem;\n  margin: 0 0.5rem 0 0;\n  border-radius: 0.1rem;\n  color: var(--jp-ui-inverse-font-color0);\n\n  /* background-color: var(--jp-layout-color4); */\n}\n\n.jfss-tree-context-menu {\n  position: absolute;\n  padding: 0.25rem;\n  border-width: var(--jp-border-width);\n  border-color: var(--jp-border-color3);\n  border-style: solid;\n  background-color: var(--jp-layout-color0);\n\n  /* background-color: orange; */\n\n  /* width: 10rem;\n  height: 200px; */\n\n  /* background-color: purple; */\n}\n\n.jfss-tree-context-item {\n  display: flex;\n  align-items: center;\n  width: 10rem;\n  height: 1.2rem;\n  padding: 0.25rem;\n  border-width: 0 0 var(--jp-border-width) 0;\n  border-color: var(--jp-border-color3);\n  border-style: solid;\n  background-color: var(--jp-layout-color1);\n}\n\n.jfss-filesys-item {\n  width: 200px;\n  height: 100px;\n\n  /* background-color: green; */\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=style_index_js.814d3c2ce209a0bd8a3e.js.map