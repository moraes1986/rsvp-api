/* Adicionando Novos Associados */

$(document).ready(function() {
    console.log('teste');
    $('#addGuest').click(function() {
        console.log('teste add guest');
        var li = document.createElement('li');
        //var guest_block = document.getElementById('parent_block');
        var newGuest = document.getElementById('parentList');
        console.log(newGuest);
        li.setAttribute('class', 'col-6 list-group-item bg-light');
        li.innerHTML = form_guest;
        newGuest.append(li);
        
    });
}
);

/* Removendo Convidados Associados */
function removeGuest(value) {
    
    console.log(value);

    var list = formGuest.getElementsByTagName('li');
    for (let i = 0; i < list.length; i++) {
        if (list.item(i).getElementsByTagName('input').namedItem('fullname').value === value) {
            list.item(i).remove();
            console.log('remove guest: ' + value + ' - ' + i);
        }else {
            if (list.item(i).getElementsByTagName('input').namedItem('fullname').value === '') {
                list.item(i).remove();
            }
        }
    }
}

/* Payload do Convidado */
async function confirmGuest() {
    var form = document.getElementById('formGuest');
    var id = form.getElementsByTagName('input').namedItem('id').value;
    var guestList = [];
    console.log('confirm guest: '+ id);

    if(form.getElementsByTagName('li').length > 0) {
        for (let i = 0; i < form.getElementsByTagName('li').length; i++) {
            var guest;
            console.log('form.getElementsByTagName: ' + form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value);
            if (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child') !== null) {
                if (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child').checked === true) {
                               
                    guest = {
                        fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                        confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                        is_child: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child').checked,
                        child_age: parseInt(form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('child_age').value),
                        confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed_at').value:"",
                        updated_at: new Date().toJSON(),
                    }
                }else {
                    guest = {
                        fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                        confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                        is_child: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child').checked,
                        confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed_at').value:"",
                        updated_at: new Date().toJSON(),
                    }
                }
            }else {
                guest = {
                    fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                    confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                    is_child: false,
                    confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed_at').value:"",
                    updated_at: new Date().toJSON(),
                }
            }    

            guestList.push(guest);
        }
    }

    var payload = {
        //_id: form.getElementsByTagName('input').namedItem('_id').value,
        code: parseInt(form.getElementsByTagName('input').namedItem('code').value),
        fullname: form.getElementsByTagName('input').namedItem('fullname').value,
        email: form.getElementsByTagName('input').namedItem('email').value,
        phone: parseInt(form.getElementsByTagName('input').namedItem('phone').value.replace(/[\s\W]/gm,'')),
        confirmed: form.getElementsByTagName('input').namedItem('confirmed').checked,
        is_child: false,
        confirmed_at: (form.getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('input').namedItem('confirmed_at').value:"",
        updated_at: new Date().toJSON(),
        parentList: guestList,
    }

    
    let response;
    await postGuestConfirme(JSON.stringify(payload)).then(res => {
        response = res;
    }
    );


    if (response.status != 200) {
        console.log('response2: ' + JSON.parse(response.responseText));
        document.getElementById('error').innerHTML = JSON.parse(response.responseText).message;
        document.getElementById('error').removeAttribute('hidden');
    }else {
        window.location.href = '/list_guests';
        //document.getElementById('success').innerHTML = JSON.parse(response.responseText).message;
        //document.getElementById('success').removeAttribute('hidden');
        //document.getElementById('formGuest').setAttribute('hidden', true);
    }

}

/* Adicionar Novos Convidados */
async function addGuest() {
    var form = document.getElementById('formGuest');
    var sfullname = form.getElementsByTagName('input').namedItem('fullname').value;
    var guestList = [];
    console.log('confirm guest: '+ sfullname);

    if(form.getElementsByTagName('li').length > 0) {
        for (let i = 0; i < form.getElementsByTagName('li').length; i++) {
            var guest;
            console.log('form.getElementsByTagName: ' + form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value);
            if (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child') !== null) {
                if (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child').checked === true) {
                               
                    guest = {
                        fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                        confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                        is_child: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child').checked,
                        child_age: parseInt(form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('child_age').value),
                        confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed_at').value:"",
                        updated_at: new Date().toJSON(),
                    }
                }else {
                    guest = {
                        fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                        confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                        is_child: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('is_child').checked,
                        confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed_at').value:"",
                        updated_at: new Date().toJSON(),
                    }
                }
            }else {
                guest = {
                    fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                    confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                    is_child: false,
                    confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed_at').value:"",
                    updated_at: new Date().toJSON(),
                }
            }    

            guestList.push(guest);
        }
    }

    var payload = {
        //_id: form.getElementsByTagName('input').namedItem('_id').value,
        fullname: form.getElementsByTagName('input').namedItem('fullname').value,
        email: form.getElementsByTagName('input').namedItem('email').value,
        phone: parseInt(form.getElementsByTagName('input').namedItem('phone').value.replace(/[\s\W]/gm,'')),
        confirmed: form.getElementsByTagName('input').namedItem('confirmed').checked,
        is_child: false,
        confirmed_at: (form.getElementsByTagName('input').namedItem('confirmed').checked===true)?form.getElementsByTagName('input').namedItem('confirmed_at').value:"",
        updated_at: new Date().toJSON(),
        parentList: guestList,
    }

    
    let response;
    await postAddGuest(JSON.stringify(payload)).then(res => {
        response = res;
    }
    );


    if (response.status != 200) {
        console.log('response2: ' + JSON.parse(response.responseText));
        document.getElementById('error').innerHTML = JSON.parse(response.responseText).message;
        document.getElementById('error').removeAttribute('hidden');
    }else {
        window.location.href = '/list_guests';
        //document.getElementById('success').innerHTML = JSON.parse(response.responseText).message;
        //document.getElementById('success').removeAttribute('hidden');
        //document.getElementById('formGuest').setAttribute('hidden', true);
    }

}

/* Confirmar convidado */
function postGuestConfirme(payload) {

    console.log('payload: ' + payload);
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/api/v1/guest/confirm', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(payload);
       

    return new Promise((resolve, reject) => {
        xhr.onload = function() {
            if (xhr.status === 200 && xhr.readyState === 4) {
                resolve(xhr);
            } else {
                reject(xhr);
            }
        }
    }
    );
}


form_guest = '<div> \
                <label for="fullname">Nome</label> \
                <align class="float-right"> \
                  <a href="#" class="btn btn-danger" name="removeGuest" id="removeGuest" onclick="removeGuest(\'{{ parent.fullname }}\')">Remover</a> \
                </align> \
                <input type="text" class="form-control" name="fullname" value="" placeholder="Nome"> \
              </div> \
              <div> \
                <label for="confirmed">Confirmado</label> \
                <input type="checkbox" class="form-control" name="confirmed"  /> \
              </div> \
              <div> \
                <label for="confirmed_at">Data de Confirmação</label> \
                <input type="datetime-local" class="form-control" name="confirmed_at" value="" placeholder="Data de Confirmação"> \
              </div> \
              <div> \
                <label for="is_child">Criança</label> \
                <input type="checkbox" class="form-control" name="is_child"  /> \
              </div>   \
              <div> \
                <label for="child_age">Idade</label> \
                <input type="number" class="form-control" name="child_age" value="" placeholder="Idade"> \
              </div>';
