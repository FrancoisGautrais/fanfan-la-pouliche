module.load(".third-party.*")
module.load(".react.*")
module.load(".common.test")

var print = console.log;


function on_post(){
    var data = {}
    $("[name^=data-]").each( function(i,e){
        e=$(e)
        data[e.attr("name").substr(5)] = e.val()
    })

    print(data)
}
