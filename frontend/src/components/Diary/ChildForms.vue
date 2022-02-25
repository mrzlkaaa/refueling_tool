<template>
    <div>
        <div>
            <div class="row">
                <div class="col">
                    <Label
                    class="form-label"
                    for="AR"
                    text="AR"
                    />
                    <div class="input-group mb-3">
                        <Input
                        v-model="FormsData.rodsPosition.AR"
                        type="number"
                        :min="ksLimits[0]"
                        :max="ksLimits[1]"
                        />
                        <span class="input-group-text" id="basic-addon2">cm</span>
                    </div>
                </div>
                <div class="col">
                    <Label
                    class="form-label"
                    for="KS1"
                    text="KS1"
                    />
                    <div class="input-group mb-3">
                        <Input
                        v-model="FormsData.rodsPosition.KS1"
                        type="number"
                        :min="ksLimits[0]"
                        :max="ksLimits[1]"
                        />
                        <span class="input-group-text" id="basic-addon2">cm</span>
                    </div>
                </div>
                <div class="col">
                    <Label
                    class="form-label"
                    for="KS2"
                    text="KS2"
                    />
                    <div class="input-group mb-3">
                        <Input
                        v-model="FormsData.rodsPosition.KS2"
                        type="number"
                        :min="ksLimits[0]"
                        :max="ksLimits[1]"
                        />
                        <span class="input-group-text" id="basic-addon2">cm</span>
                    </div>
                </div>
                <div class="col">
                    <Label
                    class="form-label"
                    for="KS3"
                    text="KS3"
                    />
                    <div class="input-group mb-3">
                        <Input
                        v-model="FormsData.rodsPosition.KS3"
                        type="number"
                        :min="ksLimits[0]"
                        :max="ksLimits[1]"
                        />
                        <span class="input-group-text" id="basic-addon2">cm</span>
                    </div>
                </div>
                <div class="col">
                    <Label
                    class="form-label"
                    for="Temp"
                    text="Temperature"
                    />
                    <div class="input-group mb-3">
                        <Input
                        v-model="FormsData.rodsPosition.Temp"
                        type="number"
                        />
                        <span class="input-group-text" id="basic-addon2">&#176;C</span>
                    </div>
                </div>
            </div>
        </div>
        <br>
        <div v-for="(obj,index) in FormsData.weeklyDetail" v-bind:key="index">
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
            msg="Add Fields"
            class="btn btn-primary"
            @click="addFileds"
        />
    </div>
</template>

<script>
import Input from "./Input.vue"
import Button from "./Button.vue"
import Label from "../Label.vue"
export default {
    name: "Child",
    components: {
        Input,
        Button,
        Label,
    },
    props: ["modelValue"],
    data(){
        return {
            linked: [true],
            ksLimits:[0,60]
        }
    },
    computed: {
        FormsData:{
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
            this.FormsData.weeklyDetail.push({})
            this.linked.push(true)
        },
        onDelete(index){
            this.$emit("onDelete", index)
        }, 
        setToDate(index){
            if (this.linked[index]) {
                this.FormsData.weeklyDetail[index].toDate = this.FormsData.weeklyDetail[index].fromDate
                this.linked[index] = !this.linked[index]
            }
        },
        toggleStyle(index){this.linked[index]=!this.linked[index]}
    },
    watch: {
        modelValue: {
            deep: true,
            handler(newV) {
                if (newV.weeklyDetail.length < 2){
                    return
                }
                newV.weeklyDetail.at(-1).fromDate =  newV.weeklyDetail.at(-2).toDate
                // console.log(newV.at(-1))
                this.setToDate(this.FormsData.weeklyDetail.length-1)
            }
        },
    }
    // updated(){
    //     console.log(this.weeklyDetail)
    // }
}
</script>