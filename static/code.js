const con_elements = document.getElementsByClassName("con_time");

// converts all epoch times in table to proper formatted date times
for (let i=0; i < con_elements.length; i++) {
    let moment_time = moment(con_elements[i].innerHTML, "X");
    con_elements[i].innerHTML = `${moment_time.format("MMMM Do YYYY, h:mm a")} (about ${moment_time.fromNow()})`;
}
