class Dropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  onchange(event){
    var elem = event.target;
    var value = elem.value;
    if(this.attr.type=="file") value=elem.files[0]
    this.setState({value: value})
    if(this.onchangelistener){
        this.onchangelistener(this, value)
    }
  }


  render() {
        var file_accept=this.props.accept?this.props.accept:""
        var multiple=this.props.multiple?this.props.multiple:false;
       return (

       )
  }
}

module.exports = Dropdown;