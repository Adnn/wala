"use strict";


function alerting(message)
{
    alert(message);
}


function setStatus(element, statusResult)
{
        if (statusResult.ok)
        {
            element.className = "status_ok";
        }
        else
        {
            element.className = "status_ko";
        }
}


async function refreshStatuses_sequential(machineName, statuses)
{
    statuses.forEach((st) => {
        {
            const element = document.getElementById(`status_${machineName}_${st}`);
            element.className = "status_unknown";
        }});


    queryNext(machineName, statuses, 0);
}


function queryNext(machineName, statuses, idx)
{
    query(machineName, statuses[idx])
        .then(
            (response) =>
            {
                setStatus(document.getElementById(`status_${machineName}_${statuses[idx]}`),
                          response);

                if(idx+1 < statuses.length)
                {
                    queryNext(machineName, statuses, idx+1);
                }
            });
}


async function refreshStatuses_allAtOnce(machineName, statuses)
{
    statuses.forEach(async (stat) => {
        const element = document.getElementById(`status_${machineName}_${stat}`);
        element.className = "status_unknown";
        const statusResult = await query(machineName, stat);
        setStatus(element, statusResult);
    });
}


async function query(machine, stat)
{
    return fetch(`/execute/${machine}/status_${stat}`)
}


function act(endpoint, button)
{
    button.disabled = true;
    fetch(endpoint)
        .then(
            (response) =>
            {
                if(!response.ok)
                {
                    response.text().then(
                        (text) => alert(`Response status ${response.status} : ${text}.`));
                }
            },
            (typeError) => alert("Fetch failed with: ", typeError))
        .finally(() => button.disabled = false);
}
