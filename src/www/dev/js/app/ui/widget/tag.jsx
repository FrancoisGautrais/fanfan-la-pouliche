var tags = module.load("js.app.model.tag")
var select = module.load("js.react.component.ui.widget.select")
var utils =  module.load("js.react.component.common.utils")

class MultipleTagSelect extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        var childopts = utils.assign({}, this.props);
        delete childopts.className;
        return (
            <div className={"tag-select-multiple "+this.props.className}>
                <select.MultipleSelect
                    options={tags.list()} getkey={(k,v)=>[k, v.path]} {...childopts}/>
                <span className="material-icons">add</span>
            </div>
        )
    }
}


function MultipleTagSelectInline(prop){
    var attr = {
        label: prop.label?prop.label:"Tags"
    }
    var  props = Object.assign({}, prop)

    if(!props.id) props.id=utils.new_id();

    return (
        <div className="input-group mb-2">
            <label className="input-group-text " htmlFor={props.id+".input"}>{attr.label}</label>
            <MultipleTagSelect className="" {...prop}/>
        </div>
    )

}

module.exports={
    MultipleTagSelect: MultipleTagSelect,
    MultipleTagSelectInline: MultipleTagSelectInline
}