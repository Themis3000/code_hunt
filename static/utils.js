function epochToReadable(element, includeRelative=true) {
    element.each(function() {
        let dateStr = "";
        let moment_time = moment($(this).text(), "X");
        dateStr += moment_time.format("MMMM Do YYYY, h:mm a");
        if (includeRelative) {
            dateStr +=  ` (about ${moment_time.fromNow()})`
        }
        $(this).text(dateStr);
    });
}