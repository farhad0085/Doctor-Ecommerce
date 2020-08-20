STORAGE_TOKEN = "gd_token"
STORAGE_USER_ID = "gd_user_id"

function getuser(data_handler){
    var xhr = new XMLHttpRequest();
    tag("Returning",localStorage.getItem(STORAGE_TOKEN))
    if(localStorage.getItem(STORAGE_TOKEN)==null){
        return
    }
    var str = localStorage.getItem(STORAGE_TOKEN)+":"+"null";

    formData = btoa(str)
    print("formdata: "+formData)
    print("api host:"+api_host)
    xhr.open("GET", api_host+'/api/get/user/'+localStorage.getItem(STORAGE_USER_ID), true); //basics.js->api_host
    xhr.setRequestHeader("Authorization", "Basic " + formData)
    // xhr.setRequestHeader('Content-Type', 'Basic base64 encoded string');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            // print(xhr.responseText)
            var jData = JSON.parse(xhr.responseText)

            // print(jData)
            // tag("token",xhr.responseText);
            // tag("jData",jData[1]["message"])
            data_handler(jData)
            // if(jData["token"]!=""){
            //     // window.open(web_host+"/index.html","_self")
            // }
        }
    }
    xhr.send();
}