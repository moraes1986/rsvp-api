// Confirm guest

// phone mask
const handlePhone = (event) => {
    let input = event.target
    input.value = phoneMask(input.value)
  }
  
  const phoneMask = (value) => {
    if (!value) return ""
    value = value.replace(/\D/g,'')
    value = value.replace(/(\d{2})(\d)/,"($1) $2")
    value = value.replace(/(\d)(\d{4})$/,"$1-$2")
    return value
  }


/* Construir formulário de convidado */  
const setGuestForm = (guest) => {
    console.log('guest: ' + guest._id.$oid);
    document.getElementById('_id').value = guest._id.$oid;
    document.getElementById('code').value = guest.code;
    document.getElementById('fullname').value = guest.fullname;
    document.getElementById('email').value = guest.email;
    document.getElementById('phone').value = guest.phone;
    document.getElementById('confirmed').checked = guest.confirmed;
    var listParent = document.getElementById('parentList');
    if (guest.parentList.length > 0) {
        
        for (let i = 0; i < guest.parentList.length; i++) {
            const li = document.createElement('li');
            console.log('guest.parent[i].fullname: ' + guest.parentList[i].fullname);
            var confirmed;
            var is_child;

            if(guest.parentList[i].confirmed === true) {
                confirmed = 'checked';
            }else {
                confirmed = '';
            }

            li.innerHTML =  '<div class="form-group">\
                                <label for="fullname" >Nome</label> \
                                <input type="text" class="form-control" style="width: 300px;" name="fullname" id="fullname" value="' + guest.parentList[i].fullname + '" disabled>' + 
                            '</div>' +
                            '<div class="form-group">\
                                <label for="confirmed" class="col-md-3">Confirmar?</label> \
                                <div class="col-md-1"> \
                                    <input type="checkbox" class="form-control"  name="confirm" id="confirmed" ' + confirmed + ' > \
                                </div> \
                            </div>';
            if(guest.parentList[i].is_child === true) {
                is_child = 'checked';
                li.innerHTML += '<div class="form-group row-md-2">\
                                    <label for="is_child" class="col-md-3">É Criança?</label> \
                                    <div class="col-md-1"> \
                                        <input type="checkbox" class="form-control"  name="is_child" id="is_child" ' + is_child + ' > \
                                    </div> \
                                </div><br><br>  \
                                <div class="form-group">\
                                    <label for="child_age" >Idade</label> \
                                    <input type="number" class="form-control" style="width: 150px;" name="child_age" id="child_age" value=' + guest.parentList[i].child_age + ' >\
                                </div>';
                                //'<input type="checkbox" class="form-control" name="is_child" id="is_child" value=' + guest[0].parentList[i].is_child + ' disabled>' +
                                //'<input type="number" class="form-control" name="child_age" id="child_age" value=' + guest[0].parentList[i].child_age + '>';
            }

            li.innerHTML += '<br><br>';
            
         
            listParent.appendChild(li);
            
        }
        
    }
}

/* Confirmar convidado */
function postGuestConfirme(payload) {
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', 'api/v1/guest/confirm', true);
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


/* Localizar convidado por ID */
function getGuestId(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    console.log('established connection');
    var response;

    xhr.onload = function() {
        response = xhr.responseText;
        console.log('Response1: ' + response);
        if (xhr.status === 200 && xhr.readyState === 4) {
            
            console.log('Response: ' + response);
        }
        else {
            console.log('Response: ' + response);
        }
    
    }
    xhr.send();
    console.log('Response3: ' + response);
    return response;
}

/* Payload do Convidado */
async function confirmGuest() {
    var form = document.getElementById('formGuest');
    var id = form.getElementsByTagName('input').namedItem('_id').value;
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
                        confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?new Date().toJSON():"",
                        updated_at: new Date().toJSON(),
                    }
                }
            }else {
                guest = {
                    fullname: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('fullname').value,
                    confirmed: form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked,
                    is_child: false,
                    confirmed_at: (form.getElementsByTagName('li').item(i).getElementsByTagName('input').namedItem('confirmed').checked===true)?new Date().toJSON():"",
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
        confirmed_at: (form.getElementsByTagName('input').namedItem('confirmed').checked===true)?new Date().toJSON():"",
        updated_at: new Date().toJSON(),
        parentList: guestList,
    }

    console.log('payload: ' + JSON.stringify(payload) + ' - ' + form.getElementsByTagName('input').namedItem('phone').value.replace(/[\s\W]/gm,''));
    let response;
    await postGuestConfirme(JSON.stringify(payload)).then(res => {
        response = res;
    }
    );
    
    console.log('response1: ' + JSON.parse(response.responseText).message + " - " + response.status);

    if (response.status != 200) {
        console.log('response2: ' + JSON.parse(response.responseText));
        document.getElementById('error').innerHTML = JSON.parse(response.responseText).message;
        document.getElementById('error').removeAttribute('hidden');
    }else {
        document.getElementById('success').innerHTML = JSON.parse(response.responseText).message;
        document.getElementById('success').removeAttribute('hidden');
        document.getElementById('formGuest').setAttribute('hidden', true);
    }

}

/* Evento de clique no botão de confirmação */
document.addEventListener('DOMContentLoaded', function() {

  var confirmButton = document.getElementById('confirm');
 
    if (confirmButton) {
        confirmButton.addEventListener('click', function() {
            var form = document.getElementById('bookingForm');
            console.log("result: " + form.getElementsByTagName('input').namedItem('id').value);
            var guestId = form.getElementsByTagName('input').namedItem('id');
            var url = 'api/v1/guest/id?id=' + guestId.value;
            var ret = getGuestId(url);
            
            var result = document.getElementById('error');
            var response = JSON.parse(ret);
            
            console.log('Message: ' +  response);
            
            if (!response.message) {
                if( response.code > 0){
                    document.getElementById('formGuest').removeAttribute('hidden'); 
                    setGuestForm(response);
                    document.getElementById('bookingForm').setAttribute('hidden', true);
                }else {
                    result.innerHTML = ret.message;
                    document.getElementById('error').removeAttribute('hidden')
                    
                }
                console.log('exibir form');
                

            } else {
                console.log('exibir erro');
                result.innerHTML = 'Hóspede não encontrado';
                document.getElementById('error').removeAttribute('hidden')
                

            }
            document.getElementById('fullname').focus();



        });    
    }
  
});
