function clearInput() {
    document.getElementById('usernameInput').value = '';
    document.getElementById('usernameInput').disabled = false;
    $('#btn_clear').hide();
}

document.getElementById('usernameInput').addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        var username = document.getElementById('usernameInput').value;
        if (validateInput(username)) {
            run(username);
        }
    }
});

document.getElementById('usernameInputBtn').addEventListener('click', function () {
    var username = document.getElementById('usernameInput').value;
    if (validateInput(username)) {
        run(username);
    }
});

function validateInput(username) {
    var regex = /^[a-zA-Z0-9_]+$/;

    if (regex.test(username)) {
        document.getElementById('usernameInError').innerText = "";
        return true;
    } else {
        document.getElementById('usernameInError').innerText = "These are not the characters you're looking for.";
        return false;
    }
}

function run(input) {
    $('#inputScreen').hide();
    $('#loadingScreen').show();

    console.log(input)

    var ajaxOptions = {
        type: 'POST',
        url: '/process',
        data: { 'username': input },
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',  // Change content type if not a file
        processData: true,
        success: function (response) {
            $('#loadingScreen').hide();
            display(response);
        },
        error: function (error) {
            console.error(`Error `, error);
        }
    };

    $.ajax(ajaxOptions);
}

function display(data) {
    var resultContainer = $('#result-container');
    resultContainer.empty();

    for (var i = 0; i < data.length; i++) {
        var listItem = $('<li>').text(data[i].title);
        resultContainer.append(listItem);
    }
}
