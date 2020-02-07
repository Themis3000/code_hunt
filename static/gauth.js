function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  console.log(id_token)
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/gtokensignin');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("idtoken", id_token)
  xhr.setRequestHeader("idtoken", id_token)
  xhr.send();
  xhr.onloadend = (e) => {
    console.log('Signed in as: ' + xhr.responseText);
  };
}
