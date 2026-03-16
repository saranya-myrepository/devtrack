// -----------------------------
// Create Ticket
// -----------------------------
async function createTicket(event){

    event.preventDefault()

    const title = document.getElementById("title").value
    const description = document.getElementById("description").value
    const priority = document.getElementById("priority").value

    try{

        const response = await fetch("/create_ticket", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title,
                description: description,
                priority: priority
            })

        })

        if(!response.ok){
            const errorText = await response.text()
            alert(errorText)
            return
        }

        const message = await response.text()

        alert(message)

        window.location.href = "/view_my_issues"

    }
    catch(error){
        console.error("Error creating ticket:", error)
        alert("Something went wrong while creating the ticket.")
    }

}


// -----------------------------
// Load My Tickets (optional)
// -----------------------------
async function loadMyTickets(){

    try{

        const response = await fetch("/view_my_issues", {
            method: "GET"
        })

        if(!response.ok){
            console.error("Failed to load tickets")
        }

    }
    catch(error){
        console.error("Error loading tickets:", error)
    }

}  