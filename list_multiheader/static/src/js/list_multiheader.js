/* list_multiheader
 * Odoo, Open Source Management Solution
 * Copyright (C) Anybox
 * Copyright (C) 2017 Decodio applications ltd.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('list_multiheader', function (require) {
"use strict";

    var core = require('web.core');
    var View = require('web.View');
    var ListView = require('web.ListView');
    var _t = core._t;
    var _lt = core._lt;
    var QWeb = core.qweb;

    var list_widget_registry = core.list_widget_registry;

    var ListViewMultiHeader = ListView.extend({
        _template: 'ListViewMultiHeader',
        require_fields: true,
        defaults: _.extend({}, View.prototype.defaults, {
            // records can be selected one by one
            selectable: true,
            // list rows can be deleted
            deletable: false,
            // whether the column headers should be displayed
            header: true,
        }),

        display_name: _lt('List multi header'),
        view_type: 'list_multiheader',
        init: function(parent, dataset, view_id, options) {
            this.multiheader_columns = [];
            this.levels = [];
            this._super(parent, dataset, view_id, options);
        },
        setup_columns: function (fields, grouped) {
            var header_class = this.fields_view.arch.attrs.header_class || '';
            this.columns.splice(0, this.columns.length);
            this.multiheader_columns.splice(0, this.multiheader_columns.length);
            var multiheader_columns = [];
            var res = this.multiheader_setup_columns(
                fields, this.fields_view.arch.children, multiheader_columns, 0, header_class);
            this.columns.push.apply(this.columns, res);
            this.multiheader_columns.push.apply(this.multiheader_columns, multiheader_columns);
            this.levels = _.range(multiheader_columns.length);
            if (grouped) {
            this.columns.unshift(new ListView.MetaColumn('_group'));
        }

        this.visible_columns = _.filter(this.columns, function (column) {
            return column.invisible !== '1';
        });

        this.aggregate_columns = _(this.visible_columns).invoke('to_aggregate');
        },
        multiheader_setup_columns: function(fields, nodes, multiheader_columns, depth,
                                            initclass){
            var self = this;
            var simple_columns = [];
            if (!multiheader_columns[depth]) {
                multiheader_columns[depth] = [];
            }
            _(nodes).each(function(node) {
                var nodeclass = initclass;
                if (node.attrs.header_class)
                    nodeclass += " " + node.attrs.header_class;
                if (node.tag == 'field'){
                    var id = node.attrs.name;
                    var c = for_(id, fields[id], node);
                    var modifiers = _.extend({}, c.modifiers);
                    if (modifiers['invisible']) c.invisible = '1';
                    nodeclass += " o_multiheader-field";
                    nodeclass += " oe_list_header_" + (c.widget || c.type);
                    if (self.options.sortable && c.tag !== 'button')
                        nodeclass += " o_column_sortable"
                    c.header_class = nodeclass;
                    simple_columns.push(c);
                    multiheader_columns[depth].push(c);
                } else {
                    nodeclass += " o_multiheader-group";
                    var res = self.multiheader_setup_columns(
                        fields, node.children, multiheader_columns, depth + 1, nodeclass);
                    simple_columns = simple_columns.concat(res);
                    multiheader_columns[depth].push({
                        tag: 'group',
                        colspan: node.children.length,
                        string: node.attrs.string,
                        header_style: node.attrs.header_style,
                        header_class: nodeclass
                    });
                };
            });
            return simple_columns;
        },
        edition_view: function (editor) {
            var view = $.extend(true, {}, this.fields_view);
            view.arch.tag = 'form';
            _.extend(view.arch.attrs, {
                'class': 'o_list_editable_form',
                version: '7.0'
            });
            var nodes = this.multiheader_get_nodes(view.arch.children);
            _(nodes).chain()
                .zip(_(this.columns).filter(function (c) {
                    return !(c instanceof ListView.MetaColumn);}))
                .each(function (ar) {
                    var widget = ar[0], column = ar[1];
                    var modifiers = _.extend({}, column.modifiers);
                    widget.attrs.nolabel = true;
                    if (modifiers['tree_invisible'] || widget.tag === 'button') {
                        modifiers.invisible = true;
                    }
                    widget.attrs.modifiers = JSON.stringify(modifiers);
                });
            // for the form view we remove the groups and put only the fields
            // else groupe apear on top of the header
            view.arch.children = nodes;
            return view;
        },
        multiheader_get_nodes: function(nodes) {
            var self = this;
            var res = [];
            _(nodes).each(function (node){
                node.attrs.nolabel = true;;
                if (node.tag == 'field'){
                    res.push(node);
                } else {
                    res = res.concat(self.multiheader_get_nodes(node.children));
                };
            });
            return res;
        },
    });
    core.view_registry.add('list_multiheader', ListViewMultiHeader);

    function for_ (id, field, node) {
        var description = _.extend({tag: node.tag}, field, node.attrs);
        var tag = description.tag;
        var Type = list_widget_registry.get_any([
            tag + '.' + description.widget,
            tag + '.'+ description.type,
            tag
        ]);
        return new Type(id, node.tag, description);
    }
    return ListViewMultiHeader;
});
