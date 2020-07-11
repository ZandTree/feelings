
new Vue({
    el:"#app",
    data:{
        thoughts:[],
        displayMore:""
    },
    methods:{
        showMore:function(th){
            // event.preventDefault(); 
            console.log('but was clicked');
            // toDo backend should add extra attr = displayMore for each obj
            // otherwise it will be broad-casted for all elem (this.)

            th.displayMore =! th.displayMore;
        },

    },
    
    created:function(){
        fetch('/api/v1/my-thoughts/')
        .then(resp =>resp.json())
        .then(data=>{
                this.thoughts=data;
                // console.log("data",data);
        })
    }
    
})

