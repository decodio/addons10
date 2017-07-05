// Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license. See full license at the bottom of this file.

Office.initialize = function () {
}

// Helper function to add a status message to
// the info bar.
function statusUpdate(icon, text) {
  Office.context.mailbox.item.notificationMessages.replaceAsync("status", {
    type: "informationalMessage",
    icon: icon,
    message: text,
    persistent: false
  });
}


function buildEmailAddressString(address) {
    return address.displayName + " <" + address.emailAddress + ">";
}


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


// Gets the sender of the item, using the from property if the
// item is a message and the organizer property if the item
// is an appointment.
function getSender(item) {
    var sender;
    if (item.itemType === Office.MailboxEnums.ItemType.Message) {
        sender = Office.context.mailbox.item.from;
    } else if (item.itemType === Office.MailboxEnums.ItemType.Appointment) {
        sender = Office.context.mailbox.item.organizer;
    }
    return sender;
}

// TODO refactor this
// Gets the subject of the item and displays it in the info bar.
function sendSenderToLeads(event) {
    console.log("sendSenderToLeads");
    var self = this;
    self.item = Office.context.mailbox.item;

    var dataPromise = AttachMessageToNewObject(self.item, 'crm.lead' );
    dataPromise.done(function(data1){
        if (!data1) {
            data1 = "Unknow exception!";
        }
        $('#outlook_response').html(data1);
        Office.context.mailbox.item.notificationMessages.addAsync("information", {
            type: "informationalMessage",
            message: data1,
            icon: "blue-icon-16",
            persistent: false
        });
        if (event) {
            event.completed();
        }
    });

    // register the failure function
    dataPromise.fail(function(data2){
        if (!data2) {
            data2 = "Unknow exception!";
        }
        $('#outlook_response').html(data2);
        Office.context.mailbox.item.notificationMessages.addAsync("error", {
            type: "errorMessage",
            message: data2,
            //persistent: false
        });
        if (event) {
            event.completed();
        }
    });
}

// Gets the subject of the item and displays it in the info bar.
function getSubject(event) {
  var subject = Office.context.mailbox.item.subject;
  var sender = Office.context.mailbox.item.sender;
  console.log('sender');
    console.log(Office.context.mailbox.item.from);
  console.log(sender);
  console.log(sender.emailAddress);
  console.log(subject);
  console.log(Office.context.mailbox.item);
  Office.context.mailbox.item.notificationMessages.addAsync("subject", {
    type: "informationalMessage",
    icon: "blue-icon-16",
    message: "Subject: " + subject,
    persistent: false
  });
  
  event.completed();
}

// Gets the item class of the item and displays it in the info bar.
function getItemClass(event) {
  var itemClass = Office.context.mailbox.item.itemClass;
  
  Office.context.mailbox.item.notificationMessages.addAsync("itemClass", {
    type: "informationalMessage",
    icon: "red-icon-16",
    message: "Item Class: " + itemClass,
    persistent: false
  });
  
  event.completed();
}

// Gets the date and time when the item was created and displays it in the info bar.
function getDateTimeCreated(event) {
  var dateTimeCreated = Office.context.mailbox.item.dateTimeCreated;
  
  Office.context.mailbox.item.notificationMessages.addAsync("dateTimeCreated", {
    type: "informationalMessage",
    icon: "red-icon-16",
    message: "Created: " + dateTimeCreated.toLocaleString(),
    persistent: false
  });
  
  event.completed();
}

// Gets the ID of the item and displays it in the info bar.
function getItemID(event) {
  // Limited to 150 characters max in the info bar, so 
  // only grab the first 50 characters of the ID
  var itemID = Office.context.mailbox.item.itemId.substring(0, 50);
  
  Office.context.mailbox.item.notificationMessages.addAsync("itemID", {
    type: "informationalMessage",
    icon: "red-icon-16",
    message: "Item ID: " + itemID,
    persistent: false
  });
  
  event.completed();
}

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