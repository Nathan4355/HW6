
//learned onclick=function(this) from here 
//https://www.w3schools.com/jsref/event_onclick.asp
function deleteRow(button) {
    let row = button.parentNode.parentNode;
    let table = button.parentNode.parentNode.parentNode;
    let id = row.id
    table.removeChild(row);
    fetch("/api/contact", {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json"
        }, body: JSON.stringify({ id: id })
    }).then(response => response.json)
}
//stuff to convert form submission as json


const dateEntries = document.querySelectorAll('.date-entry');
function updateCountdown() {
    dateEntries.forEach((dateEntry) => {
        const timeUntil = dateEntry.querySelector('.time-until');
        timeUntil.textContent = "";

        if (Date.parse(dateEntry.textContent) != NaN & dateEntry.textContent != "") {
            const date = new Date(dateEntry.textContent);
            const currentTime = new Date();
            const timeRemaining = date - currentTime;
            if (date < currentTime) {

                timeUntil.textContent = " PAST";
            }
            else {

                const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
                const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
                const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));




                //timeUntil.textContent = new Date(timeRemaining).toString();
                timeUntil.textContent = "  " + days + " days, " + hours + " hours, " + minutes + " minutes, and " + seconds + " seconds left";
            }
        }

    });
}

window.addEventListener("load", updateCountdown);


setInterval(updateCountdown, 1000);

