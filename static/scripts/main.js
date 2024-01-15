document.getElementById('usernameInput').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        var username = document.getElementById('usernameInput').value;
         if (validateInput(username)){
            run(username)
         }
    }
});
document.getElementById('usernameInputBtn').addEventListener('click', function() {
    var username = document.getElementById('usernameInput').value;
    if (validateInput(username)){
        run(username)
     }

});

function validateInput(username) {
    var regex = /^[a-zA-Z0-9_]+$/;

    if (regex.test(username)) {
        document.getElementById('usernameInError').innerText = "";
        return true
    } else {
        document.getElementById('usernameInError').innerText = "These are not the characters you're looking for.";
        return false
    }
}

function run(username){
    $('#inputScreen').hide()
    $('#loadingScreen').show()
    $.ajax({
        type: 'POST',
        url: '/process',
        data: { 'username': username },
        success: function(response) {
            $('#loadingScreen').hide()
            display(response);
        },
        error: function(error) {
            console.error('Error sending data to Flask:', error);
        }
    });
}

function display(data) {
    // Assuming "data" is an array of strings
    var resultContainer = $('#result-container'); // Assuming you have a container element in your HTML

    console.log(data)
    // Clear previous content
    resultContainer.empty();

    // Iterate through the array and append each string to the container
    for (var i = 0; i < data.length; i++) {
        var listItem = $('<li>').text(data[i].title);
        resultContainer.append(listItem);
    }
}
