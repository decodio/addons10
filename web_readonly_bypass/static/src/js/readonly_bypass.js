odoo.define('web.readonly_bypass', function(require) {
"use strict";
var data = require('web.data');

/**
 * NOT in use. yet

var core = require('web.core');
var Model = require('web.Model');

var _t = core._t;
var QWeb = core.qweb;

*/

function ignore_readonly(data, options, mode, context) {
    var readonly_by_pass_fields = this.retrieve_readonly_by_pass_fields(
        options, context);
    if(mode){
        $.each( readonly_by_pass_fields, function( key, value ) {
            if(value==false){
                delete(readonly_by_pass_fields[key]);
            }
        });
    }
    data = $.extend(data,readonly_by_pass_fields);
}
/**
 * NOT in use yet
*/
function retrieve_readonly_by_pass_fields (options, context){
    var readonly_by_pass_fields = {};
    if (options && 'readonly_fields' in options &&
       options['readonly_fields'] && context &&
       'readonly_by_pass' in context && context['readonly_by_pass']){
        if (_.isArray(context['readonly_by_pass'])){
            $.each( options.readonly_fields, function( key, value ) {
                if(_.contains(context['readonly_by_pass'], key)){
                    readonly_by_pass_fields[key] = value;
                }
            });
        }else{
            readonly_by_pass_fields = options.readonly_fields;
        }
    }
    return readonly_by_pass_fields;
}


data.BufferedDataSet.include({

        init : function() {
            this._super.apply(this, arguments);
        },
        /**
         * Creates Overriding
         *
         * @param {Object} data field values to set on the new record
         * @param {Object} options Dictionary that can contain the following keys:
         *   - readonly_fields: Values from readonly fields that were updated by
         *     on_changes. Only used by the BufferedDataSet to make the o2m work correctly.
         * @returns super {$.Deferred}
         */
        create : function(data, options) {
            var all_data = _.extend({}, data, (options || {}).readonly_fields || {});
            return this._super(all_data,options);
        },
        write : function(id, data, options) {
            var all_data = _.extend({}, data, (options || {}).readonly_fields || {});
            return this._super(id,all_data,options);
        },

    });

data.DataSet.include({
        /*
        BufferedDataSet: case of 'add an item' into a form view
        */
        init : function() {
            this._super.apply(this, arguments);
        },
        create : function(data, options) {
            var all_data = _.extend({}, data, (options || {}).readonly_fields || {});
            return this._super(all_data,options);
        },
        write : function(id, data, options) {
            var all_data = _.extend({}, data, (options || {}).readonly_fields || {});
            return this._super(id,all_data,options);
        },

    });

data.ProxyDataSet.include({
        /*
        ProxyDataSet: case of 'pop-up'
        */
        init : function() {
            this._super.apply(this, arguments);
        },
        create : function(data, options) {
            var all_data = _.extend({}, data, (options || {}).readonly_fields || {});
            return this._super(data,options);
        },
        write : function(id, data, options) {
            var all_data = _.extend({}, data, (options || {}).readonly_fields || {});
            return this._super(id,data,options);
        },

    });

});
