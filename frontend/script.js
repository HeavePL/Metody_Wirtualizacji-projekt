const backendurl = 'api';

async function fetchLogs() {
    try {
        const response = await fetch(`${backendurl}/logs`);
        const logs = await response.json();
        const tbody = document.getElementById('table_godziny_zarejestrowane');
        tbody.innerHTML = '';
        logs.forEach(log => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${log.employee_name}</td>
                <td>${log.date}</td>
                <td>${log.start_hour} - ${log.end_hour}</td>
                <td>${log.description || '-' }</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('błąd pobierania danych - ', error);
    }    
}

document.getElementById('form_workDay').addEventListener('submit', async (e) =>{
    e.preventDefault();
    const data = {
        employee_name: document.getElementById('employee_name').value,
        date: document.getElementById('date').value,
        start_hour: document.getElementById('start_hour').value,
        end_hour: document.getElementById('end_hour').value,
        description: document.getElementById('description').value
    };
    console.log(data)
    console.log(JSON.stringify(data))

    try {
        const response = await fetch(`${backendurl}/logs`,{
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(data)
        } );
        if (response.ok){
            document.getElementById('form_workDay').reset();
            fetchLogs();
        } else {
            alert('Błąd zapisu danych');
        }
    } catch (error) {
        console.error('Błąd wysyłania danych - ', error);
    };
})

fetchLogs();