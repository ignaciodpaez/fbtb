
function handleFetchClubsEv() {
    const competitionFormEl = document.querySelector('.jsCompetitionForm');
    competitionFormEl.addEventListener('submit', function (e) {
        e.preventDefault();
        const submitter = e.submitter;
        const actionUrl = submitter.getAttribute("formaction") || this.action;
        const formData = new FormData(this, submitter);
        // formData.append('action', 'getnations');
        // const url = this.getAttribute('action') + "?" + new URLSearchParams(formData);
        const url = actionUrl + "?" + new URLSearchParams(formData);
        fetch(url)
            .then(response => response.text())
            .then(html => {
                let boxEl = null;
                if (submitter.value === "getclubs") {
                    boxEl = document.querySelector('.jsClubsBox');
                } else if (submitter.value === "getnations") {
                    boxEl = document.querySelector('.jsNationsBox');
                } else if (submitter.value === "getplayers") {
                    boxEl = document.querySelector('.jsPlayersBox > table');
                }
                boxEl.style.display = 'block';
                boxEl.innerHTML = html;
            })
    });
}