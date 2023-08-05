(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modHelpers = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.helpers = void 0;

  function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

  function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

  function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

  /* global MyAMS */

  /**
   * MyAMS generic helpers
   */
  var $ = MyAMS.$;
  var helpers = {
    /**
     * Click handler used to clear input
     */
    clearValue: function clearValue(evt) {
      var target = $(evt.currentTarget).data('target');

      if (target) {
        $(target).val(null);
      }
    },

    /**
     * Click handler used to clear datetime input
     */
    clearDatetimeValue: function clearDatetimeValue(evt) {
      var target = $(evt.currentTarget).data('target'),
          picker = $(target).data('datetimepicker');

      if (picker) {
        picker.date(null);
      }
    },

    /**
     * Scroll anchor parent element to given anchor
     *
     * @param anchor: scroll target
     * @param parent: scroll parent
     * @param props: scroll properties
     */
    scrollTo: function scrollTo() {
      var parent = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '#content';
      var anchor = arguments.length > 1 ? arguments[1] : undefined;

      var _ref = arguments.length > 2 ? arguments[2] : undefined,
          props = _extends({}, _ref);

      if (typeof anchor === 'string') {
        anchor = $(anchor);
      }

      if (anchor.exists()) {
        MyAMS.require('ajax').then(function () {
          MyAMS.ajax.check($.fn.scrollTo, "".concat(MyAMS.env.baseURL, "../ext/jquery-scrollto").concat(MyAMS.env.extext, ".js")).then(function () {
            $(parent).scrollTo(anchor, props);
          });
        });
      }
    },

    /**
     * Store location hash when redirecting to log in form
     */
    setLoginHash: function setLoginHash() {
      var form = $('#login_form'),
          hash = $("input[name=\"login_form.widgets.hash\"]", form);
      hash.val(window.location.hash);
    },

    /**
     * SEO input helper
     */
    setSEOStatus: function setSEOStatus(evt) {
      var input = $(evt.target),
          progress = input.siblings('.progress').children('.progress-bar'),
          length = Math.min(input.val().length, 100);
      var status = 'success';

      if (length < 20 || length > 80) {
        status = 'danger';
      } else if (length < 40 || length > 66) {
        status = 'warning';
      }

      progress.removeClassPrefix('bg-').addClass('bg-' + status).css('width', length + '%');
    },

    /**
     * Select2 change helper
     */
    select2ChangeHelper: function select2ChangeHelper(evt) {
      var source = $(evt.currentTarget),
          data = source.data(),
          target = $(data.amsSelect2HelperTarget);

      switch (data.amsSelect2HelperType) {
        case 'html':
          target.html('<div class="text-center"><i class="fas fa-2x fa-spinner fa-spin"></i></div>');
          var params = {};
          params[data.amsSelect2HelperArgument || 'value'] = source.val();
          $.get(data.amsSelect2HelperUrl, params).then(function (result) {
            var callback = MyAMS.core.getFunctionByName(data.amsSelect2HelperCallback) || function (result) {
              if (result) {
                target.html(result);
                MyAMS.core.initContent(target).then();
              } else {
                target.empty();
              }
            };

            callback(result);
          }).catch(function () {
            target.empty();
          });
          break;

        default:
          var callback = data.amsSelect2HelperCallback;

          if (callback) {
            MyAMS.core.executeFunctionByName(callback, source, data);
          }

      }
    },

    /**
     * Refresh a DOM element with content provided in
     * the <code>options</code> object.
     *
     * @param form: optional parent element
     * @param options: element properties:
     *   - object_id: ID of the refreshed element
     *   - content: new element content
     */
    refreshElement: function refreshElement(form, options) {
      return new Promise(function (resolve, reject) {
        var element = $("[id=\"".concat(options.object_id, "\"]"));
        MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, element).then(function () {
          element.replaceWith($(options.content));
          element = $("[id=\"".concat(options.object_id, "\"]"));
          var parent = element.parents().first();
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, parent).then(function () {
            resolve(element);
          }, reject);
        }, reject);
      });
    },

    /**
     * Refresh a form widget with content provided in
     * the <code>options</code> object
     *
     * @param form: optional parent form
     * @param options: updated widget properties:
     *   - widget_id: ID of the refreshed widget
     *   - content: new element content
     */
    refreshWidget: function refreshWidget(form, options) {
      return new Promise(function (resolve, reject) {
        var widget = $("[id=\"".concat(options.widget_id, "\"]")),
            group = widget.parents('.widget-group');
        MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, group).then(function () {
          group.replaceWith($(options.content));
          widget = $("[id=\"".concat(options.widget_id, "\"]"));
          group = widget.parents('.widget-group');
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, group).then(function () {
            resolve(widget);
          }, reject);
        }, reject);
      });
    },

    /**
     * Add new row to table
     *
     * @param form: optional parent form
     * @param options: added row properties:
     *  - content: new row content
     */
    addTableRow: function addTableRow(form, options) {
      return new Promise(function (resolve, reject) {
        var selector = "table[id=\"".concat(options.table_id, "\"]"),
            table = $(selector),
            dtTable = table.DataTable();
        var newRow;

        if (options.data) {
          dtTable.rows.add(options.data).draw();
          newRow = $("tr[id=\"".concat(options.row_id, "\"]"), table);
          resolve(newRow);
        } else {
          newRow = $(options.content);
          dtTable.rows.add(newRow).draw();
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, newRow).then(function () {
            resolve(newRow);
          }, reject);
        }
      });
    },

    /**
     * Refresh a table row with content provided in
     * the <code>options</code> object
     *
     * @param form: optional parent form
     * @param options: updated row properties:
     *   - row_id: ID of the refreshed row
     *   - content: new row content
     */
    refreshTableRow: function refreshTableRow(form, options) {
      return new Promise(function (resolve, reject) {
        var selector = "tr[id=\"".concat(options.row_id, "\"]"),
            row = $(selector),
            table = row.parents('table').first();

        if (options.data) {
          if ($.fn.DataTable) {
            var dtTable = table.DataTable();

            if (typeof options.data === 'string') {
              dtTable.row(selector).remove();
              dtTable.row.add($(options.data)).draw();
            } else {
              dtTable.row(selector).data(options.data).draw();
            }

            resolve(row);
          } else {
            reject('No DataTable plug-in available!');
          }
        } else {
          var newRow = $(options.content);
          row.replaceWith(newRow);
          MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, newRow).then(function () {
            resolve(newRow);
          }, reject);
        }
      });
    },

    /**
     * Refresh a single image with content provided in
     * the <code>options</code> object.
     *
     * @param form: optional parent element
     * @param options: image properties:
     *   - image_id: ID of the refreshed image
     *   - src: new image source URL
     */
    refreshImage: function refreshImage(form, options) {
      var image = $("[id=\"".concat(options.image_id, "\"]"));
      image.attr('src', options.src);
    },

    /**
     * Move given element to the end of it's parent
     *
     * @param element: the element to be moved
     * @returns {*}
     */
    moveElementToParentEnd: function moveElementToParentEnd(element) {
      var parent = element.parent();
      return element.detach().appendTo(parent);
    },

    /**
     * Add given element to the end of specified parent
     *
     * @param source: event source
     * @param element: the provided element
     * @param parent: the parent to which element should be added
     * @param props: additional props
     * @returns {*}
     */
    addElementToParent: function addElementToParent(source, _ref2) {
      var element = _ref2.element,
          parent = _ref2.parent,
          props = _objectWithoutProperties(_ref2, ["element", "parent"]);

      element = $(element);
      parent = $(parent);
      var result = element.appendTo(parent);

      if (props.scrollTo) {
        MyAMS.helpers.scrollTo(props.scrollParent, element);
      }

      return result;
    },

    /**
     * Toggle dropdown associated with given event target
     *
     * @param evt: source event
     */
    hideDropdown: function hideDropdown(evt) {
      $(evt.target).closest('.dropdown-menu').dropdown('hide');
    }
  };
  /**
   * Global module initialization
   */

  _exports.helpers = helpers;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('helpers');
    } else {
      MyAMS.helpers = helpers;
      console.debug("MyAMS: helpers module loaded...");
    }
  }
});
//# sourceMappingURL=mod-helpers-dev.js.map
