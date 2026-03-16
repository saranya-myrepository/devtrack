// Logout function
function logoutUser(){

    localStorage.removeItem("token")

    window.location.href = "/login"
}


// Optional API login if you later switch to fetch login
async function loginUser(email, password){

    const response = await fetch("/login",{

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({
            email: email,
            password: password
        })

    })

    const data = await response.json()

    if(data.token){

        localStorage.setItem("token", data.token)

        window.location.href = "/dashboard"
    }
    else{
        alert("Login failed")
    }

}