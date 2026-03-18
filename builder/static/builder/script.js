
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
            const rows = document.querySelectorAll('#alineation tr');
            const rowsLen = rows.length;
            const emptyRows = document.querySelectorAll('#alineation tr.fb-js-empty');
            if (rowsLen >= 11 && emptyRows.length === 0) {
                const targetRow = rows[10];
                const emptyRow = document.createElement('tr');
                emptyRow.innerHTML = '<td colspan="10">&nbsp;</td>';
                targetRow.parentNode.insertBefore(emptyRow, targetRow.nextSibling);
                emptyRow.classList.add('fb-js-empty', 'fb-table-squad', 'fb-row-empty');
            }
            const row = checkbox.closest('tr');
            var clonedRow = row.cloneNode(true);
            clonedRow.id = "newID_" + Math.random().toString(36).substr(2, 9);
            var destinationTableBody = document.getElementById("alineation");
            destinationTableBody.appendChild(clonedRow);
            checkbox.checked = false;
            clonedRow.querySelector('input[type="checkbox"]').checked = false;
            clonedRow.querySelector('.fb-js-player-btn-group').style.display = 'block';
        });
    });
}

function handlePrevPlayersTable() {
    const btnEl = document.querySelector('.jsPrevBtn');
    btnEl.addEventListener('click', function (e) {
        if (fbCtx.playersHtml.length === 0) {
            return;
        }
        const boxEl = document.querySelector('.jsPlayersBox > table');
        fbCtx.playersHtmlIndex -= 1;
        const i = fbCtx.playersHtmlIndex;
        const n = fbCtx.playersHtml.length;
        boxEl.innerHTML = fbCtx.playersHtml.at((i % n + n) % n);
    });

    const nextBtnEl = document.querySelector('.jsNextBtn');
    nextBtnEl.addEventListener('click', function (e) {
        if (fbCtx.playersHtml.length === 0) {
            return;
        }
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

function handleClearPlayers() {
    const btnEl = document.querySelector('.jsResetAlinBtn');
    btnEl.addEventListener('click', function (e) {
        const tbodyRef = document.getElementById("alineation");
        tbodyRef.innerHTML = "";
    });
}

function handlePlayerBtn() {
    const squadEl = document.getElementById('alineation');
    squadEl.addEventListener('click', function (e) {

        const emptyRow = squadEl.querySelector('tr.fb-js-empty');
        if (emptyRow) {
            emptyRow.remove();
        }
        
        const row = e.target.closest('tr');
        
        if (e.target.classList.contains('js-up-btn')) {
            const prev = row.previousElementSibling;
            if (prev) row.parentNode.insertBefore(row, prev);
        } 
    
        else if (e.target.classList.contains('js-down-btn')) {
            const next = row.nextElementSibling;
            if (next) row.parentNode.insertBefore(next, row);
        } 
        
        else if (e.target.classList.contains('js-remove-btn')) {
            row.remove();
        }

        const rows = squadEl.querySelectorAll('tr');
        const emptyRowAfter = squadEl.querySelector('tr.fb-js-empty');
        if (rows.length > 11 && !emptyRowAfter) {
            const targetRow = rows[10];
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = '<td colspan="10">&nbsp;</td>';
            targetRow.parentNode.insertBefore(emptyRow, targetRow.nextSibling);
            emptyRow.classList.add('fb-js-empty', 'fb-table-squad', 'fb-row-empty');
        }
    });
}

function handleSwapPlayers() {
    const btnEl = document.querySelector('.js-swap-btn');
    btnEl.addEventListener('click', function (e) {
        const checkedBoxes = document.querySelectorAll('#alineation input[type="checkbox"]:checked');

        if (checkedBoxes.length !== 2) {
            return;
        }

        const row1 = checkedBoxes[0].closest('tr');
        const row2 = checkedBoxes[1].closest('tr');

        const tempMarker = document.createElement('div');
        row1.parentNode.insertBefore(tempMarker, row1);

        row2.parentNode.insertBefore(row1, row2);

        tempMarker.parentNode.insertBefore(row2, tempMarker);

        tempMarker.remove();
        checkedBoxes[0].checked = false;
        checkedBoxes[1].checked = false;
    });
}

function handleSaveSquad() {
    const formEl = document.querySelector('.fb-js-save-squad');
    formEl.addEventListener('submit', function (e) {
        e.preventDefault();
        const squadName = prompt("Enter squad name:");
        if (!squadName) {
            return;
        }
        const rows = document.querySelectorAll('#alineation tr');
        const players = [];
        rows.forEach(row => {
            const playerId = row.getAttribute('data-playerid');
            const clubId = row.getAttribute('data-clubid');
            const seasonId = row.getAttribute('data-seasonid');
            if (playerId && clubId && seasonId) {
                players.push({
                    id: playerId,
                    club_id: clubId,
                    season_id: seasonId,
                });
            }
        });

        fetch(formEl.getAttribute('action'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: squadName,
                players: players,
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving the squad.');
        });
    });
}

function handleFindSquad() {
    const formEl = document.querySelector('.fb-js-find-squad');
    formEl.addEventListener('submit', function (e) {
        e.preventDefault();
        const squadName = formEl.querySelector('input[name="squad_name"]').value;
        if (!squadName) {
            return;
        }
        const url = formEl.getAttribute('action') + "?" + new URLSearchParams({ squad_name: squadName });
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const tableEl = document.querySelector('.fb-squad-list');
                tableEl.style.display = 'block';
                tableEl.innerHTML = html;
            })
    });
}

function handleShowSquad() {
    const tableEl = document.querySelector('.fb-squad-list');
    tableEl.addEventListener('click', function (e) {
        if (!e.target.classList.contains('js-show-squad-btn')) {
            return;
        }
        e.preventDefault();
        const formEl = e.target.closest('form');
        formData = new FormData(formEl);
        const url = formEl.getAttribute('action') + "?" + new URLSearchParams(formData);
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const tableEl = document.querySelector('#alineation');
                tableEl.style.display = 'block';
                tableEl.innerHTML = html;
                btnGroupEl = document.querySelectorAll('.fb-js-player-btn-group');
                btnGroupEl.forEach(btn => {
                    btn.style.display = 'block';
                });
            })
    });
}