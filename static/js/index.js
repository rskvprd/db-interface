const ADD_SELECTOR = '#addButton';
const sectionButton = document.querySelectorAll('.db-table__tables-item');
const answerTable = document.querySelector('#table')
const addButton = document.querySelector(ADD_SELECTOR)



//============================
//========ADD BUTTON==========
//============================
function listenAddButton() {
    const tableName = document.createElement('input');
    const active = 'db-table__add-button_active';
    tableName.setAttribute('type', 'text');
    tableName.setAttribute('placeholder', 'Введите имя таблицы');
    if (addButton)
        addButton.addEventListener('click', async() => {
            if(!addButton.classList.contains(active)) {
                addButton.after(tableName);
                addButton.classList.add(active);
            }
            else {
                const response = await addNewTable(tableName.value);
                console.log(tableName.value);
                console.log(response)
            }
        });
}

// Send request to backend for add new table
// Return backend response
async function addNewTable(name, url='/admin/add'){
    await fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: name
    })
}
//============================
//============================
//============================





//============================
//==========HEADER============
//============================
//Highlight current url in header
function highlightActiveLink() {
    for (let i = 0; i < document.links.length; i++) {
        if (document.links[i].href !== document.URL) continue;
        document.links[i].classList.add('active-link');
        return true;
    }
    return false;
}
//============================
//============================
//============================



//============================
//======GET TABLE DATA========
//============================
//Fetch table data from backend with table name
function fetchTable(tableName) {
    const url = '/admin';
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: tableName
    })
}
//Adding listener for button with table name in innerHTML for get table data from backend
function addTableNameListener(button, answerTable){
    const tableName = button.innerHTML;
        button.onclick = async () => {
            const response = await fetchTable(tableName);
            if (response.ok){
                answerTable.innerHTML = await response.text();
            }
            console.log(this.innerHTML);
        }
}
//Adding listener for all buttons with selector .table-view__tables-item
function buttonListener(){
    for (const button of sectionButton){
        addTableNameListener(button, answerTable)
    }
}
//============================
//============================
//============================

//INITIALISE
buttonListener();
highlightActiveLink();
listenAddButton();