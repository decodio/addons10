

serviceRequest = new Object();





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





function Attach() {
    //var deferred = $.Deferred();

    $.ajax({
        type:"POST",
        url: "/web_outlook_plugin/REST/AttachAttachmentToObject/",
        data: serviceRequest,
        dataType: "json",
        timeout: 200000,
        success: function(result)
        {
            console.log("success!!!!!!!!!");
            console.log(result);
            var respStr = "Adding message success: " + status + " result: " + result;
            var respStr_html = respStr;
        },
        error:function(xhr,status,error){
            console.log("error!!!!!!!!!");
            console.log(error);
            var respStr = "Adding message failed: " + status + " error: " + error;
            var respStr_html = respStr;
        }
    });

    //return deferred.promise();
}

function attachmentTokenCallback(asyncResult, userContext) {
    if (asyncResult.status === "succeeded") {
        // Cache the result from the server.
        serviceRequest.attachmentToken = asyncResult.value;
        serviceRequest.state = 3;
        Attach();
    } else {
        showToast("Error", "Could not get callback token: " + asyncResult.error.message);
    }
};


function AttachAttachmentToObject(item, res_id, res_model) {
    if (!item) {
        return;
    }
    if (!item.attachments) {
        return;
    }
    serviceRequest.attachmentToken = "";
    serviceRequest.res_id = res_id;
    serviceRequest.res_model = res_model;
    serviceRequest.ewsUrl = Office.context.mailbox.ewsUrl;
    serviceRequest.attachments = new Array();
    serviceRequest.attachments_len = item.attachments.length;
    for (var i = 0; i < item.attachments.length; i++) {
        serviceRequest.attachments[i] = new Object();
        serviceRequest.attachments[i].name = item.attachments[i].name;
        serviceRequest.attachments[i].contentType = item.attachments[i].contentType;
        serviceRequest.attachments[i].id = item.attachments[i].id;
    }

    Office.context.mailbox.getCallbackTokenAsync(attachmentTokenCallback);
}



function AttachMessageToObject(item,  model, res_id) {
    var deferred = $.Deferred();

    var subject = item.subject;
    var from = buildEmailAddressString(item.from);
    var to = buildEmailAddressString(item.to);

    item.body.getAsync('html', function(result){
        if (result.status === 'succeeded') {
            body = result.value;
            var _data = {'res_id': Number(res_id),
                'message_body': body,
                'subject': subject,
                'from': from,
                'to': to,
                'model': model,
            };

            AttachAttachmentToObject(item, res_id, model, function() {

            });
            $.ajax({
                type:"POST",
                url: "/web_outlook_plugin/REST/attach_message_to_model/",
                data: _data,
                dataType: "json",
                timeout: 200000,
                success: function(result)
                {
                    _url = result['url'];

                    if (result['status']) {
                        var respStr = "";
                        var respStr_html = "";
                        switch(result['status']) {
                        case "success":
                            respStr = "Message has been added to lead. ";
                            respStr_html = respStr + "<br />Use following URL to view lead:<br />";
                            if (_url) {
                                respStr_html = respStr_html + "<a class='ms-font-weight-regular ms-font-color-themeDark'' href='" + _url + "' target='_blank'>" + _url + "</a>";
                            }
                            deferred.resolve(respStr);
                            break;
                        case "expired":
                            respStr = "Please login to Odoo. ";
                            deferred.reject(respStr);
                            break;
                        default:
                            respStr = result['desc'];
                            deferred.reject(respStr);
                        }
                    } else {
                            deferred.reject("Unknown error!");
                    }
                },
                error:function(xhr,status,error){
                    var respStr = "Adding message failed: " + status + " error: " + error;
                    deferred.reject(respStr);
                }
            });



        } else {
            deferred.reject(result.status);
        }
    });

    return deferred.promise();
}




//
// Create new object of desired model and attach message to it (via AttachMessageToObject call)
//
function AttachMessageToNewObject(item, model) {
    var deferred = $.Deferred();
    var respStr = "";

    var senderAddress = item.sender.emailAddress;
    var senderName = item.sender.displayName;
    var subject = item.subject;

    if (senderAddress) {
        var _data = {'senderAddress': senderAddress,
            'senderName': senderName,
            'name': subject,
            'model': model
        };
        $.ajax({
            type:"POST",
            url: "/web_outlook_plugin/REST/createobject/",
            data: _data,
            dataType: "json",
            timeout: 200000,
            success: function(result) {
                if (result['status']) {
                    switch(result['status']) {
                        case "success":
                            res_id = result['res_id'];
                            respStr = "User " + senderName + "<" + senderAddress + "> has been added as lead. ";
                            var dataAttachMessagePromise = AttachMessageToObject(item, model, res_id);
                            dataAttachMessagePromise.done(function(data){
                                deferred.resolve(data);
                            });
                            dataAttachMessagePromise.fail(function(data){
                                deferred.reject(data);
                            });
                            break;
                        case "expired":
                            respStr = "Please login to Odoo. ";
                            deferred.reject(respStr);
                            break;
                        default:
                        respStr = result['desc'];
                        deferred.reject(respStr);
                    }
                } else {
                    deferred.reject("Unknown error!");
                }
            },
            error:function(xhr,status,error) {
                respStr = "Adding user " + senderName + "<" + senderAddress + "> failed: " + status + " error: " + error;
                deferred.reject("HTTP error: " + xhr.status + " " + respStr);
            }
        });
    } else {
        respStr = "User " + senderName + " does not have a valid email address.";
        deferred.reject(respStr);
    }
    return deferred.promise();
}