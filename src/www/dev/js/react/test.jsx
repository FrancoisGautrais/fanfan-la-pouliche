'module';
module.load('.component.ui.widget.*')
const SimpleImageForm = module.load("js.app.ui.form.file")
let domContainer = document.querySelector('#like_button_container');
ReactDOM.render(<SimpleImageForm label="Nom" placeholder="Votre nom"/>, domContainer);


module.exports={}
