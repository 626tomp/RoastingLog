# RoastingLog

This will be a program to help keep track of roasting progress and calculate volume required when roasting coffee.

\* Needs a rework for what task is in each milestone - for a more up to date description go to https://github.com/626tomp/RoastingLog/projects/1

## STAGES:
### MVP:
- [ ] Display all cafes and the amount of coffee they need
- [ ] Be able to edit the coffee needed for each cafe
- [ ] Calculate the amount of coffee needed to fullfill each cafe's requirements
- [x] Have a database to store the amount of coffee each cafe has / needs weekly
- [ ] Be able to add a new cafe or delete an existing one
  - [x] In the database
- [ ] Be able to add a new blend
  - [x] In the database 

### STRETCH 1
- [x] Be able to calculate the number of roasts required, including smaller 9kg or 4kg roasts
  - [ ] Be able to alter the options for roast size
- [x] Keep track of how many roasts i have done today of each type
- [ ]  Allow cafes to have multiple blends / single origins
- [x]  Handle single origin roasts rather than just blends (might require a database rethink)
- [x]  Basic prediction on time to finish roasting (eg. roasts * 20 mins + current time)


### STRETCH 2
- [ ] Have existing inventory for each cafe before i roast and for this top be subtracted from the amount i have to do
- [ ] Update blend ratios
- [x] Advanced prediction for when i will finish (More accurate - hopefully - with maybe some simple ML (sklearn something))
- [ ] A user who has never been shown how to use the program should be able to use it easily - final usability tweaks
- [x] Have a button to reset all the values that will change from day to day.
- [ ] A way to either select, finish Roasting or finish Week
  - [ ] finish roasting should: Move all the roasts that were completed to the quantitiy of each blend in stock
  - [ ] finish week should: do the same as finish roasting, but then subtract the amount of coffee needed for each cafe from this volume to show the leftover coffee volume


## Plan for OOP approach
Will test - not sure how viable it will be, or if its worth the hassle to change

Program:
* Cafes: List[Cafe]
* Roasts: List[Roast]
* Green: List[Green]
* CalculsteRoasts()
* GetRoastFromID(id)
* AddRoast(ID)

Roasts:


Green:


Cafe:


PostRoast inhgerits from Roast:
Components: List[Dict]
PostRoast = True
