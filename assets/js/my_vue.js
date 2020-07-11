
new Vue({
    el:"#app",
    data:{
        thoughts:[],      
        
    },       
    methods:{        

    },    
    async created(){
        let resp = await fetch('/api/v1/my-thoughts/')
        this.thoughts = await resp.json();        
    }    
})

