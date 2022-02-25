<template>
    <div class="DW-section" :style="{display:display}">
        <div class="row">
            <Table
            :data="rods"
            />
        </div>
        <div class="row">
            <div class="col"><b>Power</b></div>
            <div class="col"><b>Parameters</b></div>
        </div>
        <div v-for="dw in DW" :key=dw >
            <div class="row DW">
                <div class="col">
                    <div> {{dw.Power}}</div>
                </div>
                <div class="col">
                    <div class="row">
                        <div class="col right">
                            {{(dw.EnergyOutput).toFixed(1)}} Mev<span>&#215;</span>hours
                        </div>
                    </div>
                    <div class="row">
                        <div class="col right">
                            {{(dw.Time).toFixed(2)}} Hours            
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Table from "../Table.vue"
export default {
    name: "ViewDWData",
    components:{
        Table,
    },
    props:["DW", "rods", "display"],
    data(){
        return {
            data:""
        }
    },
}
</script>
<style>
    .DW-section {
        margin:auto;
        width:80%;
        border-top: 2px solid #eee;
        border-bottom: 2px solid #eee;
    }
    .WD:hover {
        background: #eee;
    }
</style>