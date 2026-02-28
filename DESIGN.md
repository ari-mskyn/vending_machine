# Vending Machine Design Document

The vending machine has three modes:

* Admin mode
* User mode
* Default mode

## Admin Mode

The admin can refill the vending machine with products as well as with cash for change. It can be done through the interface. They are also able to withdraw cash out of the vending machine. The main state will be refreshed.

## User Mode

Users are able to insert the coins in the machine, select only one product and press the button for buying. There is also a button for canceling, which allows the user to get the inserted money back and  cancel the transaction, which means the product will be unselected. 

## Default Mode

There is a screen which shows "Insert money". This is a default state before and after a transaction. Also the default state will be returned in case of cancellation.

## The Functionality Of The Vending Machine(User Mode)

### Inserting Coins

---
The user is able to insert the coins through the slot. This action brings the system of the machine to running. The sum of the coins will be added to the cashbox of the machine.

The slot is a pop-up window, which can be triggered by clicking on the slot sign. It shows the accepted coins that can be inserted. Clicking on the coin means inserting it to the machine. 

### Selecting Product

---
There is a database of the products. There are 6 kinds of products by default. Each product comes in 5 pieces. There is  a button which represents the image of the product as well as the price for each. The button can be pressed for the selection of the product. The user can only buy one product per transaction.

There is a screen, which shows the selected amount of the products, the price, the inserted money. 

### Buying Products

---
There is a button for buying the selected products. 
Buying is only possible to proceed when the inserted money is the same as the price of the products or it exceeds the price.In the last case the change will be returned to the user. The products that the user buys will be deleted from the database.

### Cancelling

---

The user can cancel the transaction via the button "Cancel". The inserted money will be returned and the machine goes back to the default mode.

## The Functionality Of The Vending Machine(Admin Mode)

To enter the mode admin should be able to verify themselves. After the succeeded verification there are three main functions in this mode:

* refill products from the database
* refill money to the cashbox
* withdraw money from the cashbox

### Refill Products

---
The admin will be able to refill the products via special button. It allows to select each product and increment the amount until 5 pieces. The products will be taken from the database.

### Refill Coins

---
Via the coin slot the admin will be able to choose the coins and their amount and add them to the cashbox. 

### Withdraw money

---
The admin has the authority to withdraw money from the cashbox(can be changed to a coin database). They only can withdraw the money that is available or less. 
This case will be first proved then executed. 

### The Functionality Of The Default Mode

---

Default mode can only exist when the acquired amount of money and products already exist thus the vending machine can be used. There will be two conditions:

* prove the amount of money and products
* in case of deficiency inform the admin internally 