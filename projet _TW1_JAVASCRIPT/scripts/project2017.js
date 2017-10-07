// YOUR NAME HERE

// === constants ===
const MAX_QTY = 9;
const productIdKey = "product";
const orderIdKey = "order";
const inputIdKey = "qte";

// === global variables  ===
// the total cost of selected products
var total = 0;



// function called when page is loaded, it performs initializations
var init = function () {
	createShop();

	var input = document.getElementById('filter');
	input.addEventListener('keyup', filter)

	// TODO : add other initializations to achieve if you think it is required
}
window.addEventListener("load", init);



// usefull functions

/*
* create and add all the div.produit elements to the div#boutique element
* according to the product objects that exist in 'catalog' variable
*/
var createShop = function () {
	var shop = document.getElementById("boutique");
	for(var i = 0; i < catalog.length; i++) {
		shop.appendChild(createProduct(catalog[i], i));
	}
}

/*
* create the div.produit elment corresponding to the given product
* The created element receives the id "index-product" where index is replaced by param's value
* @param product (product object) = the product for which the element is created
* @param index (int) = the index of the product in catalog, used to set the id of the created element
*/
var createProduct = function (product, index) {
	// build the div element for product
	var block = document.createElement("div");
	block.className = "produit";
	// set the id for this product
	block.id = index + "-" + productIdKey;
	// build the h4 part of 'block'
	block.appendChild(createBlock("h4", product.name));

	// adds figure with image of the product inside
	block.appendChild(createFigureBlock(product));

	// build and add the div.description part of 'block'
	block.appendChild(createBlock("div", product.description, "description"));
	// build and add the div.price part of 'block'
	block.appendChild(createBlock("div", product.price, "prix"));
	// build and add control div block to product element
	block.appendChild(createOrderControlBlock(index));
	return block;
}

/* return a new element of tag 'tag' with content 'content' and class 'cssClass'
 * @param tag (string) = the type of the created element (example : "p")
 * @param content (string) = the html wontent of the created element (example : "bla bla")
 * @param cssClass (string) (optional) = the value of the 'class' attribute for the created element
 */
var createBlock = function (tag, content, cssClass) {
	var element = document.createElement(tag);
	if (cssClass != undefined) {
		element.className =  cssClass;
	}
	element.innerHTML = content;
	return element;
}


/*
* create and return the figure block for this product
* @param product (product object) = the product for which the figure block is created
*/


var createFigureBlock = function (product) {
	var img = document.createElement('img');
	img.src = product.image;
	img.alt = product.name;

	var figure = document.createElement('figure');
	figure.appendChild(img);
	return figure;
}
/*
*creates and returns the control block of a certain index
*the index is key to giving the correct id names
*@param index (integer) used to give the correct names, so that the blocks can later be found by their id
*/

var createOrderControlBlock = function (index) {
	var control = document.createElement("div");
	control.className = "controle";

	// create input quantity element and give it the needed properties
	var input = document.createElement("input");
	input.id = index + '-' + inputIdKey;
	input.type = "number";
	input.step = "1";
	input.value = "0";
	input.min = "0";
	input.max = MAX_QTY.toString();

	//add event listeners to input that check if the value entered follows the desired guidelines
	input.addEventListener('change', quantityCheck);
	input.addEventListener('mouseup', quantityCheck);

	// add input to control block as its child
	control.appendChild(input);

	// create order button and give it the desired class/id values
	var button = document.createElement("button");
	button.className = 'commander';
	button.id = index + "-" + orderIdKey;

	//add an event listener that executes the order function when the button is pressed
	button.addEventListener('click', order);

	// apend the button to the control block as its child
	control.appendChild(button);

	// the built control div node is returned so that it can be used in the desired way
	return control;
}

/*
*used to check if a correct quantity is entered in the input element of a product
*check the quantity and makes the desired changes according to MAX_QTY
*activates the order button if needed
*/
var quantityCheck = function(){
	index = parseInt(this.id);
	var button = document.getElementById(index+'-order');
	value = this.value;

	if (value>MAX_QTY) {
		this.value=MAX_QTY;
		button.style.opacity = '1';
	}else if (value>0) {
		button.style.opacity = '1';
	}else {
		this.value = 0;
		button.style.opacity = '0.25';
	}
}

var order = function(){
	//get the index of the element
	var index = parseInt(this.id);

	//if the quantity of the input of the element isnt 0 make these changes
	if (getQuantity(index)!=0) {
		//get all the ordered products
		var achats = document.getElementsByClassName('achat');
		//make a list with their indexes
		var achats_index = [];
		for (var i = 0; i < achats.length; i++) {
			achats_index.push(parseInt(achats[i].id))
		}
		//get the element that holds the total value
		var total = document.getElementById('montant');

		//if the element hasnt been ordered before
		if (achats_index.indexOf(index)==-1) {
			//change the total value accordingly to the quantity
			//remark: here the del parameter of getQuantity is automatically false, we do not want the quantity to be deleted
			//after it has been 'gotten' as we will be using it again in the createAchat function
			total.innerHTML = parseInt(total.innerHTML) + parseInt(getQuantity(index))*parseInt(getPrice(index));
			//create a new achat block in the panier block
			createAchat(index);
			//if the element has been ordered befor
		} else {
			//get the achat block corresponding to the product
			achat = achats[achats_index.indexOf(index)];
			//get the quantity that has been ordered
			quantity = achat.querySelector('div.quantite');
			//get the quantity that is to be added and reset the control block(del=true)
			add = parseInt(getQuantity(index, true));
			//calculate the new quantity
			newQ = parseInt(quantity.innerHTML)+add;

			//if the new quantity is more than the aximum possible make the according changes
			if (newQ>MAX_QTY) {
				total.innerHTML = parseInt(total.innerHTML) + (MAX_QTY-parseInt(quantity.innerHTML))*parseInt(getPrice(index));
				quantity.innerHTML = MAX_QTY;
			//if not simply modify the existing quantity
			}else {
				quantity.innerHTML = newQ;
				total.innerHTML = parseInt(total.innerHTML) + add*parseInt(getPrice(index));
			}

		}
	}
}

/*
*returns the quantity of an element input, found using the parameter index and makes the according changes needed to the control box of that element
*@param index(integer) used to find the desired elements
#@param del(boolean) used to change the behaviour of the function
*/

var getQuantity = function(index, del = false) {

	//find the desired input element from which to 'get' the quantity
	var input = document.getElementById(index + '-qte');
	//find the desired button element which to channge in the result of the function
	var button = document.getElementById(index + '-order');
	//save the quantity
	value = input.value;

	//if the del paramter is set to true, reset the initial button opacity and default value of the input element
	if (del) {
		button.style.opacity = '0.25';
		input.value = '0';
	}
	return value;
}

/*
*returns the price of a product of index @param index
*/
var getPrice = function(index){
	product = document.getElementById(index+'-product');
	prix = product.getElementsByClassName('prix')[0];
	return prix.innerHTML;
}

/*
*creates an achat block in to the panier block of the elemet of index @param index
*/
var createAchat = function(index){
	//create the block and give it the needed properties
	var block = document.createElement('div');
	block.className = 'achat';
	block.id = index+'-achat';

	//append the contents of the block image, title, qunatity(reset the control block after getting it), price
	block.appendChild(createFigureBlock(catalog[index]));
	block.appendChild(createBlock('h4', catalog[index].description));
	block.appendChild(createBlock('div', getQuantity(index, true),'quantite'));
	block.appendChild(createBlock('div', getPrice(index), 'prix'))

	//create the button that allows to delete orders
	var controle = createBlock('div', '', 'controle');
	var button = createBlock('button', '', 'retirer');
	button.addEventListener('click', del)
	button.id = index+'-remove';
	button.addEventListener('click', del);
	controle.appendChild(button);

	block.appendChild(controle);
	//add this control block to the achat block4
	var achats = document.getElementsByClassName('achats')[0];
	achats.appendChild(block);
}

/*
*deletes an order and remuves its price contribution from the total\
*/
var del = function() {
	var total = document.getElementById('montant');
	//get the index of the element to delete and the element
	var index = parseInt(this.id);
	var el = document.getElementById(index+'-achat');
	//get its ordered quantity and its price
	var quantity = parseInt(el.querySelector('.quantite').innerHTML);
	var price = getPrice(index);

	//change total and delete element
	total.innerHTML = parseInt(total.innerHTML)-quantity*price;
	el.parentNode.removeChild(el);
}

/*
*filter function, used to diplay only products that
*contain the text written in the input box
*/
var filter = function(){
	var shop = document.getElementById("boutique");
	var input = document.getElementById('filter');
	text = input.value.toLowerCase();

	for (var i = 0; i < catalog.length; i++) {
		name = catalog[i].name.toLowerCase();

		if (name.indexOf(text)!= -1) {
			if (!document.getElementById(i+'-product')) {
				//doesnt exist, create
				shop.appendChild(createProduct(catalog[i], i))
			}
		}
		else {
			if (document.getElementById(i+'-product')) {
				//exists => delete
				el = document.getElementById(i+'-product');
				shop.removeChild(el);
			} //else doesnt exists => do nothing
		}
	}

}
