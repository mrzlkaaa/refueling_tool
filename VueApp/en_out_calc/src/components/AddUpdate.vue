<template>
<div>
    <Parent
        @headerData="headerData"
        @details="populateDetails"
    />
    <Child
        v-model="FormsData.weeklyDetail"
    />
    <Table v-model="FormsData.weeklyDetail"></Table>
    <button @click="submit" class="btn btn-primary"> Submit </button>
</div>
</template>

<script>
import Parent from "./ParentForms.vue"
import Child from "./ChildForms.vue"
import Table from "./Table.vue"

export default {
    name: "Container",
    components: {
        Parent,
        Child,
        Table,
        
    },
    data() {
        return {
            FormsData:{
                fcName: "",
                week: 0,
                weeklyDetail: [{}],
            },
        }
    },
    methods:{
        submit(){
            console.log(this.FormsData)
            const request = new Request(
            "http://localhost:8888/submitWeekData",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.FormsData)
            }
            );
            fetch(request)
                .then(response => response.json())
                .catch((error) => console.log(error.message))
            // this.FormsData.week += 1;
        },
        headerData(num, fcname) {
            this.FormsData.week = num
            this.FormsData.fcName = fcname
        },
        populateDetails(details) {
            this.FormsData.weeklyDetail = []
            if (details.length == 0) {
                this.FormsData.weeklyDetail.push({})
                this.changeTitle("Add")
            }
            for (let i = 0; i < details.length; i++) {
                let obj = {}
                obj.power = details[i].Power   
                obj.fromDate = details[i].FromDate
                obj.toDate = details[i].ToDate
                this.FormsData.weeklyDetail.push(obj)
                this.changeTitle("Update")
            }
        },
        changeTitle(val){
            this.$emit("msg",val)
        }
    },
}
</script>
