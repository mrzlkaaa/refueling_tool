<template>
<div>
    <div class="row">
        <div class="col">
            <label for="FCname" class="form-label">Fuel Cycle Name</label>
            <!-- <Input v-model="Refuelings" name="FCname" class="form-control"> </Input> -->
            <Select v-bind:refuelingsList="RefuelingsList" @fc-update=GetWeeks> </Select>
        </div>
        <div class="col">
            <label for="Week" class="form-label">Week</label>
            <Input v-model="FormsData.week" name="Week" class="form-control" type="number"> </Input>
        </div>
    </div>
    <br>
    <div v-for="(obj,index) in FormsData.weeklyDetail" v-bind:key="index">
        <div class="row">
            <div  class="col" style="width:50%">
                <label for="Power" class="form-label">Reactor Power</label>
                <div class="input-group mb-3">
                    <Input v-model="obj.power" name="Power" type="number"> </Input>
                    <span class="input-group-text" id="basic-addon2">kW</span>
                </div>
            </div>
            <div class="col" style="width:50%">
                    <label for="From" class="form-label">From</label>
                    <Input v-model="obj.fromDate" name="From" class="form-control" type="datetime-local"> </Input>
                </div>
                <div class="col" style="width:50%">
                    <label for="To" class="form-label">To</label>
                    <Input v-model="obj.toDate" name="To" class="form-control" type="datetime-local"> </Input>
                </div>
        </div> <br>
        </div>
        <button @click="AddFileds" class="btn btn-primary"> Add fields </button> <br>
        <Table v-model="FormsData.weeklyDetail"></Table>
        <button @click="Submit" class="btn btn-primary"> Submit </button>
</div>
</template>

<script>
import Input from "./Input.vue"
import Table from "./Table.vue"
import Select from "./Select.vue"
export default {
    name: "Container",
    components: {
        Input,
        Table,
        Select
    },
    data() {
        return {
        FormsData:{
            fcName: "FC001",
            week: 1,
            weeklyDetail: 
            [
                {
                    power:6000,
                    fromDate:"",
                    toDate: "",
                    totalHours:5,
                    energyOutput:0,
                },
            ]
        },
        RefuelingsList: [],
        }
    },
    methods:{
        AddFileds(){
            this.FormsData.weeklyDetail.push({})
        },
        Submit(){
            const request = new Request(
            "http://localhost:8888/submitWeekData",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(this.FormsData)
                }
            );
            fetch(request)
                .then(response => response.json())
        },
        GetWeeks(fcname) {
            fetch(`http://localhost:8888/getNewWeekNum/${fcname}`)
            .then(response => response.json())
            .then(data => (this.FormsData.week = data))
            this.FormsData.fcName = fcname
        }
    },
    created() {
            fetch("http://localhost:8888/refuelingsList")
            .then(response => response.json())
            .then(data => (this.RefuelingsList = data.names))
    }
}
</script>


// FormsData:{
//                 fcName: "FC001",
//                 weeklyOuts:[
//                     {
//                         week: 1,
//                         weeklyDetail: 
//                         [
//                             {
//                                 power:6000,
//                                 fromDate:"",
//                                 toDate: "",
//                                 totalHours:5,
//                                 energyOutput:0,
//                             },
//                         ]
//                     }
//                 ]
                
//             },
//             Refuelings: [],
//         }
//     },