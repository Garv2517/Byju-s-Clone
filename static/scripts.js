
function handleGoogleLogin() {
    gapi.load('auth2', function() {

        gapi.auth2.init({
            client_id: window.googleClientId
        }).then(() => {
            const auth2 = gapi.auth2.getAuthInstance();
            auth2.signIn().then(googleUser => {
                const profile = googleUser.getBasicProfile();
                
                const id_token = googleUser.getAuthResponse().id_token;
                fetch('/google-login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: id_token })
                }).then(response => {
                    if (response.ok) {
                        window.location.href = '/';
                    }
                });
            });
        });
    });
}

function handleFacebookLogin() {
    window.fbAsyncInit = function() {

        FB.init({
            appId: window.facebookAppId,
            cookie: true,
            xfbml: true,
            version: 'v12.0'
        });

        FB.login(function(response) {
            if (response.authResponse) {
                const accessToken = response.authResponse.accessToken;
                
                fetch('/facebook-login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: accessToken })
                }).then(response => {
                    if (response.ok) {
                        window.location.href = '/';
                    }
                });
            }
        }, {scope: 'email'});
    };

    
    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "https://connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
}


document.addEventListener('DOMContentLoaded', function() {
    window.googleClientId = document.getElementById('google-client-id').value;
    window.facebookAppId = document.getElementById('facebook-app-id').value;

    const navLinks = document.querySelectorAll('nav a');


    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            
            document.querySelector('.page-content').classList.add('fade-out');
            setTimeout(() => {

                window.location.href = target;
            }, 300);
        });
    });
    
    document.querySelector('.page-content').classList.add('fade-in');

});
