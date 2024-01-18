"use strict";

document.addEventListener(
    'DOMContentLoaded',
    () =>
    {
        for (const machine in gAllStatuses)
        {
            refreshStatuses_sequential(
                machine,
                gAllStatuses[machine]);
        }
    },
    false);

function alerting(message)
{
    alert(message);
}


function setStatus(element, response)
{
        if (response.status === 204)
        {
            element.className = "status_ok";
        }
        else if (response.status === 200)
        {
            element.className = "status_ko";
        }
        else
        {
            element.className = "status_error";
            response.text().then(
                (text) => {alert(`Unexepect status response code ${response.status}:\n${text}`);});
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
    return fetch(`/status/${machine}/status_${stat}`)
            .catch((typeError) => alert("Fetch failed with: ", typeError))
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
                        (text) => alert(`Response status ${response.status}:\n${text}`));
                }
            },
            (typeError) => alert("Fetch failed with: ", typeError))
        .finally(() => button.disabled = false);
}
