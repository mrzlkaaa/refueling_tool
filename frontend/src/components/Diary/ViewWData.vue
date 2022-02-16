<template>
    <div class="WD-section" :style="{display:display}">
        <div v-for="wd in WD" :key=wd >
            <div @click="toggleBlock(wd)" class="row WD">
                <div class="col">
                    <div> {{dateFormatter(wd.DetailWeek.at(0).FromDate)}} - {{dateFormatter(wd.DetailWeek.at(-1).ToDate)}}</div>
                </div>
                <div class="col">
                    <div class="row">
                        <div class="col right">
                            {{(wd.TotalEnOuts).toFixed(1)}} Mev<span>&#215;</span>hours
                        </div>
                    </div>
                    <div class="row">
                        <div class="col right">
                            {{(wd.TotalTime/24).toFixed(2)}} Days            
                        </div>
                    </div>
                    <i class="fa-solid fa-ellipsis-vertical fa-lg"></i>
                </div>
            </div>
            <ViewDWData
            :DW="wd.DetailWeek"
            :display="wd.display"
            />
        </div>
    </div>
</template>
<script>
import ViewDWData from "./ViewDWData.vue"
import { toggleBlock } from "./toggleBlock"
export default {
    name: "ViewWData",
    components: {
        ViewDWData
    },
    props:["WD", "display"],
    data(){
        return {
            data:""
        }
    },
    methods:{
        dateFormatter(v){
            let date = new Date(v)
            return date.toDateString()
        },
        toggleBlock: toggleBlock
    },
    created(){
        for(let i=0; i<this.WD.length; i++) {
            this.WD[i].display = "none"
            console.log(i)
        }
    }
}
</script>
<style>
    .WD-section {
        margin:auto;
        width:80%;
        border-top: 2px solid #eee;
        border-bottom: 2px solid #eee;
        /* background-color:rgb(250, 246, 246) */

    }
    .WD:hover {
        background: #eee;
        
    }
</style>