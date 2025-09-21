const fetchConfig = {
    headers: {
        'Content-Type': 'application/json'
    }
}
let id = 0
const link = 'http://127.0.0.1:8000/post/'
const buttonElement = document.querySelector('.fetch_button');
const fetchTemplate = document.querySelector('#template_fetch_result').content.querySelector('.fetch_item')
const fetchList = document.querySelector('.fetch_list')

const getResponseData = (res) => {
    if (res.ok) {
        return res.json()
    } else {
        Promise.reject(`Ошибока запроса на сервер : ${res.status}`)
    }
}

async function getInfo(link) {
    return fetch(link + id + '/', {
        headers: fetchConfig.headers,
        method: 'GET',
    })
    .then((res) => getResponseData(res))
    .then((res) => {
        const takedTemplate = fetchTemplate.cloneNode(true)
        id += 1
        const fetchContent = takedTemplate.querySelector('.fetch_result_json')
        fetchContent.textContent = res.body
        fetchList.append(takedTemplate)
    })
}

buttonElement.addEventListener('click', () => {
    getInfo(link)
});