<template>
    <div> 
        <div class="row">
            <div class="col">
                <label for="FCname" class="form-label">Fuel Cycle Name</label>
                <Select 
                :data="refuelingsList"
                display="value"
                @selected=getWeeksNum />
            </div>
            <div class="col">
                <label for="Week" class="form-label">Week</label>
                <Select 
                :data="weeks" 
                display="key"
                @selected=getWeekDetails />
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
            weeks: {},
            refuelingsList: []
        }
    },
    methods: {
        getWeeksNum(fcName) {
            this.fcName = fcName
            fetch(`${this.diaryDepHost}/weeksNum/${this.fcName}`)
            .then(response => response.json())
            .then(data => (this.formatDate(data)))
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
        },
        formatDate(data){
            this.weeks = {}
            let obj = Object.keys(data)
                console.log(typeof(obj))
                for (let i = 0; i < obj.length-1; i++) {
                    // console.log(obj[i])
                    try{
                        let formattedDate = []
                        obj[i].split(" - ").forEach(e => {e = new Date(e)
                            formattedDate.push(e.toDateString())
                        })
                        obj[i] = formattedDate.join(" - ")
                    }
                    catch (error){
                        console.error(error)
                    }
                    
                }
                // let newData = {}
                for (let i=0; i < obj.length; i++) {
                    // const key = obj[i]
                    this.weeks[`${obj[i]}`] = Object.values(data)[i]
                }
                // this.data = newData
        }
    },
    created() {
            fetch(`${this.refuelDepHost}/refuelingsList`)
            .then(response => response.json())
            .then(data => (this.refuelingsList = data.names.sort((a,b) => b - a)))
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