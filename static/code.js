const con_elements = document.getElementsByClassName("con_time");

for (let i=0; i < con_elements.length; i++) {
    let moment_time = moment(con_elements[i].innerHTML, "X");
    con_elements[i].innerHTML = `${moment_time.format("MMMM Do YYYY, h:mm a")} (${moment_time.fromNow()})`;
}
