<template>
    <div>
        <div v-for="(obj,index) in weeklyDetail" v-bind:key="index">
            <div class="row">
                <div  class="col">
                    <label for="Power" class="form-label">Reactor Power</label>
                    <div class="input-group mb-3">
                        <Input v-model="obj.power" name="Power" type="number"> </Input>
                        <span class="input-group-text" id="basic-addon2">kW </span>
                    </div>
                </div>
                <div class="col">
                    <label for="From" class="form-label">From </label>
                    <Input v-model="obj.fromDate" name="From" class="form-control" type="datetime-local"> </Input>
                </div>
                <div class="col">
                    <label for="To" class="form-label">To</label>
                    <Input v-model="obj.toDate" name="To" class="form-control" type="datetime-local"> </Input>
                    <i class="fas fa-times" @click=onDelete(index)> </i>
                </div>
            </div> <br>
        </div>
        <Button 
            @click="addFileds"
        />
    </div>
</template>

<script>
import Input from "./Input.vue"
import Button from "./Button.vue"
export default {
    name: "Child",
    components: {
        Input,
        Button,
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
        addFileds(){
            this.weeklyDetail.push({})
        },
        onDelete(index){
            this.$emit("onDelete", index)
        }
    },
}
</script>