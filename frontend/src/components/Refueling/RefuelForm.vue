<template>
    <!-- <div class="container"> -->
        <div class="forms-container">
            <div class="form-floating mb-3">
                <Select
                :optns="selectOpt"
                @selected="assignSelect"
                />
                <Label
                for="floatingSelect"
                text="Choose option"
                />
            </div>
            <div class="form-floating mb-3">
                <Input
                name="numbers"
                id="floatingInput"
                @typed="assignInput"
                />
                <Label
                for="floatingInput"
                text="FA numbers"
                />
            </div>
            <!-- <div class="arrows-container">
                <i @click="getNewConfig" class="fas fa-arrow-right fa-1x"></i>
            </div> -->
        </div>
        
    <!-- </div> -->
</template>
<script>
    import Input from "./Input.vue"
    import Select from "./Select.vue"
    import Label from "../Label.vue"
    import Button from "./Button.vue"
    import SO from "../../constants.js"
    export default {
        name: "RefuelForm",
        components:{
            Input,
            Select,
            Label,
            Button
        },
        props:{
            pdc: Array,
        },
        data(){
            return {
                valueee:"",
                data: {
                    action: "",
                    faNums: "",
                },
                selectOpt: SO,
            }
        },
        methods: {
            assignSelect(selected){
                this.data.action = selected
            },
            assignInput(inp){
                console.log(inp)
                this.data.faNums = inp
            },
            getNewConfig() {
                this.data.pdc = this.pdc
                console.log(this.data)
                const request = new Request(
                    `${this.procDepHost}/changes`,
                    {
                        method: "POST",
                        headers: { 
                                'Accept': 'application/json',
                                "Content-Type": "application/json",
                                'Access-Control-Allow-Origin': '*' },
                        body: JSON.stringify(this.data)
                    }
                );
                fetch(request)
                    .then(response => response.json())
                    .then(data => this.$emit("refuelForm", data))
                    .catch((error) => console.log(error.message))
            // console.log(this.fileData)
            },
        },
        // updated(){
        //     this.formsData
        // }
    }
</script>
<style>
    .forms-container {
        width:40%; 
        margin:auto;
    }
    .arrows-container {
        height:20px;
        margin:auto;
        position:relative;
    }
    .fa-arrow-right{
        position: absolute;
        left: 95%;
        color:#0d6efd;
    }
    .fa-arrow-right:hover{
        color:blue
    }
</style>