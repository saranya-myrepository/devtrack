document.addEventListener("DOMContentLoaded", function(){

    const chartData = document.getElementById("chartData")

    if(!chartData){
        return
    }

    const totalTickets = parseInt(chartData.dataset.total) || 0
    const solvedTickets = parseInt(chartData.dataset.solved) || 0
    const assignedTickets = parseInt(chartData.dataset.assigned) || 0

    const openCount = parseInt(chartData.dataset.open) || 0
    const progressCount = parseInt(chartData.dataset.progress) || 0
    const solvedCount = parseInt(chartData.dataset.solvedstatus) || 0


    const chartOptions = {

        responsive: true,

        maintainAspectRatio: false,

        layout: {
            padding: 20
        },

        plugins: {
            legend: {
                position: "right",   // legend on right side
                align: "center",     // vertically centered
                labels:{
                    boxWidth:18,
                    padding:15
                }
            }
        }
    }



    const ticketCanvas = document.getElementById("ticketAnalytics")

    if(ticketCanvas){

        new Chart(ticketCanvas,{
            type:"pie",
            data:{
                labels:["Total","Solved","Assigned"],
                datasets:[{
                    data:[totalTickets, solvedTickets, assignedTickets],
                    backgroundColor:[
                        "#3498db",
                        "#e74c3c",
                        "#f39c12"
                    ]
                }]
            },
            options:chartOptions
        })

    }



    const statusCanvas = document.getElementById("ticketStatus")

    if(statusCanvas){

        new Chart(statusCanvas,{
            type:"pie",
            data:{
                labels:["Open","In Progress","Solved"],
                datasets:[{
                    data:[openCount, progressCount, solvedCount],
                    backgroundColor:[
                        "#3498db",
                        "#f06292",
                        "#f39c12"
                    ]
                }]
            },
            options:chartOptions
        })

    }

})