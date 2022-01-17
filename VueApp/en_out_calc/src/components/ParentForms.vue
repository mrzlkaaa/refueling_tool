<template>
    <div> 
        <div class="row">
            <div class="col">
                <label for="FCname" class="form-label">Fuel Cycle Name</label>
                <Select :refuelingsList="RefuelingsList" @fcName=getWeekNum> </Select>
            </div>
            <div class="col">
                <label for="Week" class="form-label">Week</label>
                <Input v-model="week" name="Week" class="form-control" type="number" disabled="disabled"> </Input>
            </div>
        </div>
    </div>
</template>

<script>
import Select from "./Select.vue"
import Input from "./Input.vue"

export default {
    name: "Parent",
    components: {
        Select,
        Input,
    },
    props: ["week"],
    data(){
        return {
            RefuelingsList: []
        }
    },
    methods: {
        getWeekNum(fcname) {
            fetch(`http://localhost:8888/getNewWeekNum/${fcname}`)
            .then(response => response.json())
            .then(data => (submitNewWeekNum(data, fcname)))
            .catch((error) => console.log(error.message))
            
        },
        submitNewWeekNum(num, fcname) {
            this.$emit("newWeekNum", num, fcname)
        }
    },
    created() {
            fetch("http://localhost:8888/refuelingsList")
            .then(response => response.json())
            .then(data => (this.RefuelingsList = data.names))
    },
}
</script>