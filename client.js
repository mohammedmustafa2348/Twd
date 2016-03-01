const minPassLen = 3;
var view;
var myemail;
var otheremail;

var attachHandlers = function() {
    if (view == "welcomeview") {
        var login = document.getElementById("loginform");

        if (login != null) {
            var loginButton = document.getElementById("btn_login");

            loginButton.addEventListener('click', function () {
                login.setAttribute("onsubmit", "loginForm.login(this);return false;");
            });
        }

        var signup = document.getElementById("signupform");

        if (signup != null) {
            var signupButton = document.getElementById("btn_signup");

            signupButton.addEventListener('click', function () {
                signup.setAttribute("onsubmit", "signupForm.signup(this);return false;");
            });

            var passwordField = document.getElementById("su_password");
            var reapeatPasswordField = document.getElementById("su_reapeatpsw");

            passwordField.addEventListener('keyup', function ()
            {
                if(passwordField.value.length < minPassLen)
                {
                    passwordField.setCustomValidity("Password must be 3-32 characters");
                }
                else
                {
                    passwordField.setCustomValidity('');
                }
            });

            reapeatPasswordField.addEventListener('keyup', function ()
            {
                if(passwordField.value != reapeatPasswordField.value) {
                    reapeatPasswordField.setCustomValidity("Passwords do not match!");
                } else {
                    reapeatPasswordField.setCustomValidity('');
                }
            });
        }
    }

    else if (view == "profileview") {
        var logoutButton = document.getElementById("btn_log_out");
        logoutButton.addEventListener('click', logout.logout);


        var change_psw = document.getElementById("changepswform");
        if (change_psw != null) {
            var change_pswButton = document.getElementById("btn_change_psw");
            change_pswButton.addEventListener('click', function () {
                change_psw.setAttribute("onsubmit", "change_pswForm.change_psw(this);return false;");
            });

            var passwordField = document.getElementById("changepsw_new_psw");
            var reapeatPasswordField = document.getElementById("changepsw_rpt_new_psw");

            passwordField.addEventListener('keyup', function ()
            {
                if(passwordField.value.length < minPassLen)
                {
                    passwordField.setCustomValidity("Password must be 3-32 characters");
                }
                else
                {
                    passwordField.setCustomValidity('');
                }
            });

            reapeatPasswordField.addEventListener('keyup', function ()
            {
                if(passwordField.value != reapeatPasswordField.value) {
                    reapeatPasswordField.setCustomValidity("Passwords do not match!");
                } else {
                    reapeatPasswordField.setCustomValidity('');
                }
            });

        }

        var mywdetails = document.getElementById("mydetails_form");

        if (mywdetails != null) {
            userdataForm.getMyDetails(mywdetails);
        }


        var new_post = document.getElementById("new_post_form");

        if (new_post != null) {
            var postButton = document.getElementById("btn_post");
            postButton.addEventListener('click', function () {
                new_post.setAttribute("onsubmit", "newPostForm.post(this);return false;");
            });
        }

        var mywall = document.getElementById("mywall_form");

        if (mywall != null) {
            var refresh_mywallButton = document.getElementById("btn_refresh_mywall");
            refresh_mywallButton.addEventListener('click', function () {
                mywall.setAttribute("onsubmit", "wallForm.getMessages();return false;");
            });
        }

        var search_user = document.getElementById("search_user_form");

        if (search_user != null) {
            var searchButton = document.getElementById("btn_search");
            searchButton.addEventListener('click', function () {
                search_user.setAttribute("onsubmit", "search_user_form.getUser(this);return false;");
            });
        }

        var otherwall = document.getElementById("otherwall_form");

        if (otherwall != null) {
            var refresh_otherwallButton = document.getElementById("btn_refresh_otherwall");
            refresh_otherwallButton.addEventListener('click', function () {
                otherwall.setAttribute("onsubmit", "otherWallForm.getMessages();return false;");
            });
        }

        var other_new_post = document.getElementById("other_new_post_form");

        if (other_new_post != null) {
            var post_otherButton = document.getElementById("btn_post_other");
            post_otherButton.addEventListener('click', function () {
                other_new_post.setAttribute("onsubmit", "otherNewPostForm.post(this);return false;");
            });
        }
    }
};

var init = function () {
    if (localStorage.getItem("token") == null) {
        document.getElementById("client_body").innerHTML = document.getElementById("welcomeview").innerHTML;
        view = "welcomeview";
    }
    else {
        document.getElementById("client_body").innerHTML = document.getElementById("profileview").innerHTML;
        view = "profileview";
        wallForm.getMessages();
    }
    attachHandlers();
};


window.onload = function(){
    init();
};


//====================================================================================================================================================================================
var loginForm = {

    login: function(formData)
    {
        var email = formData.email.value;
        var in_psw = formData.password.value;
        var result;



        if (in_psw.length >= minPassLen) //Minimum password length
        {
            result = serverstub.signIn(email, in_psw);

            if (result.success == true)
            {
                token = result.data;
                localStorage.setItem("token", token);
                init();
            }
        }

        if (in_psw.length < minPassLen || result.message == "Wrong username or password.")
        {

            var email_field = document.getElementById("li_email_label");
            email_field.style.color = "red";

            var password_field = document.getElementById("li_password_label");
            password_field.style.color = "red";

            var password_field2 = document.getElementById("li_password_label2");
            password_field2.innerHTML = "Wrong username or password";
            password_field2.style.color = "red";
            password_field2.style.fontSize = "x-small";

            formData.password.value = "";
        }
    }

};



var signupForm = {

    signup: function(formData){

        var su_psw = formData.password.value;
        var su_rep_psw = formData.reapeatpsw.value;

        if (su_psw != su_rep_psw || su_psw.length < minPassLen) //rarely activated as the validation is done on the fly
        {
            var password_field = document.getElementById("su_password_label");
            password_field.style.color = "red";

            var repeatpassword_field = document.getElementById("su_reapeatpsw_label");
            repeatpassword_field.style.color = "red";

            var email_field = document.getElementById("su_email_label");
            email_field.style.color = "black";

            var email_field2 = document.getElementById("su_email_label2");
            email_field2.innerHTML = "Passwords do not match!";
            email_field2.style.color = "red";
            email_field2.style.fontSize = "x-small";

            formData.password.value = "";
            formData.reapeatpsw.value = "";
        }
        else
        {
            var newuser = {"email": formData.email.value, "password": formData.password.value, "firstname":formData.firstname.value, "familyname": formData.familyname.value, "gender": formData.gender.value, "city": formData.city.value, "country": formData.country.value};

            var result = serverstub.signUp(newuser);
            if (result.success == true)
            {
                loginForm.login(formData);
            }
            else
            {
                if (result.message == "User already exists.")
                {
                    var password_field = document.getElementById("su_password_label");
                    password_field.style.color = "black";

                    var repeatpassword_field = document.getElementById("su_reapeatpsw_label");
                    repeatpassword_field.style.color = "black";

                    var email_field = document.getElementById("su_email_label");
                    email_field.style.color = "red";

                    var email_field2 = document.getElementById("su_email_label2");
                    email_field2.innerHTML = "User already exists";
                    email_field2.style.color = "red";
                    email_field2.style.fontSize = "x-small";

                    formData.password.value = "";
                    formData.reapeatpsw.value = "";
                }
            }
        }
    }
};


var logout = {
    logout: function(){
        var token = localStorage.getItem("token");
        var result = serverstub.signOut(token);

        if (result.success == true)
        {
            localStorage.removeItem("token");
            init();
        }
        else //not signed in
        {
            localStorage.removeItem("token");
            init();
        }

    }
};


var change_pswForm = {

    change_psw: function(formData){

        var current_psw = formData.changepsw_current_psw.value;
        var psw = formData.changepsw_new_psw.value;
        var rep_psw = formData.changepsw_rpt_new_psw.value;

        if (current_psw.length < minPassLen)
        {
            var currentpassword_field = document.getElementById("changepsw_current_psw_label");
            currentpassword_field.style.color = "red";

            var password_field = document.getElementById("changepsw_new_psw_label");
            password_field.style.color = "black";

            var repeatpassword_field = document.getElementById("changepsw_rpt_new_psw_label");
            repeatpassword_field.style.color = "black";

            var password_field_2 = document.getElementById("changepsw_label");
            password_field_2.innerHTML = "Wrong password";
            password_field_2.style.color = "red";
            password_field_2.style.fontSize = "x-small";
        }
        if (psw != rep_psw) //rarely activated as the validation is done on the fly
        {
            var password_field = document.getElementById("changepsw_new_psw_label");
            password_field.style.color = "red";

            var repeatpassword_field = document.getElementById("changepsw_rpt_new_psw_label");
            repeatpassword_field.style.color = "red";

            var currentpassword_field = document.getElementById("changepsw_current_psw_label");
            currentpassword_field.style.color = "black";

            var password_field_2 = document.getElementById("changepsw_label");
            password_field_2.innerHTML = "Passwords do not match!";
            password_field_2.style.color = "red";
            password_field_2.style.fontSize = "x-small";
        }
        else
        {
            var token = localStorage.getItem("token");
            var result = serverstub.changePassword(token, formData.changepsw_current_psw.value, psw);

            if (result.success == true) {
                formData.reset();

                var currentpassword_field = document.getElementById("changepsw_current_psw_label");
                currentpassword_field.style.color = "black";

                var password_field = document.getElementById("changepsw_new_psw_label");
                password_field.style.color = "black";

                var repeatpassword_field = document.getElementById("changepsw_rpt_new_psw_label");
                repeatpassword_field.style.color = "black";

                var password_field_2 = document.getElementById("changepsw_label");
                password_field_2.innerHTML = "Password has changed successfully";
                password_field_2.style.color = "green";
                password_field_2.style.fontSize = "x-small";
            }
            else {
                if (result.message == "Wrong password.") {
                    var currentpassword_field = document.getElementById("changepsw_current_psw_label");
                    currentpassword_field.style.color = "red";

                    var password_field = document.getElementById("changepsw_new_psw_label");
                    password_field.style.color = "black";

                    var repeatpassword_field = document.getElementById("changepsw_rpt_new_psw_label");
                    repeatpassword_field.style.color = "black";

                    var password_field_2 = document.getElementById("changepsw_label");
                    password_field_2.innerHTML = "Wrong password";
                    password_field_2.style.color = "red";
                    password_field_2.style.fontSize = "x-small";
                }
                if(result.message == "You are not logged in.")
                {
                    localStorage.removeItem("token");
                    init();
                }
            }
        }
        formData.reset();
    }
};

var newPostForm =
{

    post: function(formData)
    {
        var token = localStorage.getItem("token");
        var result = serverstub.postMessage(token, formData.new_post.value, myemail);

        if (result.success == true)
        {
            formData.reset();
            wallForm.getMessages();
        }
        else
        {
            if(result.message == "You are not signed in.")
            {
                localStorage.removeItem("token");
                init();
            }
        }
    },


    reset: function(formData)
    {
        formData.new_post = "";
    }
};



var userdataForm =
{

    getMyDetails: function(formData)
    {
        var token = localStorage.getItem("token");
        var result = serverstub.getUserDataByToken(token);

        if (result.success == true)
        {
            myemail = result.data.email;

            document.getElementById("my_details_body").innerHTML = "Welcome <b>" + result.data.firstname + " " + result.data.familyname + "</b>! (" + myemail +")<br>"
            + "<p class=smallFont>Gender: " + result.data.gender + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Country: " + result.data.country
            + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;City: " + result.data.city + "</p>";
        }

        else
        {
            if(result.message == "You are not signed in.")
            {
                localStorage.removeItem("token");
                init();
            }
        }
    }
};



var wallForm =
{

    getMessages: function()
    {
        var token = localStorage.getItem("token");
        var result = serverstub.getUserMessagesByToken(token);

        if (result.success == true) {
            document.getElementById("wall_body").innerHTML = "";
            for(var i=0; i<result.data.length; i++)
            {
                var userData = serverstub.getUserDataByEmail(token,result.data[i].writer);

                document.getElementById("wall_body").innerHTML = document.getElementById("wall_body").innerHTML + "<b>" + userData.data.firstname
                + " " + userData.data.familyname + " (" + result.data[i].writer + ")" + ": </b><textarea disabled class=post_textarea>" + result.data[i].content + "</textarea><br>";

            }
        }

        else
        {
            if(result.message == "You are not signed in.")
            {
                localStorage.removeItem("token");
                init();
            }
        }
    }
};



var search_user_form =
{

    getUser: function(formData)
    {
        var token = localStorage.getItem("token");
        var result = serverstub.getUserDataByEmail(token,formData.email.value);

        if (result.success == true)
        {
            otheremail = result.data.email;

            document.getElementById("other_details_body").innerHTML = "<b>" + result.data.firstname + " " + result.data.familyname + "</b>! (" + otheremail + ")<br>"
            + "<p class=smallFont>Gender: " + result.data.gender + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Country: " + result.data.country+ "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;City: "
            + result.data.city + "</p>";

            document.getElementById("other_body").style.display = "block";
            otherWallForm.getMessages();
        }

        else
        {
            if(result.message == "You are not signed in.")
            {
                localStorage.removeItem("token");
                init();
            }

            document.getElementById("other_details_body").innerHTML = "<b> User not found";
            document.getElementById("other_body").style.display = "none";

        }
    }
};


var otherWallForm =
{

    getMessages: function()
    {
        var token = localStorage.getItem("token");
        var result = serverstub.getUserMessagesByEmail(token,otheremail);

        if (result.success == true) {
            document.getElementById("other_wall_body").innerHTML = "";
            for(var i=0; i<result.data.length; i++)
            {
                var userData = serverstub.getUserDataByEmail(token,result.data[i].writer);

                document.getElementById("other_wall_body").innerHTML = document.getElementById("other_wall_body").innerHTML + "<b>" + userData.data.firstname
                + " " + userData.data.familyname + " (" + result.data[i].writer + ")" + ": </b><textarea disabled class=post_textarea>" + result.data[i].content + "</textarea><br>";
            }
        }

        else
        {
            if(result.message == "You are not signed in.")
            {
                localStorage.removeItem("token");
                init();
            }
        }
    }
};


var otherNewPostForm =
{

    post: function(formData)
    {
        var token = localStorage.getItem("token");
        var result = serverstub.postMessage(token, formData.new_post.value, otheremail);

        if (result.success == true)
        {
            formData.reset();
            otherWallForm.getMessages();

        }
        else
        {
            if(result.message == "You are not signed in.")
            {
                localStorage.removeItem("token");
                init();
            }
        }
    },


    reset: function(formData)
    {
        formData.new_post = "";
    }
};