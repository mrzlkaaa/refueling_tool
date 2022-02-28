<template>
    <div id="viewData" class="card-body">
        <div class="row">
            <div class="col"><b>Name</b></div>
            <div class="col"><b>Parameters</b></div>
            <div class="col-2"><b>Burnup file</b></div>
        </div>
        <div v-for="(refuel,i) in refuels" :key="i">
            <div class="row FC">
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
                    
                </div>
                <div class="col-2">
                    <span title="Get burnup file">
                        <i @click="onDownloadBurn(refuel)" id="burn" class="fas fa-file-export"> </i>
                    </span>
                </div>
                <div class="row">
                    <i  class="fa-solid fa-ellipsis fa-lg"></i>
                    <Button
                    class="btn btn-light"
                    @click="toggleBlock(refuel)"
                    />
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
import Button from "./Button.vue"
import { toggleBlock, saveFile } from "../helpers"
export default {
    name: "ViewFCData",
    components: {
        ViewWData,
        Button,
    },
    data(){
        return {
            refuels:"",
        }
    },
    methods: {
        toggleBlock: toggleBlock,
        onDownloadBurn(refuel){
            //*fetch post
            let days = []
            for (let i=0; i<refuel.WeeklyData.length; i++) {
                days.push((refuel.WeeklyData[i].TotalEnOuts/144).toFixed(2))
                try{
                    let restFrom = new Date(refuel.WeeklyData[i].DetailWeek.at(-1).ToDate)
                    let restTo = new Date(refuel.WeeklyData[i+1].DetailWeek.at(-1).FromDate)
                    days.push(((restTo-restFrom)/1000/3600/24).toFixed(2))
                }
                catch(error){
                    days.push("0")
                }
            }
            console.log(days)
            const request = new Request(`${this.generDepHost}/generateBurn`,
                {
                    method: "POST",
                    headers: { 
                            'Accept': 'application/json',
                            "Content-Type": "application/json",
                            },
                    body: JSON.stringify({"days":days})
                }
            )
            fetch(request)
            .then(response => response.json())
            .then(data => this.save(data, `${refuel.Name}_burn`))
            .catch(error => console.log(error))
        },
        save: saveFile,
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
        /* padding-right: 7px; */
        padding-bottom:10px;
        
    }
    .right {
        text-align: center;
        padding:0px;
    }
    .FC:hover {
        background: #eee;
    }
    #viewData .fa-ellipsis {
        position:absolute;
        /* margin:auto; */
        bottom:16px;
        right:0px;
    }
    #burn {
        position:absolute;
        /* margin:auto; */
        top:20px;
        /* right:15px; */
    }
    #viewData .btn {
        width: 100%;
    }
</style>