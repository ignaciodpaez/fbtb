
function handleFetchClubsEv() {
    const competitionFormEl = document.querySelector('.jsCompetitionForm');
    competitionFormEl.addEventListener('submit', function (e) {
        e.preventDefault();
        const submitter = e.submitter;
        const actionUrl = submitter.getAttribute("formaction") || this.action;
        const formData = new FormData(this, submitter);
        formData.append('action', 'getnations');
        // const url = this.getAttribute('action') + "?" + new URLSearchParams(formData);
        const url = actionUrl + "?" + new URLSearchParams(formData);
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const clubsBoxEl = document.querySelector('.jsClubsBox');
                clubsBoxEl.style.display = 'block';
                clubsBoxEl.innerHTML = html;
            })
    });
}

function handleFetchNationsEv() {
    const competitionFormEl = document.querySelector('.jsCompetitionForm');
    competitionFormEl.addEventListener('submit', function (e) {
        e.preventDefault();
        const submitter = e.submitter;
        const actionUrl = submitter.getAttribute("formaction") || this.action;
        const formData = new FormData(this, submitter);
        const url = actionUrl + "?" + new URLSearchParams(formData);
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const clubsBoxEl = document.querySelector('.jsNationsBox');
                clubsBoxEl.style.display = 'block';
                clubsBoxEl.innerHTML = html;
            })
    });
}