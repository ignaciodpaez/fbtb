
let fbCtx = {
    playersHtml: [],
    playersHtmlIndex: 0,
}

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
                    fbCtx.playersHtml.push(html);
                }
                boxEl.style.display = 'block';
                boxEl.innerHTML = html;
            })
    });
}

function handleToggleClubsBox() {
    const boxEl = document.querySelector('.jsClubsBox');
    boxEl.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('jsRemoveClubsBtn')) {
            const btnEl = document.querySelector('.jsRemoveClubsBtn');
            const fsEl = btnEl.closest('fieldset');
            fsEl.disabled = true;
        }
    });
}

function handleAddPlayer() {
    const btnEl = document.querySelector('.jsAddPlayerBtn');
    btnEl.addEventListener('click', function (e) {
        const selectors = '.jsPlayersBox input[type="checkbox"]:checked';
        var checkedCheckboxes = document.querySelectorAll(selectors);
        checkedCheckboxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            var clonedRow = row.cloneNode(true);
            clonedRow.id = "newID_" + Math.random().toString(36).substr(2, 9);
            var destinationTableBody = document.getElementById("alineation");
            destinationTableBody.appendChild(clonedRow);
        });
    });
}

function handlePrevPlayersTable() {
    const btnEl = document.querySelector('.jsPrevBtn');
    btnEl.addEventListener('click', function (e) {
        const boxEl = document.querySelector('.jsPlayersBox > table');
        fbCtx.playersHtmlIndex -= 1;
        const i = fbCtx.playersHtmlIndex;
        const n = fbCtx.playersHtml.length;
        boxEl.innerHTML = fbCtx.playersHtml.at((i % n + n) % n);
    });

    const nextBtnEl = document.querySelector('.jsNextBtn');
    nextBtnEl.addEventListener('click', function (e) {
        const boxEl = document.querySelector('.jsPlayersBox > table');
        fbCtx.playersHtmlIndex += 1;
        const i = fbCtx.playersHtmlIndex;
        const n = fbCtx.playersHtml.length;
        boxEl.innerHTML = fbCtx.playersHtml.at((i % n + n) % n);
    });
}

function handleClearPlayers() {
    const btnEl = document.querySelector('.jsResetAlinBtn');
    btnEl.addEventListener('click', function (e) {
        const tbodyRef = document.getElementById("alineation");
        tbodyRef.innerHTML = "";
    });
}