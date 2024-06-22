const find_title_input = document.getElementById('search_input_field')
const find_title_button = document.getElementById('submit_search_button')

find_title_input.addEventListener('input', () => {
    let content = {
        "title": find_title_input.value
    }

    let title_data = JSON.stringify(content);
    fetch('/get_data/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: title_data,
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log(data)
    })

})