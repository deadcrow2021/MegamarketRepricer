document.addEventListener('DOMContentLoaded', () => {

    const find_title_input = document.getElementById('search_input_field')
    const find_title_button = document.getElementById('submit_search_button')

    const search_result_block = document.getElementById('search_result')
    
    const message_block = document.getElementById('message_block')

    const cards_wrapper_block = document.getElementById('cards_wrapper')
    
    const send_item_prices_button = document.getElementById('submit_items_change_button')


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
            cards_wrapper_block.replaceChildren()
            let result = data["result"]

            for (const key in result) {
                if (result.hasOwnProperty(key)) {
                    let item_data = result[key]
                    add_card_block(
                        item_data['item'],
                        item_data['item_id'],
                        item_data['shop'],
                        item_data['api_key']
                    )
                }
            }
        })
    })


    send_item_prices_button.addEventListener('click', () => {
        let prices_input_blocks = document.getElementsByClassName('card_price_input')

        let content = {
            "data": []
        }

        for (let index = 0; index < prices_input_blocks.length; index++) {
            const price_block = prices_input_blocks[index];
            const input_field = price_block.getElementsByTagName('input')[0]
            
            let value = input_field.value
            let api_key_attr = input_field.getAttribute('api_key')
            let item_id_attr = input_field.getAttribute('item_id')
            let shop_attr = input_field.getAttribute('shop')

            if (value && value > Math.floor('0')) {
                content['data'].push({
                    'price': value,
                    'api_key': api_key_attr,
                    'item_id': item_id_attr,
                    'shop': shop_attr
                })
            }
        }

        let json_data = JSON.stringify(content);

        fetch('/send_prices/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: json_data,
        }).then((response) => {
            return response.json();
        }).then((data) => {
            message_block.replaceChildren()

            let request_results = data['result'] 
            
            for (let index = 0; index < request_results.length; index++) {
                let result = request_results[index]

                if (result['status'] == 0) {
                    for (let index = 0; index < request_results.length; index++) {
                        let result = request_results[index]
        
                        if (result['status'] == 0) {
                            let message = document.createElement("div");
                            message.classList.add('message');
                            message.textContent = `${result['shop']}: ${result['error']}`
                            message_block.appendChild(message)
                        }
                    }
                    break
                }

                let message = document.createElement("div");
                message.classList.add('message');
                message.classList.add('message_ok');
                message.textContent = 'Prices were changed successfully!'
                message_block.appendChild(message)
                break

            }

            setTimeout(() => {
                message_block.replaceChildren()
            }, 20000)
        })
    })


    function add_card_block(item, item_id, shop, api_key) {

        let card_block = document.createElement("div");
        card_block.classList.add('card');
        
        let title_block = document.createElement("div");
        title_block.classList.add('card_title');
        title_block.textContent = item

        let shop_block = document.createElement("div");
        shop_block.classList.add('shop_title');
        shop_block.textContent = shop
        
        let price_input_block = document.createElement("div");
        price_input_block.classList.add('card_price_input');

        let input_field = document.createElement("input");
        input_field.type = "number";
        input_field.step = "1";
        input_field.setAttribute('api_key', api_key);
        input_field.setAttribute('item_id', item_id);
        input_field.setAttribute('shop', shop);

        price_input_block.appendChild(input_field)

        card_block.appendChild(title_block)
        card_block.appendChild(shop_block)
        card_block.appendChild(price_input_block)

        cards_wrapper_block.appendChild(card_block)
    }

})