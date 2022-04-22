<template>
    <div class="alertbox" :style="{'display':getAlert().display, 'position':'absolute'}">
        <div :class=getAlert().type role="alert">
            {{getAlert().msg}}
        </div>
    </div>
</template>
<script>
import {mapGetters, mapActions} from 'vuex'

export default {
    name: "AlertBox", 
    props:["info"],
    created(){
        this.resetAlert()
    },
    updated(){
        this.hideAlert()
    },
    methods:{
        ...mapGetters([
            "getAlert",
        ]),
        ...mapActions([
            "resetAlert",
            "hideAlert"
        ]),
    }
}
</script>
<style>
    .alertbox {
        top:60px;
        left:0px;
        right:0px;
        margin:auto;
    }
</style>