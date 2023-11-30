let shipConditionSelect = document.getElementById("ship-condition");
let costResult = document.getElementById("result");
let newCustcheck = document.getElementById("new-customer");

let costs = {
  "No repairs needed": 0,
  "Light repairs needed": 100,
  "Heavy repairs needed": 500,
  "New ship": 1000,
};


// they get 10% of if they check the new customer checkbox
function updateCost() {
  let selectedOption = shipConditionSelect.value;
  let cost = costs[selectedOption];
  cost = parseFloat(cost);
  
  if(newCustcheck.checked){
    cost = cost * 0.9;
  }
  costResult.textContent = `${cost} Golden doubloons`;
}
shipConditionSelect.addEventListener("change", updateCost);
newCustcheck.addEventListener("click", updateCost);

updateCost();
