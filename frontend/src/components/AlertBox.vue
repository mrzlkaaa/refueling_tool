<template>
    <div :style="{'display':info.display}">
        <div :class=info.type role="alert">
            {{info.msg}}
        </div>
        <img v-if="info.img" :src=img() style="width:50%; height:50;">
    </div>
</template>
<script>
import {mapActions} from 'vuex'
export default {
    name: "AlertBox", 
    props:["info"],
    computed:{
    },
    updated(){
        this.hideAlert()
    },
    methods:{
        ...mapActions([
            "hideAlert"
        ]),
        // hide(){
        //     return this.$emit("hide", {status:false, msg:""})
        // },
        img(){
            let path = "/src/assets/"
            console.log(path)
            return `${path}${this.info.code}.png`
        }
    }
}
</script>