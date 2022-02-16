function width(){
   return window.innerWidth
       || document.documentElement.clientWidth
       || document.body.clientWidth
       || 0;
}

function height(){
   return window.innerHeight
       || document.documentElement.clientHeight
       || document.body.clientHeight
       || 0;
}


function resize_image(evt, img=null){
    img=img || $(this)
    var window = {
        w: width() - 100,
        h: height() - 100
    }
    var image = {
        w: img.width(),
        h: img.height()
    }
    var ratio = {
        x : window.w / image.w,
        y : window.h / image.h
    }
    if(image.h*ratio.x<=window.h){
        img.width(image.w*ratio.x);
        img.height(image.h*ratio.x);
    }else{
        img.width(image.w*ratio.y);
        img.height(image.h*ratio.y);
    }
}

function on_resize_window(){
    var elem = $(".viewer-img-content");
    if(elem.length)
        resize_image(null, elem);
}

function do_nothing(e){
    e.preventDefault();
    e.stopPropagation();
}


class Viewer {

    constructor(){
        this.current_id=null;
    }

    get_images_shown(){
        var ids_show = [];
        function add_if_shown(i , e){
          e=$(e);
          if(e.is(":visible")){
            ids_show.push(e.data("image-id"))
          }
        }
        $(".tile-image").each(add_if_shown)
        return ids_show
    }

    get_next_prev_image(id){
        var ret = {
            prev: null,
            next: null
        }
        var ids_show = this.get_images_shown();
        for(var i=0; i<ids_show.length; i++){
            if(ids_show[i]==id){
                ret.prev=(i>0)?ids_show[i-1]:null;
                ret.next=(i+1<ids_show.length)?ids_show[i+1]:null;
            }
        }
        return ret;
    }

    show(id){
        if(Number.isInteger(id)){
            var liste = this.get_images_shown();
            id=liste[id];
        }
        this.current_id=id;
        var root = $(".viewer");
        var img_root = $(".viewer-img");
        var img_data = IMAGES[viewer.current_id]
        img_root.empty()
        var img = $('<img class="viewer-img-content" src="/image/'+id+'/l" />')
        img.attr("aria-label", img_data.description)
        img.on("load", resize_image);
        img.on("click", do_nothing);
        img_root.append(img)
        root.removeClass("hidden")
        if(this.next())
            $(".viewer-next").show()
        else
            $(".viewer-next").hide()

        if(this.prev())
            $(".viewer-prev").show()
        else
            $(".viewer-prev").hide()
        $(".viewer-footer").on("click", do_nothing);
        $(".viewer-title").html(img_data.name)
        root.show()
    }

    next(){
        var next = this.get_next_prev_image(this.current_id);
        return next.next
    }

    prev(){
        var prev = this.get_next_prev_image(this.current_id);
        return prev.prev
    }

    show_prev(){
        this.show(this.prev())
    }

    show_next(){
        this.show(this.next())
    }

    hide(){
        $(".viewer").hide()
    }

    init(){

        window.onresize=on_resize_window;
    }

}

var viewer = new Viewer()