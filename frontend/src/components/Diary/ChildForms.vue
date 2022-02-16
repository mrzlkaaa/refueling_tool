<template>
    <div>
        <div v-for="(obj,index) in weeklyDetail" v-bind:key="index">
            <div class="row">
                <div  class="col">
                    <label for="Power" class="form-label">Reactor Power</label>
                    <div class="input-group mb-3">
                        <Input v-model="obj.power" name="Power" type="number"/>
                        <span class="input-group-text" id="basic-addon2">kW </span>
                    </div>
                </div>
                <div class="col">
                    <label for="From" class="form-label">From </label>
                    <Input v-model="obj.fromDate" @assignToDate="setToDate(index)" name="From" class="form-control" type="datetime-local"/>
                </div>
                <div class="col">
                    <label for="To" class="form-label">To</label>
                    <Input v-model="obj.toDate"  name="To" class="form-control" type="datetime-local"/>
                    <i :class="[linked[index] ? 'fas fa-link active' : 'fas fa-link inactive']"
                        @click="toggleStyle(index)"
                    ></i>
                    <i class="fas fa-times" @click=onDelete(index)> </i>
                </div>
                
            </div> <br>
        </div>
        <Button
            class="btn btn-primary"
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
    data(){
        return {
            linked: [true],
        }
    },
    computed: {
        weeklyDetail:{
            get() {
                return this.modelValue
            },
            set(val){
                this.$emit("update:modelValue", val)
            }
        },
    },
    methods: {
        addFileds(){
            this.weeklyDetail.push({})
            this.linked.push(true)
        },
        onDelete(index){
            this.$emit("onDelete", index)
        }, 
        setToDate(index){
            if (this.linked[index]) {
                this.weeklyDetail[index].toDate = this.weeklyDetail[index].fromDate
                this.linked[index] = !this.linked[index]
            }
        },
        toggleStyle(index){this.linked[index]=!this.linked[index]}
    },
    watch: {
        modelValue: {
            deep: true,
            handler(newV) {
                if (newV.length < 2){
                    return
                }
                newV.at(-1).fromDate =  newV.at(-2).toDate
                // console.log(newV.at(-1))
                // console.log(newV.at(-2))
                this.setToDate(this.weeklyDetail.length-1)
            }
        },
    }
    // updated(){
    //     console.log(this.weeklyDetail)
    // }
}
</script>