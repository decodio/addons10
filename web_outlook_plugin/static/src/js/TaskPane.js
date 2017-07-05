// Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license. See full license at the bottom of this file.

/// <reference path="./App.js" />

(function () {
  "use strict";

  // The Office initialize function must be run each time a new page is loaded
  Office.initialize = function (reason) {
      $(document).ready(function () {
          app.initialize();

          loadProps();
      });
  };

  // Take an array of AttachmentDetails objects and
  // build a list of attachment names, separated by a line-break
  function buildAttachmentsString(attachments) {
    if (attachments && attachments.length > 0) {
      var returnString = "";

      for (var i = 0; i < attachments.length; i++) {
        if (i > 0) {
          returnString = returnString + "<br/>";
        }
        returnString = returnString + attachments[i].name;
      }

      return returnString;
    }

    return "None";
  }

  // Format an EmailAddressDetails object as
  // GivenName Surname <emailaddress>
  function buildEmailAddressString(address) {
    return address.displayName + " <" + address.emailAddress + ">";
  }

  // Take an array of EmailAddressDetails objects and
  // build a list of formatted strings, separated by a line-break
  function buildEmailAddressesString(addresses) {
    if (addresses && addresses.length > 0) {
      var returnString = "";

      for (var i = 0; i < addresses.length; i++) {
        if (i > 0) {
          returnString = returnString + "<br/>";
        }
        returnString = returnString + buildEmailAddressString(addresses[i]);
      }

      return returnString;
    }

    return "None";
  }

  // Load properties from a Message object
  function loadMessageProps(item) {
    $('#message-props').show();

    $('#attachments').html(buildAttachmentsString(item.attachments));
    $('#cc').html(buildEmailAddressesString(item.cc));
    $('#conversationId').text(item.conversationId);
    $('#from').html(buildEmailAddressString(item.from));
    $('#internetMessageId').text(item.internetMessageId);
    $('#normalizedSubject').text(item.normalizedSubject);
    $('#sender').html(buildEmailAddressString(item.sender));
    $('#subject').text(item.subject);
    $('#to').html(buildEmailAddressesString(item.to));
  }

  // Load properties from an Appointment object
  function loadAppointmentProps(item) {
    $('#appointment-props').show();

    $('#appt-attachments').html(buildAttachmentsString(item.attachments));
    $('#end').text(item.end.toLocaleString());
    $('#location').text(item.location);
    $('#appt-normalizedSubject').text(item.normalizedSubject);
    $('#optionalAttendees').html(buildEmailAddressesString(item.optionalAttendees));
    $('#organizer').html(buildEmailAddressString(item.organizer));
    $('#requiredAttendees').html(buildEmailAddressesString(item.requiredAttendees));
    $('#resources').html(buildEmailAddressesString(item.resources));
    $('#start').text(item.start.toLocaleString());
    $('#appt-subject').text(item.subject);
  }



  // Load properties from the Item base object, then load the
  // type-specific properties.
  function loadProps() {
    var item = Office.context.mailbox.item;



    $('#att_msg_2_lead').prop('disabled', false);
    $('#att_msg_2_lead').off('click');
    $('#att_msg_2_lead').on('click', function() {
        var p_id = $('#dropdownleads').val();
        var dataPromiseAttachMessageToLead = AttachMessageToObject(item, 'crm.lead', p_id);
        dataPromiseAttachMessageToLead.done(function(data){
            if (!data) {
                data = "Unknow excetion!";
            }
            $('#outlook_response').html(data);
            Office.context.mailbox.item.notificationMessages.addAsync("information", {
                type: "informationalMessage",
                message: data,
                icon: "blue-icon-16",
                persistent: false
            });
            if (typeof event !== 'undefined') {
                event.completed();
            }
        });

        // register the failure function
        dataPromiseAttachMessageToLead.fail(function(data){
            if (!data) {
                data = "Unknow excetion!";
            }
            $('#outlook_response').html(data);
            Office.context.mailbox.item.notificationMessages.addAsync("error", {
                type: "errorMessage",
                message: data,
                //persistent: false
            });
            if (typeof event !== 'undefined') {
                event.completed();
            }
        });


    });


    $('#outlook_response').html(item.attachments);
    $('#att_msg_2_nlead').off('click');
    $('#att_msg_2_nlead').on('click', function() {
        var p_id = $('#dropdownleads').val();

        var dataPromise = AttachMessageToNewObject(item, 'crm.lead' );
        dataPromise.done(function(data){
            if (!data) {
                data = "Unknow excetion!";
            }
            $('#outlook_response').html(data);
            Office.context.mailbox.item.notificationMessages.addAsync("information", {
                type: "informationalMessage",
                message: data,
                icon: "blue-icon-16",
                persistent: false
            });
            if (typeof event !== 'undefined') {
                event.completed();
            }
        });

        // register the failure function
        dataPromise.fail(function(data){
            if (!data) {
                data = "Unknow excetion!";
            }
            $('#outlook_response').html(data);
            Office.context.mailbox.item.notificationMessages.addAsync("error", {
                type: "errorMessage",
                message: data,
            });
            if (typeof event !== 'undefined') {
                event.completed();
            }
        });

    });


  }
})();

// MIT License: 
 
// Permission is hereby granted, free of charge, to any person obtaining 
// a copy of this software and associated documentation files (the 
// ""Software""), to deal in the Software without restriction, including 
// without limitation the rights to use, copy, modify, merge, publish, 
// distribute, sublicense, and/or sell copies of the Software, and to 
// permit persons to whom the Software is furnished to do so, subject to 
// the following conditions: 
 
// The above copyright notice and this permission notice shall be 
// included in all copies or substantial portions of the Software. 
 
// THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, 
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.