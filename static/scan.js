function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return undefined;
}

function encode_cookie_data(code_visits, type_visits, type_unique_visits, type_all_visits, type_all_unique_visits) {
    return code_visits + "|" + type_visits + "|" + type_unique_visits + "|" + type_all_visits + "|" + type_all_unique_visits
}

function decode_cookie_data(cookie_data) {
    return cookie_data.split("|")
}

function replace_var (element_id, var_name, content) {
    document.getElementById(element_id).innerHTML = document.getElementById(element_id).innerHTML.replace("[ " + var_name + " ]", content)
}

function getNumberWithSuffix(n) {
    var s=["th","st","nd","rd"],
    v=n%100;
    return n+(s[(v-20)%10]||s[v]||s[0]);
 }


var params = getUrlVars();

if (typeof params["code"] !== 'undefined') {
    var code_cookie = getCookie("code_" + params["code"]);
    if (typeof code_cookie == 'undefined') {
        //add visit, populate cookie and give api data
        const Http = new XMLHttpRequest();
        Http.open("POST", "/scan");
        Http.setRequestHeader("code", params["code"]);
        Http.setRequestHeader("add", "true");
        Http.send();
        Http.onloadend = (e) => {
            console.log(Http.status)
            console.log(Http.responseText)
            if (Http.status == 200){
                var response = JSON.parse(Http.responseText);
                setCookie("code_" + params["code"], encode_cookie_data(response["code_data"]["uses"], response["type_data"]["visits"], response["type_data"]["unique_visits"], response["type_all_data"]["visits"], response["type_all_data"]["unique_visits"]), 365);
                replace_var("code_find", "type_name", response["code_data"]["type"]);
                replace_var("code_find", "created_number", response["code_data"]["created_number"]);
                replace_var("code_scans", "code_uses", response["code_data"]["uses"]);
                replace_var("new_code_scans", "new_code_uses", getNumberWithSuffix(response["code_data"]["uses"] + 1));
                document.getElementById("centerDivLoading").style.display = "none";
                document.getElementById("centerDivContent").style.display = "block";
                } else {
                    document.getElementById("centerDivLoading").style.display = "none";
                    document.getElementById("centerDivError").style.display = "block";
                }
        }
    } else {
        //give data about code from cookie & api
        const Http = new XMLHttpRequest();
        Http.open("POST", "/scan");
        Http.setRequestHeader("code", params["code"]);
        Http.setRequestHeader("add", "false");
        Http.send();
        Http.onloadend = (e) => {
            var response = JSON.parse(Http.responseText);
            var code_cookie_decoded = decode_cookie_data(code_cookie);
            replace_var("code_find", "type_name", response["code_data"]["type"]);
            replace_var("code_find", "created_number", response["code_data"]["created_number"]);
            replace_var("code_scans", "code_uses", response["code_data"]["uses"]);
            replace_var("new_code_scans", "new_code_uses", getNumberWithSuffix((parseInt(code_cookie_decoded[0]) + 1).toString()));
            document.getElementById("centerDivLoading").style.display = "none";
            document.getElementById("centerDivContent").style.display = "block";
        }
    }
}


//clear params
//var query = window.location.search.substring(1)
//if(query.length) {
//   if(window.history != undefined && window.history.pushState != undefined) {
//        window.history.pushState({}, document.title, window.location.pathname);
//   }
//}