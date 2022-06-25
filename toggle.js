function toggle(elementId,element2Id) {
    var div = document.getElementById(elementId);
    var span = document.getElementById(element2Id);
    if(div.style.display == "block") {
        div.style.display = "none";
        span.style.borderTop = "8px solid #337ab8";
        span.style.borderBottom = "none";
    }
    else {
        div.style.display = "block";
        span.style.borderTop = "none";
        span.style.borderBottom = "8px solid #337ab8";
    }
}


function toggle2(elementId,element2Id) {
    var div = document.getElementById(elementId);
    var span = document.getElementById(element2Id);
    if(div.style.display == "table-row") {
        // window.alert("closing");
        // div.style.display = "none";
        span.style.borderTop = "7px solid #000";
        span.style.borderBottom = "none";
    }
    else {
        // window.alert("opening");
        // div.style.display = "inline-block";
        span.style.borderTop = "none";
        span.style.borderBottom = "7px solid #000";
    }
}
