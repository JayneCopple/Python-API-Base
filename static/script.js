`use strict`

// import the dom
import * as DOM from './dom.js';

// list item function
const writeItem = item => {
  const child = document.createElement(`li`);
  child.id = item._id;
  child.innerHTML = `${JSON.stringify(item)}`;
  DOM.listOutput.appendChild(child);
}

// GET all function
const get = () => {
  DOM.listOutput.innerHTML = ``;

  axios.get(`/read`)
    .then((response) => {
      if (!Array.isArray(response.data)) {
        writeItem(response.data);
      } else {
        for (let item of response.data) {
          writeItem(item);
        }
      }
    }).catch((err) => {
      console.log(err);
    });
}

// POST function
const post = () => {
  axios.post(`/create`, {   name : DOM.inputName.value,
                            description : DOM.inputDescription.value, 
                            price : DOM.inputPrice.value})
    .then((response) => {
      console.log(response);
      get();
    }).catch((err) => {
      console.log(err);
    });
}

// GET one function
const getOne = () => {
  axios.get(`/read/${DOM.inputID.value}`)
    .then((response) => {
      DOM.singleOutput.innerHTML = JSON.stringify(response.data);
    }).catch((err) => {
      console.log(err);
    });
}

// PUT function
const put = () => { 
  axios.put(`/update/${DOM.inputUpdateID.value}`, { name : DOM.inputUpdateName.value,
                                                    description : DOM.inputUpdateDescription.value,
                                                    price : DOM.inputUpdatePrice.value})
    .then((response) => {
     console.log(response);
     get();
    }).catch((err) => {
      console.log(err);
    });
}

// DELETE function
const del = () => { 
  axios.delete(`/delete/${DOM.inputDeleteID.value}`)
    .then((response) => {
     console.log(response);
     get();
    }).catch((err) => {
      console.log(err);
    });
}

// set up the buttons' on click events
DOM.buttonCreate.onclick = () => post();
DOM.buttonReadOne.onclick = () => getOne();
DOM.buttonUpdate.onclick = () => put();
DOM.buttonDelete.onclick = () => del();
//DOM.buttonReadAll.onclick = () => get();

// run the get function on page load
get();