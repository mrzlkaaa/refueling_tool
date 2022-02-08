<template>
    <div :class="[code < 400 ? 'alert alert-success' : 'alert alert-danger']" role="alert">
        {{ code!=400 ? text : 'ERROR: ' + text}}
    </div>
</template>
<script>
export default {
    name: "AlertBox", 
    props:["code", "text", "time"],
    watch:{
        text(){
            console.log("changed")
            setTimeout(this.hide, 3000)
        }
    },
    methods:{
        hide(){
            return this.$emit("hide", {status:false, msg:""})
        }
    }
}
</script>