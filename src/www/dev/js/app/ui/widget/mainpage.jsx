class MainPage extends React.Component {
    /*
        props:
            pages : dict[Label, React.Component]
            selected : Label
    */
    constructor(props){
        super(props);
        this.state = {
            selected: 0
        }
    }

    render(){
        return (
            <h1> OK </h1>
        )
    }
}


module.exports = {
    MainPage :  MainPage
}