// index.js



function Sign_In () {

    $('#username2').val('');                                                        // Clear out info for new input
    $('#password2').val('');                                                        // Clear out info for new input
    $(".Sign_In_alert").empty();                                                 // empty any alerts from previous use of Modal

    $('#Sign_In_Modal').on('shown', function() {
        $("#username2").focus();                                           //Bring focus username field in the sign up modal
    });
}




// Sign in Submit Button
//
//
$(document).on("click","#Sign_In_Submit_Modal_Button", function  () {
    var $Sign_In_Msg_Tag = "#Sign_In_Msg_Tag";
    var $Sign_In_alert = ".Sign_In_alert";                          // class of all the Sign in alert messages

    var $username2 = "#username2";
    var $password2 = "#password2";
    var hasError = false;
    var username = $($username2).val();
    var password = $($password2).val();
    var remember_me = $("#remember_me").prop('checked');

    $($Sign_In_alert).empty();                                    // clear out any alerts on incorrect data input
    $($Sign_In_Msg_Tag).empty();                                   // clear out 'incorrect username or Password message

    if (username == '') {
        $($username2).focus();
        $($username2).after('<span class="Sign_In_alert"><font color = "#ff0000"> Enter a username</font></span>');
        hasError = true;

    } else if (password == '') {
            $($password2).focus();
            $($password2).after('<span class="Sign_In_alert"><font color = "#ff0000"> Enter a password</font></span>');
            hasError = true;
        }

    if(hasError == false) {                                            // No errors in Sign In form
        $($username2).blur();
        $($password2).blur();

        $.ajax({                                                       // Check authentication and sign in
            'async': true,
            'type':'post',
            'data': {'username':username,'password':password, 'remember_me':remember_me},
            'url': 'Sign_In_View',
            'success': function (hasAccount) {                        // callback return TRUE if has an account or False
                if (hasAccount) {                                   // Account does exist
                    window.location = '/pointtracker';              // Move user to main page
                }
                else {
                    $("#Sign_In_Msg_Tag").after('<span class="Sign_In_alert"><font color = "#ff0000">Incorrect Username or Password</font></span>');
                }
            }
        });
    }
});










function Register () {

    $('#firstname').val('');                                // Clear out info for new input
    $('#lastname').val('');
    $('#username').val('');
    $('#password').val('');
    $('#password_confirm').val('');

    $(".Register_alert").empty();                            // Hide any alerts from previous use of Modal

    $('#Register_Modal').on('shown', function() {
        $("#firstname").focus();                             //Bring focus username field in the sign up modal
    });
}





// Register Submit Button
//
//
$(document).on("click","#Register_Submit_Modal_Button", function  () {

    var $Register_Msg_Tag = '#Register_Msg_Tag';
    var $Register_alert = '.Register_alert';

    var $firstname = "#firstname";
    var $lastname = "#lastname";
    var $username = "#username";
    var $password = "#password";
    var $password_confirm = "#password_confirm";
//    var $email = "#email";
//    var $email_confirm = "#email_confirm";
    var remember_me = $("#remember_me2").prop('checked');

    $($Register_alert).empty();                                                 // hide anything that has class error (.error)
    $($Register_Msg_Tag).empty();                                   // clear out 'incorrect username or Password message

    var hasError = false;

    var firstname = $($firstname).val();
    var lastname = $($lastname).val();
    var username = $($username).val();
    var password = $($password).val();
    var password_confirm = $($password_confirm).val();
//    var email = $($email).val();
//    var email_confirm = $($email_confirm).val();

//    var password = 'mrsfatboy';
//    var password_confirm = 'mrsfatboy';
//    var firstname = 'Melissa';
//    var lastname =  'Coe';
//    var username = 'melissacoe';
//    var email = 'melissacoe@sbcglobal.net';
//    var email_confirm = 'melissacoe@sbcglobal.net';


    if (firstname == '') {
        $($firstname).focus();
        $($firstname).after('<span class="Register_alert"><font color = "#ff0000"> Enter your first name</font></span>');
        hasError = true;
    } else if (lastname == '') {
        $($lastname).focus();
        $($lastname).after('<span class="Register_alert"><font color = "#ff0000"> Enter your last name</font></span>');
        hasError = true;
    } else if (username == '') {
        $($username).focus();
        $($username).after('<span class="Register_alert"><font color = "#ff0000"> Enter a username</font></span>');
        hasError = true;
    } else if (password == '') {
        $($password).focus();
        $($password).after('<span class="Register_alert"><font color = "#ff0000"> Enter a password</font></span>');
        hasError = true;
    } else if (password.length <  8 || password.length > 32) {
        $($password).focus();
        $($password).after('<span class="Register_alert"><font color = "#ff0000"> Must be between 8 and 32 chars.</font></span>');
        hasError = true;
    } else if (password_confirm == '') {
        $($password_confirm).focus();
        $($password_confirm).after('<span  class="Register_alert"><font color = "#ff0000"> Enter a password</font></span>');
        hasError = true;
    } else if (password != password_confirm ) {
        $($password_confirm).focus();
        $($password_confirm).after('<span class="Register_alert"><font color = "#ff0000"> Passwords do not match</font></span>');
        hasError = true;
    }

//    else if (email == '') {
//        $($email).after('<span class="error"><font color = "#ff0000"> Enter an email</font></span>');
//        hasError = true;
//    } else if (email_confirm == '') {
//        $($email_confirm).after('<span  class="error"><font color = "#ff0000"> Re - enter the email</font></span>');
//        hasError = true;
//    } else if (email != email_confirm ) {
//        $($email_confirm).after('<span class="error"><font color = "#ff0000"> Emails do not match</font></span>');
//        hasError = true;
//    }


    if(hasError == false) {                                            // No errors in Register form

    $($firstname).blur();
    $($lastname).blur();
    $($username).blur();
    $($password).blur();
    $($password_confirm).blur();

        $.ajax({                                                       // Check for existing account
            'async': true,
            'type':'post',
            'data': {'firstname':firstname,'lastname':lastname, 'username':username,'password':password, 'remember_me':remember_me},
            'url': 'Register_View',
            'success': function (hasAccount) {                        // callback return TRUE if has an account or False
                if (hasAccount) {                                       // Account already exists
                    $("#Register_Msg_Tag").after('<span class="error"><font color = "#ff0000">An account with that username and password already exists.</font></span>');
                }
                else {
                    window.location = '/pointtracker';                  // Move user to the main page
                }
            }
        });
    }
});





