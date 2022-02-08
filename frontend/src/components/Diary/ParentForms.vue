<template>
    <div> 
        <div class="row">
            <div class="col">
                <label for="FCname" class="form-label">Fuel Cycle Name</label>
                <SelectFC :data="refuelingsList" @fcName=getWeeksNum />
            </div>
            <div class="col">
                <label for="Week" class="form-label">Week</label>
                <SelectW :data="weeks" @weekName=getWeekDetails />
                <!-- <Input v-model="week" name="Week" class="form-control" type="number"> </Input> -->
            </div>
        </div>
    </div>
</template>

<script>
import SelectFC from "./SelectFC.vue"
import SelectW from "./SelectW.vue"
import Input from "./Input.vue"

export default {
    name: "Parent",
    components: {
        SelectFC,
        SelectW,
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
            fetch(`http://localhost:8889/WeeksNum/${this.fcName}`)
            .then(response => response.json())
            .then(data => this.weeks=data)
            .catch((error) => console.log(error.message))
            console.log(this.weeks)
            
        },
        getWeekDetails(weekNum) {
            this.weekNum = weekNum
            this.submitHeader(this.weekNum, this.fcName)
            fetch(`http://localhost:8889/WeekDetails/${this.fcName}/${this.weekNum}`)
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
            fetch("http://localhost:8888/refuelingsList")
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