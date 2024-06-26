document.addEventListener('DOMContentLoaded', function() {

    const find_title_input = document.getElementById('search_input_field')
    const find_title_button = document.getElementById('submit_search_button')

    const search_result_block = document.getElementById('search_result')


    find_title_input.addEventListener('input', () => {
        let title_value = find_title_input.value
        let content = {
            "title": title_value
        }

        let title_data = JSON.stringify(content);

        if (title_value.length >= 3) {
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
                search_result_block.innerHTML = ''

                data['result'].forEach(item => {
                    let new_p = document.createElement("p");

                    new_p.addEventListener('click', () => {
                        find_title_input.value = new_p.innerText
                    })

                    search_result_block.appendChild(new_p)
                    new_p.innerText = item
                }); 
            })
        }
    })


    find_title_button.addEventListener('click', () => {
        let title_value = find_title_input.value
        let content = {
            "title": title_value
        }

        let title_data = JSON.stringify(content);

        fetch('/find_cards/', {
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


})