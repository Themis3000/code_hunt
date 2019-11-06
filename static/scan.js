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

function replace_var (element_id, var_name, content) {
    document.getElementById(element_id).innerHTML = document.getElementById(element_id).innerHTML.replace("[ " + var_name + " ]", content);
}

function getNumberWithSuffix(n) {
    var s=["th","st","nd","rd"],
    v=n%100;
    return n+(s[(v-20)%10]||s[v]||s[0]);
 }

function changeUsername() {
    document.getElementById("username_change").style.display = "none";
    const Http = new XMLHttpRequest();
    Http.open("POST", "/scan");
    Http.setRequestHeader("new_username", document.getElementById("username").value);
    Http.setRequestHeader("id", getCookie("user_id"))
    Http.send();
    Http.onloadend = (e) => {
    }
}

var params = getUrlVars();

//clear params
var query = window.location.search.substring(1)
if(query.length) {
   if(window.history != undefined && window.history.pushState != undefined) {
        window.history.pushState({}, document.title, window.location.pathname);
   }
}


if (typeof params["code"] !== 'undefined') {
    var user = getCookie("user_id");
    const Http = new XMLHttpRequest();
    Http.open("POST", "/scan");
    Http.setRequestHeader("code", params["code"]);
    Http.setRequestHeader("user_id", user);
    Http.send();
    Http.onloadend = (e) => {
        if (Http.status == 200){
            var response = JSON.parse(Http.responseText);
            if (response["new_user"] == true) {
                setCookie("user_id", response["user_data"]["_id"], 1825);
                setCookie("user_id_public", response["user_data"]["public_id"], 1825);
                replace_var("user_stats", "total_scans", 1);
            }
            replace_var("sign_in_link", "username", response["user_data"]["username"]);
            document.getElementById("sign_in_confirmation").style.display = "block";
            if (response["user_data"]["username"] == "guest") {
                document.getElementById("username_change").style.display = "block";
            }
            replace_var("code_find", "type_name", response["code_data"]["type"]);
            replace_var("code_find", "created_number", response["code_data"]["created_number"]);
            replace_var("code_find", "total_amount", response["type_data"]["created_amount"]);
            document.getElementById("sign_in_link").href = "/profile/" + response["user_data"]["public_id"];
            document.getElementById("leaderboards").href = "/leaderboards/" + response["code_data"]["type"];
            document.getElementById("code_more_info").href = "/code/" + response["code_data"]["public_id"];
            if (params["code"] in response["user_data"]["codes"]) {
                replace_var("code_scans", "code_uses", response["code_data"]["uses"]);
                replace_var("new_code_scans", "new_code_uses", getNumberWithSuffix(response["user_data"]["codes"][response["code_data"]["_id"]]["visit_num"]));
                replace_var("user_stats", "total_scans", response["user_data"]["visits_counts"]["ALL"]["visits"]);
            } else {
                replace_var("code_scans", "code_uses", response["code_data"]["uses"]);
                replace_var("new_code_scans", "new_code_uses", getNumberWithSuffix(response["code_data"]["uses"] + 1));
                if ("visits_counts" in response["user_data"]) {
                    replace_var("user_stats", "total_scans", response["user_data"]["visits_counts"]["ALL"]["visits"] + 1);
                } else {
                    replace_var("user_stats", "total_scans", 1);
                }
            }
            document.getElementById("centerDivLoading").style.display = "none";
            document.getElementById("centerDivContent").style.display = "block";
        } else {
            document.getElementById("centerDivLoading").style.display = "none";
            document.getElementById("centerDivError").style.display = "block";
        }
    }
}