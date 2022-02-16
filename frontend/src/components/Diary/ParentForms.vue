<template>
    <div> 
        <div class="row">
            <div class="col">
                <label for="FCname" class="form-label">Fuel Cycle Name</label>
                <Select :data="refuelingsList" @selected=getWeeksNum />
            </div>
            <div class="col">
                <label for="Week" class="form-label">Week</label>
                <Select :data="weeks" @selected=getWeekDetails />
                <!-- <Input v-model="week" name="Week" class="form-control" type="number"> </Input> -->
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
    data(){
        return {
            fcName: 0,
            weekNum:'',
            weeks: [],
            refuelingsList: []
        }
    },
    methods: {
        getWeeksNum(fcName) {
            this.fcName = fcName
            fetch(`${this.diaryDepHost}/weeksNum/${this.fcName}`)
            .then(response => response.json())
            .then(data => this.weeks=data)
            .catch((error) => console.log(error.message))
            console.log(this.weeks)
            
        },
        getWeekDetails(weekNum) {
            this.weekNum = weekNum
            this.submitHeader(this.weekNum, this.fcName)
            fetch(`${this.diaryDepHost}/weekDetails/${this.fcName}/${this.weekNum}`)
            .then(response => response.json())
            .then(data => this.submitDetails(data))
            .catch((error) => console.log(error.message))  
        },
        submitDetails(data){
            console.log(data)
            this.$emit("details", data)
        },
        //! will be initiated by watch?
        submitHeader(num, fcname) {
            this.$emit("headerData", num, fcname)
        }
    },
    created() {
            fetch(`${this.refuelDepHost}/refuelingsList`)
            .then(response => response.json())
            .then(data => (this.refuelingsList = data.names))
    },
    watch: {
        weeks() {
            if (typeof(this.weekNum) == "number"){
                this.getWeekDetails(this.weekNum)
            }
        }
    }
}
</script>