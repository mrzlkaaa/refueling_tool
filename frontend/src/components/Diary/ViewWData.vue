<template>
    <div class="WD-section" :style="{display:display}">
        <div class="row">
            <div class="col"><b>Weeks</b></div>
            <div class="col"><b>Parameters</b></div>
            <div class="col-2"><b>Criticality files</b></div>
            <div class="col-2"><b>Margin file</b></div>
        </div>
        <div v-for="wd in WD" :key=wd >
            <div class="row WD">
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
                    
                </div>
                <div class="col-2">
                    <i @click="onDownloadNoBurn(wd, 'criticality')" id="criticality" class="fas fa-file-export"> </i>
                </div>
                <div class="col-2">
                    <i @click="onDownloadNoBurn(wd, 'margin')" id="margin" class="fas fa-file-export"> </i>
                </div>
            </div>
            <div class="row">
                <i class="fa-solid fa-ellipsis fa-lg"></i>
                <Button
                class="btn btn-light"
                @click="toggleBlock(wd)"
                />
            </div>
            <ViewDWData
            :rods=wd.RodsPosition
            :DW="wd.DetailWeek"
            :display="wd.display"
            />
        </div>
    </div>
</template>
<script>
import ViewDWData from "./ViewDWData.vue"
import Button from "./Button.vue"
import { toggleBlock, dateStringFormatter, saveFile } from "../helpers"
export default {
    name: "ViewWData",
    components: {
        ViewDWData,
        Button,
    },
    props:["WD", "fcName", "display"],
    data(){
        return {
            data:""
        }
    },
    methods:{
        dateFormatter: dateStringFormatter,
        toggleBlock: toggleBlock,
        saveFile: saveFile,
        onDownloadNoBurn(wd, option){
            console.log(wd.RodsPosition.KS1)
            const request = new Request(`${this.generDepHost}/generateNoBurn`,
                {
                    method: "POST",
                    headers: { 
                            'Accept': 'application/json',
                            "Content-Type": "application/json",
                            },
                        body: JSON.stringify({
                            "option": option,
                            "fc_name": this.fcName,
                            "ar":wd.RodsPosition.AR,
                            "kc1":wd.RodsPosition.KS1,
                            "kc2":wd.RodsPosition.KS2,
                            "kc3":wd.RodsPosition.KS3,
                            "temp":wd.RodsPosition.Temp,
                        })
                }
            )
            fetch(request)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (option=="criticality") {
                    this.saveFile(data[0], `${this.fcName}_burn`)
                    this.saveFile(data[1], `geom_be_tvs_6layer_${this.fcName}`)
                }else{
                    this.saveFile(data, `${this.fcName}_burn`)
                }
            })
            .catch(error => console.log(error))

        }
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
    #criticality{
        position:absolute;
        /* right:0px; */
        top:27px;
        bottom:0px;
    }
    #margin{
        position:absolute;
        /* left:0px; */
        top:27px;
        bottom:0px;
        /* right:0px; */
    }
</style>