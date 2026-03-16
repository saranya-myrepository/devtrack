async function addComment(event){

    event.preventDefault()

    const ticketId = document.getElementById("ticket_id").value
    const comment = document.getElementById("comment").value

    const response = await fetch("/add_comment",{

        method:"POST",

        headers: authHeaders(),

        body: JSON.stringify({
            ticket_id: ticketId,
            comment: comment
        })

    })

    handleUnauthorized(response)

    const data = await response.text()

    alert(data)

    location.reload()
}