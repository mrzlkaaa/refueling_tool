<template>
    <div id="viewData" class="card-body"> <!--* loop here -->
        <div v-for="(refuel,i) in refuels" :key="i">
            <div @click="toggleBlock(refuel)" class="row FC">
                <div class="col">
                    <div> Fuel Cycle №{{refuel.Name}}</div>
                </div>
                <div class="col">
                    <div class="row">
                        <div class="col right">
                            {{(refuel.TotalEnOuts).toFixed(1)}} Mev<span>&#215;</span>hours
                        </div>
                    </div>
                    <div class="row">
                        <div class="col right">
                            {{(refuel.TotalTime/24).toFixed(2)}} Days            
                        </div>
                    </div>
                    <i class="fa-solid fa-ellipsis-vertical fa-lg"></i>
                </div>
            </div>
            <ViewWData
            :WD="refuel.WeeklyData"
            :display="refuel.display"
            />
        </div>    
    </div>
</template>
<script>
import ViewWData from "./ViewWData.vue"
import { toggleBlock } from "./toggleBlock"
export default {
    name: "ViewFCData",
    components: {
        ViewWData
    },
    data(){
        return {
            refuels:"",
        }
    },
    methods: {
        toggleBlock: toggleBlock
    },
    created(){
        fetch(`${this.diaryDepHost}/overallData`)
            .then(response => response.json())
            .then(data => this.refuels = data)
        
    },
    watch:{
        refuels(){
            for (let i=0; i<this.refuels.length; i++) {
                this.refuels[i].display="none"
                console.log(this.refuels[i])
            }
        }
    }
}

</script>
<style>
    #viewData .col {
        margin: auto;
    }
    #viewData .row {
        margin: auto;
        padding-right: 7px;
        padding-bottom:10px;
        
    }
    .right {
        text-align: center;
        padding:0px;
    }
    .FC:hover {
        background: #eee;
    }
    .fa-ellipsis-vertical {
        position:absolute;
        /* margin:auto; */
        top:25px;
        right:0px;
    }
</style>