const grid=document.getElementById("coffeeGrid"),toast=document.getElementById("toast");
function notify(message){toast.textContent=message;toast.classList.add("show");setTimeout(()=>toast.classList.remove("show"),2300)}
function renderCoffees(items){
 grid.innerHTML=items.map(coffee=>`<article class="coffee-card"><div class="coffee-emoji">${coffee.emoji}</div><div class="coffee-info"><h3>${escapeHTML(coffee.name)}</h3><p>${escapeHTML(coffee.description)}</p><div class="vote-line">Votes: <strong>${coffee.votes}</strong></div></div><button class="vote-button" data-id="${coffee.id}" aria-label="Vote for ${escapeHTML(coffee.name)}">＋</button></article>`).join("");
 document.getElementById("totalVotes").textContent=items.reduce((sum,item)=>sum+item.votes,0).toLocaleString();
 document.getElementById("coffeeCount").textContent=items.length;
 grid.querySelectorAll(".vote-button").forEach(button=>button.addEventListener("click",()=>castVote(button)));
}
function escapeHTML(value){return String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
async function loadCoffees(){
 try{const response=await fetch("/api/coffees");if(!response.ok)throw new Error();renderCoffees(await response.json())}
 catch{grid.innerHTML='<p class="loading">Could not load the coffee menu. Please refresh the page.</p>'}
}
async function castVote(button){
 const id=button.dataset.id;button.disabled=true;button.textContent="…";
 try{
  const response=await fetch(`/api/coffees/${id}/vote`,{method:"POST"});
  const result=await response.json();if(!response.ok)throw new Error(result.error||"Vote could not be saved.");
  await loadCoffees();notify(`Vote recorded for ${result.coffee.name}!`);
 }catch(error){notify(error.message);button.disabled=false;button.textContent="＋"}
}
loadCoffees();