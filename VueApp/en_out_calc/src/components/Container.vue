<template>
<div>
    <div v-for="(obj,index) in data" v-bind:key="index">
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
        <Table v-model="data"></Table>
        <button @click="Submit" class="btn btn-primary"> Submit </button>
</div>
</template>

<script>
import Input from "./Input"
import Table from "./Table"

export default {
    name: "Container",
    components: {
        Input,
        Table,
    },
    data: function() {
        return {
            data: 
                [
                    {
                        power:6000,
                        fromDate:"",
                        toDate: "",
                        totalHours:5,
                        energyOutput:0,
                    },
                    {
                        power:5000,
                        fromDate:"",
                        toDate: "",
                        totalHours:0,
                        energyOutput:0,
                    }
                ]
        }
    },
    methods:{
        AddFileds(){
            this.data.push({})
        },
        Submit(){
            const request = new Request(
            "http://localhost:8888/post",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.data)
            }
       );
            fetch(request)
                .then(response => response.json())
    }
        }
}
</script>