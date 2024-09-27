function sendEmail(){
    Email.send({
        SecureToken : "04cb182d-52c7-4443-8204-b5216c1736d3",
        To : "ahmedsamir3bas@gmail.com",
        From : "ahmedsamir3bas@gmail.com",
        Subject : "portfolio email",
        Body : "name:  " + document.getElementById("name").value 
            + "<br> Email:  " + document.getElementById("email").value
            + "<br> message no:  " + document.getElementById("message").value
    }).then(
      message => alert("message sent succesfully")
    );
  }
  