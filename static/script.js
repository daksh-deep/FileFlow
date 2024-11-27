var userName = getCookie("user_name");

    if (!userName) {
        userName = prompt("Please enter your name:");
        if (userName != "" && userName != null) {
            document.cookie = "user_name=" + userName + ";path=/";
        }
    }

    document.getElementById("user-name").textContent = userName;

    function getCookie(cookieName) {
        var name = cookieName + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var cookieArray = decodedCookie.split(';');
        for(var i = 0; i < cookieArray.length; i++) {
            var cookie = cookieArray[i].trim(); // Trim the cookie string to remove leading/trailing spaces
            if (cookie.indexOf(name) == 0) {
                return cookie.substring(name.length); // Return only the value of the cookie
            }
        }
        return "";
    }
    