<template>
    <div>
        <div v-for="(obj,index) in weeklyDetail" v-bind:key="index">
            <div class="row">
                <div  class="col" style="width:50%">
                    <label for="Power" class="form-label">Reactor Power</label>
                    <div class="input-group mb-3">
                        <Input v-model="obj.power" name="Power" type="number"> </Input>
                        <span class="input-group-text" id="basic-addon2">kW </span>
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
    </div>
</template>

<script>
import Input from "./Input.vue"
export default {
    name: "Child",
    components: {
        Input,
    },
    props: ["modelValue"],
    computed: {
        weeklyDetail:{
            get() {
                return this.modelValue
            },
            set(val){
                this.$emit("update:modelValue", val)
            }
        }
    },
    methods: {
        AddFileds(){
            this.weeklyDetail.push({})
        },
    },
    updated() {
        console.log(this.weeklyDetail)
        // this.$emit("updateData", this.weeklyDetails)
    },
    // mounted(){
    //     this.$emit("updateData", this.weeklyDetails)
    // }
}
</script>