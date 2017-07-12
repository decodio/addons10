Multi header list
=================

Allows to define n lines of header for a ``tree`` view.

Example: for header::

    Field 1 |      Group 1      |           Group 2
            | Field 2 | Field 3 | Field 4 |      Group 3
            |         |         |         | Field 5 | Field 6

The configuration is::

    <list_multiheader version="7.0" header_class="To add a global class">
    <field name="Field 1" header-style="background-color: blue;"/>
        <group string="Group 1" header-style="background-color: red;"/>
            <field name="Field 2"/>
            <field name="Field 3"/>
        </group>
        <group string="Group 2" header_class="Add a class on the childrend element"/>
            <field name="Field 4"/>
            <group string="Group 3"/>
                <field name="Field 5"/>
                <field name="Field 6" header_class="Add specific class for this field"/>
            </group>
        </group>
    </list_multiheader>

Don't forget to modify the related ir.actions.act_window like this:

           <field name="view_type">form</field>
           <field name="view_mode">list_multiheader</field>

Tested with
-----------

* List view by action
* Group_by
* Editable bottom and top
* Sortable fields
* Add a header_style on a specific node of the view (Not distribut)
* Add header_class on a specific field
* Add header_class on a specific group and their children
* Add header_class on the list_multiheader for all the node of the view
* invisible in the field of the main line, invisible is forbidden for group and field in group

TODO
----

* Multi header list in form view
